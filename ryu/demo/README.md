# upwan sdn 

```

创建
{
	"cmd_type":"create_mpls",
	"netid":1,
	"pe_vlan_ip":"192.168.22.1"
}

加路由
{
	"cmd_type":"add_route",
	"netid":1,
    "ipsec_ip_mask":"172.168.0.0/26",
	"nas_vlan_ip":"192.168.22.1"
}

删路由
{
	"cmd_type":"del_route",
	"netid":1,
    "ipsec_ip_mask":"172.168.0.1/26",
	"nas_vlan_ip":"192.168.22.1"
}

删除
{
	"cmd_type":"delete_mpls",
	"netid":1,
    "ipsec_ip_mask":"172.168.0.1/26",
	"nas_vlan_ip":"192.168.22.1"
}

```