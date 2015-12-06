#!/usr/bin/env python
""" run pyvows after patching """

#pylint: disable=W0611,wrong-import-order
import test.run.patch

from pyvows.cli import main
import sys
if __name__ == '__main__':
    sys.exit(main())
