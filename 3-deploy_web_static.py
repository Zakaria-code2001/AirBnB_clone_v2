#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py) that creates and distributes an archive to your web servers
"""
from fabric.api import *
from datetime import datetime
import os

env.hosts = ['100.26.136.33', '54.90.34.106']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'

def do_pack():
    """
    Compresses web_static folder into .tgz archive
    """
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        filename = "versions/web_static_{}.tgz".format(now)
        local("tar -cvzf {} web_static".format(filename))
        return filename
    except:
        return None

def do_deploy(archive_path):
    """
    Deploys the web_static content to the web servers
    """
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        folder_name = archive_path.split("/")[-1][:-4]
        run("mkdir -p /data/web_static/releases/{}/".format(folder_name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            archive_path.split("/")[-1], folder_name))
        run("rm /tmp/{}".format(archive_path.split("/")[-1]))
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(folder_name, folder_name))
        run("rm -rf /data/web_static/releases/{}/web_static".format(folder_name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(folder_name))
        return True
    except:
        return False

def deploy():
    """
    Full deployment of web_static
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
