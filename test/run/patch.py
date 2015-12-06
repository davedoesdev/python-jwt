#!/usr/bin/env python
""" patch pyvows and coverage """

# pylint: disable=wrong-import-position,wrong-import-order,ungrouped-imports
import gevent.monkey
gevent.monkey.patch_all()
import pyvows.runner
import gevent.pool
pyvows.runner.gevent.VowsParallelRunner.pool = gevent.pool.Pool(50000)

from pyvows.core import Vows
from pyvows.runner import VowsRunner
from pyvows.result import VowsResult

# pylint: disable=too-few-public-methods
class _Dummy(object):
    # pylint: disable=missing-docstring
    @classmethod
    def run(cls, on_vow_success, on_vow_error):
        # Run batches in series
        r = VowsResult()
        for suite, batches in Vows.suites.items():
            for batch in batches:
                result = VowsRunner({suite: [batch]},
                                    Vows.Context,
                                    on_vow_success,
                                    on_vow_error,
                                    Vows.exclusion_patterns).run()
                r.contexts += result.contexts
                r.elapsed_time += result.elapsed_time
        return r

Vows.run = _Dummy.run

import sys
if sys.version_info >= (3, 0):
    import pyvows.reporting.common
    pyvows.reporting.common.unicode = str

import inspect
_orig_ismethod = inspect.ismethod
inspect.ismethod = lambda o: _orig_ismethod(o) or inspect.isfunction(o)

import coverage
import types
orig_coverage = coverage.coverage
def new_xml_report(self, *args, **kwargs):
    """ write html report too """
    self.html_report(directory='coverage/html')
    return self.orig_xml_report(*args, **kwargs)
def new_coverage(*args, **kwargs):
    """ xml_report """
    r = orig_coverage(*args, **kwargs)
    r.orig_xml_report = r.xml_report
    r.xml_report = types.MethodType(new_xml_report, r)
    return r
coverage.coverage = new_coverage
