#!/usr/bin/python3
"""A module that compresses the web static folder
   and deploys it to two web servers"""
from fabric.api import *
import datetime
import os


env.user = 'ubuntu'
env.hosts = ['54.90.50.38', '54.84.251.92']
env.key_filename = '~/.ssh/id_rsa'


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


def do_deploy(archive_path):
    """Distributes an archive to two web servers

    Return: True if all operations have been done correctly,
            otherwise returns False
    """
    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')

        filename = archive_path.split('/')[-1]
        compressed = '/tmp/' + filename
        uncompressed = "/data/web_static/releases/" + filename.split('.')[0]

        # make dir where uncompressed files are going to
        # ie /data/web_static/releases/web_static_223233232/
        run("sudo mkdir -p {}".format(uncompressed))

        # uncompress file in created folder.
        # It will now be /data/web_static/releases/
        # web_static_232343423/web_static
        run("sudo tar -xzf {} -C {}".format(compressed, uncompressed))

        # move content to the parent directory
        run("sudo mv {}/web_static/* {}".format(uncompressed, uncompressed))

        # delete the empty web_static dir
        run("sudo rm -rf {}/web_static/".format(uncompressed))

        # remove compressed file
        run("sudo rm {}".format(compressed))

        # delete former symbolic link
        run("sudo rm /data/web_static/current")

        # create new symbolic link to uncompressed files,
        run("sudo ln -s {} /data/web_static/current".format(uncompressed))

        return True
    except Exception:
        return False
