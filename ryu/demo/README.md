# upwan sdn 

* [x] netconf 南向接口 CLI 实现
* [x] 北向实现挂载, 卸载 netconf 设备接口.
* [x] 北向实现创建、删除 mpls, 增加删除路由接口.
* [x] netconf 南向接口 CLI 实现
* [ ] 程序初始化挂载 netconf 设备
* [ ] 检测 netconf 设备在线状态, 断线重连


```

创建
{
	"cmd_type":"create_mpls",
	"netid":1,
	"pe_vlan_ip":"192.168.22.2/30",
	"nas_vlan_ip":"192.168.22.1"
}

加路由
{
	"cmd_type":"add_route",
	"netid":1,
	"route":"192.168.22.2/30",
	"next_route_ip":"192.168.22.1"
}

删路由
{
	"cmd_type":"del_route",
	"netid":1,
	"route":"192.168.22.2/30",
	"next_route_ip":"192.168.22.1"
}

删除
{
	"cmd_type":"delete_mpls",
	"netid":1
}

```


