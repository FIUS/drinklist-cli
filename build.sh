#!/bin/bash

cp src/drink.py __main__.py
zip drinklist.zip __main__.py src/ppformat.py src/levenshtein.py src/parameter_store.py src/utils.py
echo "#!/usr/bin/env python3" > packages/drinklist
cat drinklist.zip >> packages/drinklist
chmod +x packages/drinklist

rm __main__.py
rm drinklist.zip
