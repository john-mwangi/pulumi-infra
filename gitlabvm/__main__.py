"""Spins a GitLab instance on Pulumi"""

import pulumi_digitalocean as do

import pulumi


def create_droplet(kwargs: dict, user_data: str = None):
    """Creates a virtual machine on Digital Ocean"""

    vm = do.Droplet(
        **kwargs,
        resize_disk=False,
        user_data=user_data,
    )

    reserved_ip = do.ReservedIp(
        "reserved_ip",
        droplet_id=vm.id,
        region=vm.region,
    )

    pulumi.export("vm_ip", vm.ipv4_address)
    pulumi.export("static_ip", reserved_ip.ip_address)
    pulumi.export("monthly_price_usd", vm.price_monthly)
    pulumi.export("disk_size", vm.disk)
    pulumi.export("ram", vm.memory)


def resize_droplet(id: str, size: str):
    """Resizes and existing droplet and retains the IPv4 address"""

    existing_droplet = do.Droplet.get("existing-droplet", id)

    # https://docs.digitalocean.com/products/networking/reserved-ips/how-to/modify/
    existing_reserved_ip = do.ReservedIp.get("existing-reserved-ip", id)

    new_droplet = do.Droplet(
        "gitlab-server",
        image=existing_droplet.image,
        size=size,
        region=existing_droplet.region,
        user_data=existing_droplet.user_data,
        tags=existing_droplet.tags,
    )

    reserved_ip_assign = do.ReservedIpAssignment(
        "reserved-ip-assign",
        droplet_id=new_droplet.id,
        ip_address=existing_reserved_ip.ip_address,
    )

    pulumi.export("vm_ip", new_droplet.ipv4_address)
    pulumi.export("static_ip", reserved_ip_assign.ip_address)
    pulumi.export("monthly_price_usd", new_droplet.price_monthly)
    pulumi.export("disk_size", new_droplet.disk)
    pulumi.export("ram", new_droplet.memory)


if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()

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
    kwargs = {
        "resource_name": "gitlab-server",
        "size": "s-4vcpu-8gb",
        "region": "ams3",
        "image": "ubuntu-20-04-x64",
    }

    # create_droplet(kwargs, user_data=install_gitlab)
    # resize_droplet(id=os.environ["DROPLET_ID"], size="s-4vcpu-8gb")
