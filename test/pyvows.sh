#!/bin/bash
(
cat <<EOF

import gevent.monkey
gevent.monkey.patch_all()
import pyvows
import gevent.pool
pyvows.runner.gevent.VowsParallelRunner.pool = gevent.pool.Pool(50000)

import coverage
import types
orig_coverage = coverage.coverage
def new_xml_report(self, *args, **kwargs):
    self.html_report(directory='coverage/html')
    return self._orig_xml_report(*args, **kwargs)
def new_coverage(*args, **kwargs):
    r = orig_coverage(*args, **kwargs)
    r._orig_xml_report = r.xml_report
    r.xml_report = types.MethodType(new_xml_report, r)
    return r
coverage.coverage = new_coverage

EOF
cat "$(which pyvows)"
) | python - "$@"
