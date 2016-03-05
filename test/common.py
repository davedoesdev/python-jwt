""" Common setup and patching for tests """

#pylint: disable=wrong-import-order
from datetime import datetime as orig_datetime, timedelta
from mock import patch
import threading
#pylint: disable=W0401,W0614
from test.fixtures import *

_thread_state = threading.local()

def _new_utcnow():
    """ Return last set datetime, or set it to current datetime if not set """
    if not hasattr(_thread_state, 'utcnow'):
        _thread_state.utcnow = orig_datetime.utcnow()
    return _thread_state.utcnow

def _new_now():
    """ Work out current local datetime """
    return _new_utcnow() + (orig_datetime.now() - orig_datetime.utcnow())

def clock_load(utcnow):
    """ Set datetime """
    _thread_state.utcnow = utcnow
    return _thread_state.utcnow

def clock_tick(delta=timedelta()):
    """ Tick clock """
    return clock_load(_new_utcnow() + delta)

def clock_reset():
    """ Forget set datetime """
    if hasattr(_thread_state, 'utcnow'):
        delattr(_thread_state, 'utcnow')

_config = {'utcnow.side_effect': _new_utcnow,
           'now.side_effect': _new_now}
_patcher = patch('datetime.datetime', **_config)
_mocker = _patcher.start()
