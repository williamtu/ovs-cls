ovsdb/ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock \
        --remote=db:Open_vSwitch,Open_vSwitch,manager_options \
        --private-key=db:Open_vSwitch,SSL,private_key \
        --certificate=db:Open_vSwitch,SSL,certificate \
        --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert \
        --pidfile --detach --log-file
    #echo "r unix:/usr/local/var/run/openvswitch/db.sock --enable-dummy --pidfile"
    #gdb vswitchd/ovs-vswitchd
    gdb -ex=r --args vswitchd/ovs-vswitchd unix:/usr/local/var/run/openvswitch/db.sock --enable-dummy --pidfile --disable-system




ovs-vsctl add-br br0 -- set bridge br0 datapath_type=netdev
ovs-appctl dpctl/add-flow "in_port(121),eth(),eth_type(0x800),ipv4(src=12.1.1.0/255.255.255.0,dst=101.1.1.2)" 2
