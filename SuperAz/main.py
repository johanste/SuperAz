#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import sys
from cli.application import Application
    
if __name__=='__main__':
    app = Application()
    app.execute(sys.argv[1:])