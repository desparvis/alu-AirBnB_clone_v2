#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""
import warnings
from cryptography.utils import CryptographyDeprecationWarning
from fabric import Connection
from os.path import exists

warnings.filterwarnings(action='ignore', category=CryptographyDeprecationWarning)

hosts = ["54.144.93.26", "3.80.93.124"]
user = "ubuntu"
key_filename = "~/.ssh/id_rsa"

def do_deploy(archive_path):
    """Function to distribute an archive to your web servers"""
    if not exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]
        path_name = "/data/web_static/releases/" + name
        
        for host in hosts:
            conn = Connection(host=host, user=user, connect_kwargs={"key_filename": key_filename})
            conn.put(archive_path, "/tmp/")
            conn.run("mkdir -p {}/".format(path_name))
            conn.run('tar -xzf /tmp/{} -C {}/'.format(file_name, path_name))
            conn.run("rm /tmp/{}".format(file_name))
            conn.run("mv {}/web_static/* {}".format(path_name, path_name))
            conn.run("rm -rf {}/web_static".format(path_name))
            conn.run('rm -rf /data/web_static/current')
            conn.run('ln -s {}/ /data/web_static/current'.format(path_name))
        
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False

# Run the script like this:
# $ python 2-do_deploy_web_static.py versions/file_name.tgz