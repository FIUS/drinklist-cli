#!/bin/bash

cp src/drink.py __main__.py
zip drinklist.zip __main__.py src/ppformat.py src/levenshtein.py src/parameter_store.py src/utils.py
echo "#!/usr/bin/env python3" > drinklist
cat drinklist.zip >> drinklist
chmod +x drinklist

rm __main__.py
rm drinklist.zip
