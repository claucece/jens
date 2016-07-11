# Copyright (C) 2014, CERN
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.

import logging

from functools import wraps
from time import time
from git.exc import GitCommandError, NoSuchPathError
from jens.errors import JensGitError

def timed(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        elapsed = time() - start
        logging.info("Executed '%s' in %.2f ms" % (f.__name__, elapsed*1000))
        return result
    return wrapper

def git_exec(f):
    @wraps(f)
    def wrapper(*w_args, **w_kwargs):
        args = w_kwargs["args"]
        kwargs = w_kwargs["kwargs"]
        name = w_kwargs["name"]

        logging.debug("Executing git %s %s %s" % (name, args, kwargs))

        try:
            res = f(*args, **kwargs)
        except GitCommandError as e:
            raise JensGitError("Couldn't execute %s (%s)" %
                               (e.command, e.stderr))
        except NoSuchPathError as e:
            raise JensGitError("No such path %s" % e)
        return res

    return wrapper
