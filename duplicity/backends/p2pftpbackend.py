# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
import os

import duplicity.backend
from duplicity import log
from duplicity import path
from duplicity.errors import BackendException


class P2PFtpBackend(duplicity.backend.Backend):
    """Use this backend when saving to local disk

    Urls look like file://testfiles/output.  Relative to root can be
    gotten with extra slash (file:///usr/local).

    """
    def __init__(self, parsed_url):
        duplicity.backend.Backend.__init__(self, parsed_url)
        # The URL form "file:MyFile" is not a valid duplicity target.
        log.Info("init: %s" % (parsed_url.path[1:]))
        if not parsed_url.path.startswith('//'):
            raise BackendException("Bad file:// path syntax.")
        self.remote_pathdir = parsed_url.path[1:]

    def _put(self, source_path, remote_filename):
        log.Info("put: source - %s, remote - %s" % (source_path.name, remote_filename))
        self.subprocess_popen("p2pftp put {0} {1}/{2}".format(source_path.name, self.remote_pathdir, remote_filename))

    def _get(self, filename, local_path):
        log.Info("get: filename - %s, localpath - %s" % (filename, local_path))
        self.subprocess_popen("p2pftp get {0}/{1} {2}".format(self.remote_pathdir, filename, local_path))

    def _list(self):
        _, l, _ = self.subprocess_popen("p2pftp list {0}".format(self.remote_pathdir))
        o = l.splitlines()
        log.Info("result: %s" % o)
        return o

    def _delete(self, filename):
        log.Info("delete: filename - %s" % (filename))
        self.subprocess_popen("p2pftp delete {0}/{1}".format(self.remote_pathdir, filename))

duplicity.backend.register_backend("p2pftp", P2PFtpBackend)
