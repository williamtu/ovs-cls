#!/usr/bin/python
import sys

MIN_UDP_SPORT = 2048

if __name__ == "__main__":
    N_SUBTABLES = int(sys.argv[1])
    N_RULES = int(sys.argv[2])
    assert N_RULES >= N_SUBTABLES

    rules_per_subtable = N_RULES / N_SUBTABLES

    if rules_per_subtable > 100:
        udp_port_range = 100
        ip_dst_range = rules_per_subtable /100
        # assert rules_per_subtable % 100 == 0
    else:
        udp_port_range = 1
        ip_dst_range = rules_per_subtable

    for i in range (0, N_SUBTABLES):
        flow = 'udp,nw_src='
        flow = flow + str(i + 1) + '.0.0.0/' + str(8 + i) + ','
        for j in range (0, ip_dst_range):
            a = j / 256 / 256;
            b = (j / 256) % 256;
            c = j % 256
            flow2 = flow + 'nw_dst=10.' + str(a) + '.' + str(b) + '.' + str(c) + '/32,tp_src=2048,'
            for k in range (20, 20 + udp_port_range):
                flow3 = flow2 + 'tp_dst=' + str(k) + ' '
                flow3 = flow3 + 'actions=output:2'
                print flow3
