#!/usr/bin/python3
"""This script creates and distributes an archive to web servers"""

from fabric.api import run, env, put, local
from datetime import datetime
import os

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = '<username>'
env.key_filename = '<path to ssh key>'


def do_pack():
    """Packs web_static files into .tgz archive"""
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = "versions/web_static_{}.tgz".format(now)
    local('mkdir -p versions')
    local('tar -cvzf {} web_static'.format(file_name))
    return file_name


def do_deploy(archive_path):
    """Distributes archive to web servers"""
    if os.path.isfile(archive_path) is False:
        return False

    file_name = archive_path.split('/')[-1]
    name = file_name.split('.')[0]
    releases = '/data/web_static/releases'
    symlink = '/data/web_static/current'

    try:
        put(archive_path, '/tmp/')
        run('mkdir -p {}/{}/'.format(releases, name))
        run('tar -xzf /tmp/{} -C {}/{}/'
            .format(file_name, releases, name))
        run('rm /tmp/{}'.format(file_name))
        run('mv {}/{}/web_static/* {}/{}/'
            .format(releases, name, releases, name))
        run('rm -rf {}/{}/web_static'.format(releases, name))
        run('rm -rf {}'.format(symlink))
        run('ln -s {}/{}/ {}'.format(releases, name, symlink))

        return True
    except:
        return False


def deploy():
    """Calls do_pack and do_deploy functions"""
    path = do_pack()

    if path is None:
        return False

    success = do_deploy(path)
    return success


def do_clean(number=0):
    """Deletes out-of-date archives"""
    if number == 0:
        number = 1
    number = int(number)
    archives = sorted(os.listdir("versions"))
    for archive in archives[:-number]:
        path = "versions/{}".format(archive)
        local("rm -rf {}".format(path))
    archive_releases = sorted(os.listdir("/data/web_static/releases"))
    for archive in archive_releases[:-number]:
        if archive != "test":
            path = "/data/web_static/releases/{}".format(archive)
            run("sudo rm -rf {}".format(path))
