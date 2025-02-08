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
    """
    Deploy web files to the server.

    Args:
        archive_path (str): The path to the archive file to be deployed.

    Returns:
        bool: True if all operations were successful, otherwise False.

    The function performs the following steps:
    1. Checks if the archive path exists.
    2. Uploads the archive to the /tmp/ directory on the server.
    3. Creates the necessary directory structure on the server.
    4. Extracts the contents of the archive to the created directory.
    5. Deletes the uploaded archive from the /tmp/ directory.
    6. Moves the extracted files to the correct location.
    7. Removes the extraneous web_static directory.
    8. Deletes the old symbolic link to the web static content.
    9. Creates a new symbolic link to the web static content.
    """
    if not exists(archive_path):
        return False
    try:
        timestamp = archive_path[-18:-4]
        path_name = f"/data/web_static/releases/web_static_{timestamp}"
        
        for host in hosts:
            conn = Connection(host=host, user=user, connect_kwargs={"key_filename": key_filename})
            conn.put(archive_path, "/tmp/")
            conn.run(f"mkdir -p {path_name}/")
            conn.run(f"tar -xzf /tmp/web_static_{timestamp}.tgz -C {path_name}/")
            conn.run(f"rm /tmp/web_static_{timestamp}.tgz")
            conn.run(f"mv {path_name}/web_static/* {path_name}/")
            conn.run(f"rm -rf {path_name}/web_static")
            conn.run('rm -rf /data/web_static/current')
            conn.run(f"ln -s {path_name}/ /data/web_static/current")
        
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False

# Run the script like this:
# $ python 2-do_deploy_web_static.py versions/file_name.tgz
