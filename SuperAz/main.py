#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import sys
from cli.main import run

if __name__=='__main__':
    run(sys.argv[1:])