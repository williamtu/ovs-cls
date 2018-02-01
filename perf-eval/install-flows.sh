#!/bin/bash
# argv[1]: # of subtables
# argv[2]: # of flows
ovs-ofctl del-flows br0
./gen-flows.py $1 $2  > flows.txt
ovs-ofctl add-flows br0 ./flows.txt
ovs-ofctl add-flow br0 "in_port=2 action=output:1"
ovs-ofctl dump-flows br0
ovs-ofctl dump-flows br0 | wc -l
