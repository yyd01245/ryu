import logging
import numbers
import socket
import struct
import json
import xmltodict
import lxml.etree as ET

# from ncclient.xml_ import *
from ncclient.xml_ import new_ele, sub_ele

from netconf_switch import NetconfSwitch

from upwan_type import *


class UpWanNetconfClient(NetconfSwitch):
  
  def __init__(self, switch_id, name, 
          host, port, username, 
          password,device_params):
    self._name = name   
    self._switch_id =  switch_id
    self._host = host
    self._port = port
    self._device_params = device_params
    super(UpWanNetconfClient, self).__init__(
        host=host, port=port, username=username, password=password,
        device_params=device_params,
        unknown_host_cb=lambda host, fingeprint: True)
  def __del__(self):
    self.close_session()

  def get_switch(self,data):
    # self._LOGGER.info('get_switch:%s',self._name )
    # return self._name 
    res = self.do_raw_get()
    result = {}
    result["node_name"]=self._name
    result["host"]=self._host
    result["port"]=self._port
    result["device_params"]=self._device_params
    result["switch_id"]=self._switch_id
    text = []
    print "-- type cap : %s" % type(self.netconf.server_capabilities)
    for i in self.netconf.server_capabilities:
      text.append(i)
    result["capabilities"] = text       
    result["node"]=res
    return result
    # return self.do_list_cap()
  def create_mpls(self,data):
    if REST_UID not in data.keys():
      return {"Execution":"error cannot find uid param"}
    if REST_MPLS_ACTION not in data.keys():
      return {"Execution":"error cannot find mpls_action"}
    uid = data[REST_UID]
    asn_nn = data[REST_MPLS_ACTION]
    text = create_template % (uid,asn_nn)
    print "get command: %s" % text
    node = ET.Element('Execution')
    node.text = text            
    print ET.tostring(node)
    cli_res = self.netconf.cli(node)
    res = xmltodict.parse(cli_res._raw)
    if "rpc-reply" in res.keys():
      res = res["rpc-reply"]["CLI"]
    print "--- res type=%s" % type(res)
    return res;

  def delete_mpls(self,data):
    if REST_UID not in data.keys():
      return {"Execution":"error cannot find uid param"}
    if REST_MPLS_ACTION not in data.keys():
      return {"Execution":"error cannot find mpls_action"}
    uid = data[REST_UID]
    asn_nn = data[REST_MPLS_ACTION]
    text = delete_template % (uid,asn_nn)
    print "get command: %s" % text
    node = ET.Element('Execution')
    node.text = text            
    print ET.tostring(node)
    cli_res = self.netconf.cli(node)
    res = xmltodict.parse(cli_res._raw)
    if "rpc-reply" in res.keys():
      res = res["rpc-reply"]["CLI"]
    print "--- res type=%s" % type(res)
    return res;

  def test_mpls(self,data):
    if REST_UID not in data.keys():
      return {"Execution":"error cannot find uid param"}
    if REST_MPLS_ACTION not in data.keys():
      return  {"Execution":"error cannot find mpls_action"}
    uid = data[REST_UID]
    asn_nn = data[REST_MPLS_ACTION]
    text = test_template % (uid,asn_nn)
    print "get command: %s" % text
    node = ET.Element('Execution')
    node.text = text            
    print ET.tostring(node)
    cli_res = self.netconf.cli(node)
    res = xmltodict.parse(cli_res._raw)
    if "rpc-reply" in res.keys():
      res = res["rpc-reply"]["CLI"]
    print "--- res type=%s" % type(res)
    return res;

  def cli_switch(self,data):
    print " ---- data : %s" % data
    
    print " ---- data cmd: %s" % data[REST_CMD_TYPE]
    # if REST_CMD not in data.keys():
    #     return "cannot find command"
    if REST_CMD_TYPE not in data.keys():
      return {"Execution":"error cannot find cmd_type param","code":ERROR_CODE}
    # cmd = data[REST_CMD]
    cmd_type = data[REST_CMD_TYPE]
    # node = ET.Element('Execution')
    # node.text = cmd     
    result_txt = ""   
    if cmd_type == CREATE_MPLS:
      result_txt = self.create_mpls(data)
    elif cmd_type == DELETE_MPLS:
      result_txt = self.delete_mpls(data)
    elif cmd_type == TEST_MPLS:
      result_txt = self.test_mpls(data)
    else: 
      result_txt = { "Execution":"unkown command"}
    result_code = SUCCESS_CODE
    for va in result_txt.values():
      print "--- in for %s" % va
      if va.find("error") >= 0 :
        result_code = ERROR_CODE
        break
    result_txt["code"] = result_code
    return result_txt

  def do_list_cap(self):
    """list_cap
    """
    text = []
    print "-- type cap : %s" % type(self.netconf.server_capabilities)
    for i in self.netconf.server_capabilities:
        text.append(i)

    return {"node_name":self._name, "switch_id":self._switch_id, "capabilities":text}
  def do_raw_get(self):
    """raw_get <peer>
    """
    c = self.netconf.get_config(source='running') 
    # .data_xml
    res = xmltodict.parse(c._raw)
    if "rpc-reply" in res.keys():
      res = res["rpc-reply"]["data"]["top"]
    return res

  def edit_switch(self,data):
    print 'edit_switch:%s' % self._name 
    # return self._name 

    # rpc_obj = self.netconf.edit_config(target='running', config=confstr)
    root = new_ele('config')
    configuration = sub_ele(root, 'configuration')
    system = sub_ele(configuration, 'system')
    location = sub_ele(system, 'location')
    sub_ele(location, 'building').text = "Main Campus, A"
    sub_ele(location, 'floor').text = "5"
    sub_ele(location, 'rack').text = "27"
    print ET.tostring(root)
    rpc_obj = self.netconf.edit_config(target='running',config=root)

    res = xmltodict.parse(rpc_obj._raw)        
    # if "rpc-reply" in res.keys():
    #     res = res["rpc-reply"]["data"]["top"]
    return res
    # return self.do_list_cap()

  def _validate(self, tree):
    xmlschema = _get_schema()
    try:
      xmlschema.assertValid(tree)
    except:
      traceback.print_exc()

  def raw_edit_config(self, target, config, default_operation=None,
                      test_option=None, error_option=None):
    self.netconf.edit_config(target, config,
                            default_operation, test_option, error_option)
  def _do_edit_config(self, config):
    tree = lxml.etree.fromstring(config)
    self._validate(tree)
    # self.switch.raw_edit_config(target='running', config=config)

  def do_raw_edit(self,target,capable_switch, default_operation=None):
    """raw_edit <peer>
    """
    xml = ofc.NETCONF_Config(capable_switch=capable_switch).to_xml()
    self.raw_edit_config(target, xml, default_operation)


  def _do_of_config(self):
    self._do_get()
    self._do_get_config('running')
    self._do_get_config('startup')

    # LINC doesn't support 'candidate' datastore
    try:
      self._do_get_config('candidate')
    except ncclient.NCClientError:
      traceback.print_exc()

    # use raw XML format
    self._do_edit_config(SWITCH_PORT_DOWN)
    self._do_edit_config(SWITCH_ADVERTISED)
    self._do_edit_config(SWITCH_CONTROLLER)

    self._set_ports_down()

    self.switch.close_session()

