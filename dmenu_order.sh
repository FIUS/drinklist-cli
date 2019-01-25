#!/bin/bash

DRINK=$(drinklist -columns name -format text list | tail -n +3 | dmenu)

if [ ! -z "$DRINK" ]; then
	drinklist order $DRINK &> /tmp/drinklist.out && notify-send -u normal "Drinklist $DRINK" "$(cat /tmp/drinklist.out)" || notify-send -u critical "Drinklist $DRINK FAILED" "$(cat /tmp/drinklist.out)"
fi
