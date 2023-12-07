#!/usr/bin/python3
"""
Deleting out-of-date archives
"""
import os.path
from fabric.api import *
from fabric.operations import run, put
from datetime import datetime


env.hosts = ['100.26.241.75', '100.27.12.186']
env.user = "ubuntu"


def deploy():
    """creates and distributes an archive to your web servers

    Returns:
        _type_: the do_deploy value.
    """
    archive_path = do_pack()
    if archive_path is None:
        print("Failed to create archive from web_static")
        return False
    return do_deploy(archive_path)


def do_pack():
    """ generates a .tgz archive from the content

    Returns:
        fabric.operations._AttributeString: path.
    """
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    )
    try:
        print("Packing web_static to {}".format(output))
        # extract the contents of a tar archive
        local("tar -cvzf {} web_static".format(output))
        archize_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archize_size))
    except Exception:
        output = None
    return output


def do_deploy(archive_path):
    """distributing an archive to your web servers.

    Args:
        archive_path (string): path 

    Returns:
        Boolean:  distributed or not
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False

    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        success = True

    except Exception:
        success = False
        print("Could not deploy")
    return success


def do_clean(number=0):
    """deleting out-of-date archives
    Args:
        number (int, optional): number of the archives, including the most
        recent, to keep. Defaults to 0.
    """
    archives = os.listdir('versions/')
    archives.sort(reverse=True)
    start = int(number)
    path = '/data/web_static/releases'
    if not start:
        start += 1
    if start < len(archives):
        archives = archives[start:]
    else:
        archives = []
    for archive in archives:
        os.unlink('versions/{}'.format(archive))
    cmd_parts = [
        "rm -rf $(",
        "find {}/ -maxdepth 1 -type d -iregex",
        " '{}/web_static_.*'",
        " | sort -r | tr '\\n' ' ' | cut -d ' ' -f{}-)"
        .format(path, path, start + 1)
    ]
    run(''.join(cmd_parts))
