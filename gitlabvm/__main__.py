"""Spins a GitLab instance on Pulumi"""

import pulumi
import pulumi_digitalocean as do

# ref: https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-gitlab-on-ubuntu-20-04
install_gitlab = '''#!/bin/bash
sudo ufw allow http
sudo ufw allow https
sudo ufw allow OpenSSH
curl -fsSL https://get.docker.com/ | sh
docker system prune --all -f
docker run -d -p 443:443 -p 80:80 -p 23:22 --name gitlab_instance gitlab/gitlab-ce:latest
'''

vm = do.Droplet(
    resource_name="gitlab-server",
    image="ubuntu-20-04-x64",
    size="s-2vcpu-4gb",
    region="ams3",
    resize_disk=False,
    user_data=install_gitlab,
)

reserved_ip = do.ReservedIp("reserved_ip_3", droplet_id=vm.id, region=vm.region)

pulumi.export("vm_ip", vm.ipv4_address)
pulumi.export("static_ip", reserved_ip.ip_address)
pulumi.export("monthly_price_usd", vm.price_monthly)
pulumi.export("disk_size", vm.disk)
pulumi.export("ram", vm.memory)