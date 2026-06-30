#!/usr/bin/env python3
"""Verify the exception fixes."""
import ast
import sys

FILE_PATH = (
    'c:/Users/bizle/OneDrive/bsean4890@gmail.com/.github/'
    'Equity-Shield-Advocates/Equity-Shield-Advocates/src/api_server.py'
)

# Count broad exceptions
with open(FILE_PATH, 'r', encoding="utf-8") as f:
    content = f.read()

count = content.count('except Exception')
print(f'Remaining "except Exception": {count}')

# Check syntax
try:
    ast.parse(content)
    print('Python syntax: OK')
except SyntaxError as e:
    print(f'Syntax error: {e}')
    sys.exit(1)
