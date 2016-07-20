#!/bin/bash
# port_and_prefix=':'$1
# kill -9 `lsof -P | grep $port_and_prefix | awk '{print $2}'`

kill -9 `lsof -i:$1 |tail -1|awk '{print $2}'`

