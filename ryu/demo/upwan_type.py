_ID_LEN = 4
ID_PATTERN = r'[0-9a-f]{%d}' % _ID_LEN
SWITCHID_PATTERN = ID_PATTERN + r'|all'

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
REST_ASN_NN = "asn_nn"
REST_ASN = "asn"
REST_IP_MASK = "ip_mask"
REST_NEXT_ROUTE = "next_route"
REST_IF_NAME = "if_name"

CREATE_MPLS = "create_mpls"

TEST_MPLS = "test_mpls"

DELETE_MPLS = "delete_mpls"

test_template = "python test.py %s %s "

create_template = "python create.py %s %s "

delete_template = "python delete.py %s %s "

add_route_template = "python route.py %s %s "

interface_template = "python interface.py %s %s "

add_station_template = "python station.py %s %s %s"