#!/bin/bash

DRINK=$(drinklist -format json list | python3 -c "import sys, json; [print(f['name']) for f in json.load(sys.stdin)]" | dmenu)

if [ ! -z "$DRINK" ]; then
	drinklist order $DRINK &> /tmp/drinklist.out && notify-send -u normal "Drinklist $DRINK" "$(cat /tmp/drinklist.out)" || notify-send -u critical "Drinklist $DRINK FAILED" "$(cat /tmp/drinklist.out)"
fi