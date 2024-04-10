# All resources will be in the same region
REGION = "ams3"

# ref: https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-gitlab-on-ubuntu-20-04
install_gitlab = """#!/bin/bash
sudo ufw allow http
sudo ufw allow https
sudo ufw allow OpenSSH
curl -fsSL https://get.docker.com/ | sh
docker system prune --all -f
docker run -d -p 443:443 -p 80:80 -p 23:22 --name gitlab_instance gitlab/gitlab-ce:latest
"""

# ref: https://slugs.do-api.dev/
gitlab_droplet_params = {
    "resource_name": "gitlab-server",
    "size": "s-4vcpu-8gb",
    "region": REGION,
    "image": "ubuntu-20-04-x64",
    "user_data": install_gitlab,
    "resize_disk": False,
}

resize_gitlab = {
    "id": None,
    "size": "s-4vcpu-8gb",
    "droplet_name": "gitlab-server",
    "is_backed_up": False,
}

pg_db_params = {"size": "db-s-2vcpu-4gb"}

outsystems_bucket_params = {
    "resource_name": "outsystems-bucket",
    "name": "outsystems-bucket",
    "region": REGION,
    "acl": "private",
    "force_destroy": False,
}

pyxis_bucket_params = {
    "resource_name": "pyxis-bucket",
    "name": "pyxis-bucket",
    "region": REGION,
    "acl": "private",
    "force_destroy": False,
}
