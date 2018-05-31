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
        timeout=120,
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
      return {"Execution":"error cannot find netid param"}
    if REST_PE_VLAN_IP not in data.keys():
      return {"Execution":"error cannot find pe_vlan_ip"}
    if REST_NAS_VLAN_IP not in data.keys():
      return {"Execution":"error cannot find nas_vlan_ip"}
    if REST_USER_IP not in data.keys():
      return {"Execution":"error cannot find user_ip"}
      
    # netid = "%d" % (data[REST_UID] + BEGIN_INTERFACE_ID)
    pe_vlan_ip = data[REST_PE_VLAN_IP]
    nas_vlan_ip = data[REST_NAS_VLAN_IP]
    # user_ip use ; split :1.1.1.1/24;2.2.2.2/24
    user_ip = data[REST_USER_IP]
    # print user_ip
    # print type(user_ip)
    strStation = ""
  
    for value in user_ip:
      # print "get station : ", value
      if strStation != "":
        strStation += ";"
      strStation += value
    print strStation

    param = create_param_template % ((data[REST_UID] + BEGIN_INTERFACE_ID),
               (data[REST_UID] + BEGIN_VLAN_ID),
               pe_vlan_ip,strStation,nas_vlan_ip)
    # txt_split = pe_vlan_ip.split("/")
    # ip = txt_split[0]
    # mask = txt_split[1]
    # param = "netid=%d,vlan=%d,vip=%s %s,nip=%s" % ((data[REST_UID] + BEGIN_INTERFACE_ID),
    #            (data[REST_UID] + BEGIN_VLAN_ID),
    #            ip,mask,nas_vlan_ip)
    text = create_template % (param)  
    # text = create_template % (netid,pe_vlan_ip)
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
      return {"Execution":"error cannot find netid param"}
    # if REST_ROUTE not in data.keys():
    #   return {"Execution":"error cannot find ipsec_ip_mask"}
    
    # netid = "%d" % (data[REST_UID] + BEGIN_INTERFACE_ID)
    # ipsec_mask = data[REST_ROUTE]
    # nas_vlan_ip = data[REST_NAS_VLAN_IP]
    param = "netid=%d,vlan=%d" % ((data[REST_UID] + BEGIN_INTERFACE_ID),
              (data[REST_UID] + BEGIN_VLAN_ID))
    text = delete_template % (param)
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

  def add_route(self,data):
    if REST_UID not in data.keys():
      return {"Execution":"error cannot find netid param"}
    if REST_ROUTE not in data.keys():
      return {"Execution":"error cannot find ipsec_ip_mask"}
    if REST_NEXT_ROUTE_IP not in data.keys():
      return {"Execution":"error cannot find next_route_ip"}
    user_ip = data[REST_ROUTE]
    next_route_ip = data[REST_NEXT_ROUTE_IP]

    strStation = ""
    for value in user_ip:
      # print "get station : ", value
      if strStation != "":
        strStation += ";"
      strStation += value
    print strStation
    # txt_split = ipsec_mask.split("/")
    # ip = txt_split[0]
    # mask = txt_split[1]
    # param = "netid=%d,vip=%s %s,nip=%s" % ((data[REST_UID] + BEGIN_INTERFACE_ID),
    #           ip,mask,next_route_ip)
    param = "netid=%d,ip=%s,nip=%s" % ((data[REST_UID] + BEGIN_INTERFACE_ID),
              strStation,next_route_ip)
    # todo multi ip mask cannot add chinese 
    text = add_route_template % (param)
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

  def del_route(self,data):
    if REST_UID not in data.keys():
      return {"Execution":"error cannot find netid param"}
    if REST_ROUTE not in data.keys():
      return {"Execution":"error cannot find ipsec_ip_mask"}
    if REST_NEXT_ROUTE_IP not in data.keys():
      return {"Execution":"error cannot find nas_vlan_ip"}
    user_ip = data[REST_ROUTE]
    next_route_ip = data[REST_NEXT_ROUTE_IP]

    strStation = ""
    for value in user_ip:
      # print "get station : ", value
      if strStation != "":
        strStation += ";"
      strStation += value
    print strStation

    # txt_split = ipsec_mask.split("/")
    # ip = txt_split[0]
    # mask = txt_split[1]
    # param = "netid=%d,vip=%s %s,nip=%s" % ((data[REST_UID] + BEGIN_INTERFACE_ID),
    #           ip,mask,next_route_ip)
    param = "netid=%d,vip=%s,nip=%s" % ((data[REST_UID] + BEGIN_INTERFACE_ID),
              strStation,next_route_ip)
    # todo multi ip mask cannot add chinese 
    text = del_route_template % (param)
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
      return {"Execution":"error cannot find netid param"}
    netid = "%d" % (data[REST_UID] + BEGIN_INTERFACE_ID)
    text = test_template % (netid)
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
    
    # print " ---- data cmd: %s" % data[REST_CMD_TYPE]
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
    elif cmd_type == ADD_ROUTE:
      result_txt = self.add_route(data)
    elif cmd_type == DEL_ROUTE:
      result_txt = self.del_route(data)
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

