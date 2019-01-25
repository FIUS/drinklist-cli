#!/bin/bash

cp drink.py __main__.py
zip drinklist.zip __main__.py config.py ppformat.py
echo "#!/usr/bin/env python3" > drinklist
cat drinklist.zip >> drinklist
chmod +x drinklist

rm __main__.py
rm drinklist.zip