# _ID_LEN = 4
# ID_PATTERN = r'[0-9a-f]{%d}' % _ID_LEN
# SWITCHID_PATTERN = ID_PATTERN + r'|all'
SWITCHID_PATTERN = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'

REST_RESULT = 'result'
REST_DETAILS = 'details'
REST_OK = 'success'
REST_NG = 'failure'
REST_ALL = 'all'
REST_SWITCHID = 'switch_id'
RESR_NAME = 'name'
REST_USERNAME = 'username'
REST_PASSWORD = 'password'
REST_HOST = 'host'
REST_PORT = 'port'
REST_CMD = 'cmd'
REST_CMD_TYPE = 'cmd_type'
REST_DEVICES = 'device'
REST_UID = "netid"
REST_PE_VLAN_IP = 'pe_vlan_ip'
REST_NAS_VLAN_IP = 'nas_vlan_ip'
REST_ROUTE = 'route'
# REST_ASN_NN = "asn_nn"
# REST_MPLS_ACTION = "mpls_action"
# REST_ASN = "asn"
REST_NEXT_ROUTE_IP = "next_route_ip"
REST_IF_NAME = "if_name"

CREATE_MPLS = "create_mpls"
ADD_ROUTE = "add_route"
DEL_ROUTE = "del_route"
TEST_MPLS = "test_mpls"

DELETE_MPLS = "delete_mpls"

BEGIN_INTERFACE_ID = 10000
BEGIN_VLAN_ID = 1000
ERROR_CODE = 100
SUCCESS_CODE = 0

test_template = "python test.py %s "
# nn 10000 - uint32
# python vpn.py add_mpls "netid=10001,vlan=1001,vip=1.1.1.1 30,nip=21.1.2.1"

create_template = 'python vpn.py add_mpls "%s" '
# python vpn.py del_mpls "netid=10001,vlan=1001"
delete_template = 'python vpn.py del_mpls "%s" '
# python vpn.py add_route "netid=10001,vip=1.1.1.1 30,nip=21.1.2.1"
add_route_template = 'python vpn.py add_route "%s" '
# python vpn.py del_route "netid=10001,vip=1.1.1.1 30,nip=21.1.2.1"
del_route_template = 'python vpn.py del_route "%s" '

