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
REST_UID = "uid"
# REST_ASN_NN = "asn_nn"
REST_MPLS_ACTION = "mpls_action"
REST_ASN = "asn"
REST_IP_MASK = "ip_mask"
REST_NEXT_ROUTE = "next_route"
REST_IF_NAME = "if_name"

CREATE_MPLS = "create_mpls"

TEST_MPLS = "test_mpls"

DELETE_MPLS = "delete_mpls"

ERROR_CODE = 100
SUCCESS_CODE = 0

test_template = "python test.py %s %s "
# nn 10000 - uint32
create_template = "python vpn.py %s %s "
# nn 10000 - uint32
delete_template = "python vpn.py %s %s "

add_route_template = "python route.py %s %s "

interface_template = "python interface.py %s %s "

add_station_template = "python station.py %s %s %s"