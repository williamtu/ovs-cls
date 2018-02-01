#!/usr/bin/python
# The command line arguments are as following
# argv[1]: # of subtables
# argv[2]: # of Openflow rules


import locale, sys, time
from signal import *

import stl_path
from trex_stl_lib.api import *

[tx_port, rx_port] = my_ports = [0, 1]
tx_ports = [tx_port]
rx_ports = [rx_port]

global c
global N_SUBTABLES
global N_RULES

# Test duration
RUN_TIME = 20

# Packet size
size = 64

#create stream blocks. Each stream has one srcIP with various dstIP.
#There are in total of 20 different srcIP.
def make_streams():
    rules_per_subtable = N_RULES / N_SUBTABLES

    if rules_per_subtable > 100:
        udp_port_range = 100
        ip_dst_range = rules_per_subtable /100
        # assert rules_per_subtable % 100 == 0
    else:
        udp_port_range = 1
        ip_dst_range = rules_per_subtable

    # calculate max_ip_dst, and max_udp_dport_dst
    max_udp_dport = 20 + udp_port_range - 1

    ip_dst_range = ip_dst_range - 1
    a = ip_dst_range / 256 / 256
    b = (ip_dst_range / 256) % 256
    c = ip_dst_range % 256
    max_ip_dst = '10.' + str(a) + '.' + str(b) + '.' + str(c)

    streams = [
        {"base_pkt":Ether()/IP(src="{}.0.0.0".format(i), tos=0x20)/UDP(sport=2048),
         "vm":[
            STLVmFlowVar(name="ip_dst", min_value="10.0.0.0",
                         max_value=max_ip_dst, size=4, op="random"),
            STLVmFlowVar(name="udp_dport", min_value=20,
                         max_value=max_udp_dport, size=2, op="random"),
            STLVmWrFlowVar(fv_name="ip_dst", pkt_offset="IP.dst"),
            STLVmWrFlowVar(fv_name="udp_dport", pkt_offset="UDP.dport"),
            ]
        }
        for i in range(1, N_SUBTABLES + 1)
    ]
    return streams

if __name__ == "__main__":

    N_SUBTABLES = int(sys.argv[1])
    N_RULES = int(sys.argv[2])
    assert N_RULES >= N_SUBTABLES

    c = STLClient(verbose_level = LoggerApi.VERBOSE_QUIET)
    c.connect()

    c.reset(ports = my_ports)
    new_streams = make_streams()

    for s in new_streams:
        # 64 - 4 for FCS
        pad = max(0, size - 4 - len(s["base_pkt"])) * 'x'
        s["base_pkt"] = s["base_pkt"]/pad

    pkts = [STLPktBuilder(pkt = s["base_pkt"], vm = s["vm"]) for s in new_streams]

    #generate contiguous traffic. Each stream has equal bandwidth.
    final_streams = [STLStream(packet = pkt, mode = STLTXCont(percentage = 100.0/len(pkts))) for pkt in pkts]
    c.add_streams(final_streams, ports=[tx_port])
    c.set_port_attr(my_ports, promiscuous = True)

    #start the traffic
    c.start(ports = tx_ports, mult = "8mpps", core_mask=STLClient.CORE_MASK_PIN, duration = RUN_TIME)

    #wait for 20 seconds
    time.sleep(RUN_TIME)
    #write rx pps to stdio
    sys.stdout.write(str("RX KPPS: ")+str(int(c.get_stats(my_ports)[1]["rx_pps"])/1000) + str("\n"))
    #stop the traffic
    c.stop(ports=my_ports)
    c.disconnect()
    c = None
