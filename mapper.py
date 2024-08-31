#! /usr/bin/python3
import json
import sys
for line in sys.stdin:
    obj = json.loads(line)
    if obj['artist']:
        print('{}\t{}'.format(obj['artist'], 1))