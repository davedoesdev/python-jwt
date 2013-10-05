import bentomaker
import setuptools
from bento.distutils.monkey_patch import monkey_patch
monkey_patch()

from setuptools import setup

import types
from os import path
import shutil
import bento

# copy .egg-info to install directory and write it to install record

_orig_resolve_paths_with_destdir = bento.installed_package_description.BuildManifest.resolve_paths_with_destdir

_src = None
_dest = None

def resolve_paths_with_destdir(self, src_root_node):
    global _src, _dest
    _src = path.join('pip-egg-info', self.meta['name'] + '.egg-info')
    _dest = path.abspath(self.resolve_path(path.join('$sitedir', self.meta['name'] + '-' + self.meta['version'] + '-py$py_version_short.egg-info')))
    return _orig_resolve_paths_with_destdir(self, src_root_node)

bento.installed_package_description.BuildManifest.resolve_paths_with_destdir = resolve_paths_with_destdir

_orig_safe_write = bento.utils.io2.safe_write

def _safe_write(target, writer, mode="wb"):
    if target.endswith('install-record.txt'):
        _orig_writer = writer
        def _writer(fid):
            r = _orig_writer(fid)
            shutil.copytree(_src, _dest)
            fid.write(_dest + "\n")
            return r
        writer = _writer
    return _orig_safe_write(target, writer, mode)

bento.utils.io2.safe_write = _safe_write

if __name__ == '__main__':
    setup()
