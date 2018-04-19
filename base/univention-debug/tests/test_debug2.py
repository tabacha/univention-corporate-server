#!/usr/bin/python
import debug as ud
import debug2 as ud2

native = set(_ for _ in dir(ud) if not _.startswith('_'))
native -= set(('_debug', 'begin', 'end', 'exit'))
python = set(_ for _ in dir(ud2) if not _.startswith('_'))
python -= set(('sys', 'logging', 'DEFAULT'))

# The C implementation implements everything from the Python version
assert python <= native, 'Missing C implementation: %s' % (python - native,)

# The Python implementation implements everything from the C version
assert native <= python, 'Missing Python implementation: %s' % (native - python,)
