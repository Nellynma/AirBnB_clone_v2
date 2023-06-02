#!/usr/bin/python3
"""A module that generates a .tgz file using fabric"""
from fabric.api import local
import datetime


def do_pack():
    """generates a .tgz archive

    Return: path to archive on success; None on fail
    """

    now = datetime.datetime.now()
    filename = 'web_static_{}.tgz'.format(now.strftime('%Y%m%d%H%M%S'))
    local("mkdir -p versions")
    info = local("tar -cvzf versions/{} web_static".format(filename))
    if info.succeeded:
        return 'versions/{}'.format(filename)
    return None
