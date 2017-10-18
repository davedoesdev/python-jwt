#!/usr/bin/env python
""" patch pyvows and coverage """

# pylint: disable=wrong-import-position,wrong-import-order,ungrouped-imports
import gevent.monkey
gevent.monkey.patch_all()
import pyvows.runner
import gevent.pool
from pyvows.runner.gevent import VowsParallelRunner
VowsParallelRunner.pool = gevent.pool.Pool(50000)

from pyvows.core import Vows
from pyvows.runner import VowsRunner
from pyvows.runner.executionplan import ExecutionPlanner
from pyvows.result import VowsResult

VowsParallelRunner.orig_run_context = VowsParallelRunner.run_context

def new_run_context(self,
                    ctx_collection,
                    ctx_name,
                    ctx_obj,
                    execution_plan,
                    index=-1,
                    suite=None,
                    skipReason=None):
    """ Make sure exceptions in topic are caught """
    try:
        return self.orig_run_context(ctx_collection, ctx_name, ctx_obj, execution_plan, index, suite, skipReason)
    # pylint: disable=broad-except
    except Exception, e:
        ctx_collection[-1]['error'] = e

VowsParallelRunner.run_context = new_run_context

# pylint: disable=too-few-public-methods
class _Dummy(object):
    # pylint: disable=missing-docstring
    @classmethod
    def run(cls, on_vow_success, on_vow_error, capture_error=False):
        # Run batches in series
        r = VowsResult()
        for suite, batches in Vows.suites.items():
            for batch in batches:
                suites = {suite: [batch]}
                plan = ExecutionPlanner(suites,
                                        set(Vows.exclusion_patterns),
                                        set(Vows.inclusion_patterns)).plan()
                result = VowsRunner(suites,
                                    Vows.Context,
                                    on_vow_success,
                                    on_vow_error,
                                    plan,
                                    capture_error).run()
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
