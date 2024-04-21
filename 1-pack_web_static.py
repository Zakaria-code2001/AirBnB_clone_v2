#!/usr/bin/python3
"""
Compress before sending
"""

from datetime import datetime
from fabric.api import *


def do_pack():
    """
    creating an archive on web_static
    """

    time = datetime.now()
    archive = 'web_static_' + time.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'
    local('mkdir -p versions')
    create = local('tar -cvzf versions/{} web_static'.format(archive))
    if create is not None:
        return archive
    else:
        return None
