# Copyright (C) 2012 Nippon Telegraph and Telephone Corporation.
# Copyright (C) 2012 Isaku Yamahata <yamahata at private email ne jp>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module provides a set of REST API for switch configuration.
- Per-switch Key-Value store

Used by OpenStack Ryu agent.
"""

import logging
import numbers
import socket
import struct

import json

from upwan_type import *
from upwan_netconf_client import UpWanNetconfClient

from six.moves import http_client

from ryu.app.wsgi import ControllerBase
from ryu.app.wsgi import Response 
from ryu.app.wsgi import WSGIApplication
from ryu.base import app_manager
from ryu.lib import hub
from ryu.exception import RyuException
from ryu.controller import conf_switch
from ryu.lib import dpid as dpid_lib
from ryu.lib.of_config import classes as ofc


class NotFoundError(RyuException):
    message = 'switch is not connected. : switch_id=%(switch_id)s'

class NotNetconfError(RyuException):
    message = 'cannot find netconf info. : switch_id=%(switch_id)s'

class CommandFailure(RyuException):
    pass


# REST command template
def rest_command(func):
    def _rest_command(*args, **kwargs):
        try:
            msg = func(*args, **kwargs)
            return Response(content_type='application/json',
                            body=json.dumps(msg))

        except SyntaxError as e:
            status = 400
            details = e.msg
        except (ValueError, NameError) as e:
            status = 400
            details = e.message

        except NotFoundError as msg:
            status = 404
            details = str(msg)

        msg = {REST_RESULT: REST_NG,
               REST_DETAILS: details}
        return Response(status=status, body=json.dumps(msg))

    return _rest_command

def _get_schema():
    # file_name = of_config.OF_CONFIG_1_0_XSD
    # file_name = of_config.OF_CONFIG_1_1_XSD
    file_name = of_config.OF_CONFIG_1_1_1_XSD
    return lxml.etree.XMLSchema(file=file_name)

class UpWanSwitchController(ControllerBase):
    # _SWITCH_LIST = {}
    _LOGGER = None

    def __init__(self, req, link, data, **config):
        super(UpWanSwitchController, self).__init__(req, link, data, **config)
        # self.monitor_thread = hub.spawn(self._monitor)
        # self.conf_switch = data
    @classmethod
    def set_logger(cls, logger):
        cls._LOGGER = logger
        cls._LOGGER.propagate = False
        hdlr = logging.StreamHandler()
        fmt_str = '[RT][%(levelname)s] : %(message)s'
        hdlr.setFormatter(logging.Formatter(fmt_str))
        cls._LOGGER.addHandler(hdlr)

    @classmethod
    def register_switch(cls, switch_id, data ):
        details = None
        cls._LOGGER.info('register_switch:%s',switch_id)

        try:
            # Set address data
            name = data[RESR_NAME]
            username = data[REST_USERNAME]
            password = data[REST_PASSWORD]
            port = data[REST_PORT]
            host = data[REST_HOST]
            device_params = {}
            if REST_DEVICES in data.keys():
                device_params = data[REST_DEVICES]
            cls._LOGGER.info('username:%s',username)
            switch = UpWanNetconfClient(switch_id=switch_id,name=name, host=host, 
                port=port, username=username, password=password,
                device_params=device_params)   
            # switch = UpWanNetconfClient(switch_id,name, host, 
            #     port, username, password,device_params)             
            details = 'register new neconf switch [switch_id=%s,name=%s]' % (switch_id,name)
            
        except CommandFailure as err_msg:
            msg = {REST_RESULT: REST_NG, REST_DETAILS: str(err_msg)}
            msg.setdefault(REST_SWITCHID, switch_id)
            return msg

        if details is not None:
            msg = {REST_RESULT: REST_OK, REST_DETAILS: details}
            cls._SWITCH_LIST.setdefault(switch_id, switch)

            cls._LOGGER.info('register_switch netconf switch. %s', switch_id)
            msg.setdefault(REST_SWITCHID, switch_id)            
            return msg
        else:
            raise ValueError('Invalid parameter.')                
        
    @classmethod
    def mount_switch(cls, switch_id, data ):
        details = None
        cls._LOGGER.info('register_switch:%s',switch_id)

        try:
            # Set address data
            name = data[RESR_NAME]
            username = data[REST_USERNAME]
            password = data[REST_PASSWORD]
            port = data[REST_PORT]
            host = data[REST_HOST]
            device_params = {}
            if REST_DEVICES in data.keys():
                device_params = data[REST_DEVICES]
            cls._LOGGER.info('username:%s',username)
            switch = UpWanNetconfClient(switch_id=switch_id,name=name, host=host, 
                port=port, username=username, password=password,
                device_params=device_params)   
            # switch = UpWanNetconfClient(switch_id,name, host, 
            #     port, username, password,device_params)             
            details = 'mount new neconf switch [switch_id=%s,name=%s]' % (switch_id,name)
            
        except CommandFailure as err_msg:
            msg = {REST_RESULT: REST_NG, REST_DETAILS: str(err_msg)}
            msg.setdefault(REST_SWITCHID, switch_id)
            return (msg,None)

        if details is not None:
            msg = {REST_RESULT: REST_OK, REST_DETAILS: details}

            cls._LOGGER.info('mount_switch netconf switch. %s', switch_id)
            msg.setdefault(REST_SWITCHID, switch_id)            
            return (msg,switch)
        else:
            raise ValueError('Invalid parameter.')                
        
 
    @classmethod
    def unmount_switch(cls, switch_id, switch):
        cls._LOGGER.info('begin Leave switch %s.', switch_id)
        del switch       
        cls._LOGGER.info('Leave switch %s.', switch_id)
        valu = "delete switch %s success." % switch_id
        return {"result":valu}       

    @classmethod
    def unregister_switch(cls, switch_id):
        cls._LOGGER.info('begin Leave switch %s.', switch_id)

        if switch_id in cls._SWITCH_LIST:
            # cls._SWITCH_LIST[switch_id].delete()
            ob = cls._SWITCH_LIST[switch_id]
            cls._SWITCH_LIST.pop(switch_id)
            del ob       
            cls._LOGGER.info('Leave switch %s.', switch_id)
        valu = "delete switch %s success." % switch_id
        return {"result":valu}

    @rest_command
    def list_switches(self, _req, **_kwargs):
        # dpids = self.conf_switch.dpids()
        body = json.dumps("hello list_switches")
        return Response(content_type='application/json', body=body)

    # @rest_command
    # def get_switch(self, req, switch_id, **_kwargs):
    #     # dpids = self.conf_switch.dpids()
    #     body = json.dumps("hello get_switch")
    #     return Response(content_type='application/json', body=body)

    @rest_command
    def get_switch(self, req, switch_id, **_kwargs):
        self._LOGGER.info('get_switch netconf switch:%s',switch_id)
        return self._access_switch(switch_id,'get_switch', req)


    # @rest_command        
    # def connect_switch(self, _req, switch_id, **_kwargs):
    #     self._LOGGER.info('Join netconf switch:%s',switch_id)
    #     return self._access_switch(switch_id,'config_switch', req)

    @rest_command         
    def config_switch(self, _req, switch_id, **_kwargs):
        self._LOGGER.info('1 config_switch netconf switch:%s',switch_id)
        try:
            param = _req.json if _req.body else {}
        except ValueError:
            raise SyntaxError('invalid syntax %s', _req.body)
        #check id if exist
        # if switch_id in self._SWITCH_LIST.keys():
        #     return "node switch id %s is exist" % switch_id

        return UpWanSwitchController.register_switch(switch_id,param)
        # body = json.dumps(msg)
        # return Response(content_type='application/json', body=body)        
        # return self._access_switch(switch_id,'config_switch', req)

    @rest_command        
    def edit_switch(self, _req, switch_id, **_kwargs):
        self._LOGGER.info('edit_switch netconf switch:%s',switch_id)
        return self._access_switch(switch_id,'edit_switch', _req)

    @rest_command        
    def cli_switch(self, _req, switch_id, **_kwargs):
        self._LOGGER.info('cli_switch netconf switch:%s',switch_id)
        return self._access_switch(switch_id,'cli_switch', _req)

    @rest_command         
    def delete_switch(self, _req, switch_id, **_kwargs):
        # self._LOGGER.info('delete_switch netconf switch:%s',switch_id)
        # return self._access_switch(switch_id,'delete_switch', _req)
        return UpWanSwitchController.unregister_switch(switch_id)

    # def _access_switch(self, switch_id, func, req):
    #     rest_message = []
    #     self._LOGGER.info('_access_switch:%s',switch_id)        
    #     switches = self._get_switch(switch_id)
    #     try:
    #         param = req.json if req.body else {}
    #     except ValueError:
    #         raise SyntaxError('invalid syntax %s', req.body)
    #     for switch in switches.values():
    #         function = getattr(switch, func)
    #         # body data as param
    #         data = function(param)
    #         rest_message.append(data)
    #     return rest_message
    def _access_switch(self, switch_id, func, req):
        self._LOGGER.info('_access_switch:%s',switch_id)        
        # switches = self._get_switch(switch_id,req)
        switches = self._create_switch(switch_id,req)        
        try:
            param = req.json if req.body else {}
        except ValueError:
            raise SyntaxError('invalid syntax %s', req.body)
        for switch in switches.values():
            function = getattr(switch, func)
            # body data as param
            data = function(param)
            # unmount
            del switch
            return data
    def _create_switch(self, switch_id,_req):
        switches = {}
        self._LOGGER.info('_get_switch: %s',switch_id)  

        # mount netconf
        try:
            param = _req.json if _req.body else {}
            if REST_NETCONF_INFO not in param.keys():
                raise NotNetconfError(switch_id=switch_id)
        except ValueError:
            raise SyntaxError('invalid syntax %s', _req.body)            

        self._LOGGER.info('register_switch netconf switch. %s', switch_id) 
        self._LOGGER.info('info netconf switch. %s', param[REST_NETCONF_INFO])                                   
        (msg,switch) = UpWanSwitchController.mount_switch(switch_id,param[REST_NETCONF_INFO])
        if switch:
            return {switch_id: switch}
        else:
            raise NotFoundError(switch_id=switch_id)
                
    def _get_switch(self, switch_id,_req):
        switches = {}
        self._LOGGER.info('_get_switch: %s',switch_id)  
        for k in self._SWITCH_LIST:
           self._LOGGER.info('list in switches: k=%s,v=%s',k,self._SWITCH_LIST[k])   

        if switch_id == REST_ALL:
            switches = self._SWITCH_LIST
        else:
            # sw_id = dpid_lib.str_to_dpid(switch_id)
            if switch_id in self._SWITCH_LIST:
                switches = {switch_id: self._SWITCH_LIST[switch_id]}

        if switches:
            self._LOGGER.info('find switch: %s',switch_id)        
            return switches
        else:
            # mount netconf
            try:
                param = _req.json if _req.body else {}
                if REST_NETCONF_INFO not in param.keys():
                    raise NotNetconfError(switch_id=switch_id)
            except ValueError:
                raise SyntaxError('invalid syntax %s', _req.body)            

            self._LOGGER.info('register_switch netconf switch. %s', switch_id) 
            self._LOGGER.info('info netconf switch. %s', param[REST_NETCONF_INFO])                                   
            UpWanSwitchController.register_switch(switch_id,param[REST_NETCONF_INFO])
            if switch_id in self._SWITCH_LIST:
                return {switch_id: self._SWITCH_LIST[switch_id]}
            else:
                raise NotFoundError(switch_id=switch_id)
    
    # def _monitor(self):
    #     while True:
    #         for dp in self._SWITCH_LIST.values():
                
    #         hub.sleep(10)

class UpWanSwitchAPI(app_manager.RyuApp):
    # _CONTEXTS = {
    #     'conf_switch': conf_switch.ConfSwitchSet,
    # }
    _CONTEXTS = {'wsgi': WSGIApplication}


    def __init__(self, *args, **kwargs):
        super(UpWanSwitchAPI, self).__init__(*args, **kwargs)
        wsgi = kwargs['wsgi']
        mapper = wsgi.mapper

        # use data
        self.conf_switch = {}

        UpWanSwitchController.set_logger(self.logger)
        controller = UpWanSwitchController

        wsgi.registory[controller.__name__] = self.conf_switch
        requirements = {'switch_id': SWITCHID_PATTERN}

        # For no vlan data
        # rootPath = '/upwan'
        path = '/upwan/{switch_id}'
        cliPath = '/upwan/cli/{switch_id}'
        editPath = '/upwan/edit_config/{switch_id}'
        # mapper.connect('upwan', rootPath, controller=UpWanSwitchController,
        #             #    requirements=requirements,
        #                action='list_switches',
        #                conditions=dict(method=['GET']))

        mapper.connect('upwan', path, controller=UpWanSwitchController,
                       requirements=requirements,
                       action='get_switch',
                       conditions=dict(method=['GET']))                       
        mapper.connect('upwan', path, controller=UpWanSwitchController,
                       requirements=requirements,
                       action='config_switch',
                       conditions=dict(method=['POST']))  

        mapper.connect('upwan', editPath, controller=UpWanSwitchController,
                       requirements=requirements,
                       action='edit_switch',
                       conditions=dict(method=['POST']))    

        mapper.connect('upwan', cliPath, controller=UpWanSwitchController,
                       requirements=requirements,
                       action='cli_switch',
                       conditions=dict(method=['POST']))                                           
        mapper.connect('upwan', path, controller=UpWanSwitchController,
                       requirements=requirements,
                       action='delete_switch',
                       conditions=dict(method=['DELETE']))
