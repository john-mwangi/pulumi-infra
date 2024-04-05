"""Spins a GitLab instance on DigitalOcean"""

import os

import pulumi_digitalocean as do
from dotenv import load_dotenv

import pulumi

load_dotenv()


def create_droplet(kwargs: dict, id: str, user_data: str = None):
    """Creates a virtual machine on Digital Ocean

    Args:
    ---
    kwargs: key-word arguments for Droplet params
    user_data: install script to run on the Linux machine
    """

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


def resize_droplet(
    id: str, size: str, droplet_name: str, is_backed_up: bool = False
):
    """Resizes an existing droplet and retains the IPv4 address.

    Args:
    ---
    id: The id of the Droplet to resize
    size: The new slug
    droplet_name: The resource name to assign the new Droplet
    """

    if not is_backed_up:
        print("Back up the data from the VM first")
        exit(0)

    # Get existing droplet
    existing_droplet = do.Droplet.get("existing-droplet", id)

    # Get reserved ip of the existing droplet
    # https://docs.digitalocean.com/products/networking/reserved-ips/how-to/modify/
    existing_reserved_ip = do.ReservedIp.get(
        "existing-reserved-ip", os.environ["VM_STATIC_IP"]
    )
    existing_reserved_ip.ip_address.apply(lambda ip: print("static_ip:", ip))

    # Create a new droplet
    new_droplet = do.Droplet(
        resource_name=droplet_name,
        image=existing_droplet.image,
        size=size,
        region=existing_droplet.region,
        user_data=existing_droplet.user_data,
        tags=existing_droplet.tags,
    )

    # Reassign the existing IP to the new droplet
    reassigned_ip = do.ReservedIpAssignment(
        "reassign-ip",
        droplet_id=new_droplet.id,
        ip_address=existing_reserved_ip.ip_address,
    )

    pulumi.export("vm_ip", new_droplet.ipv4_address)
    pulumi.export("static_ip", reassigned_ip.ip_address)
    pulumi.export("monthly_price_usd", new_droplet.price_monthly)
    pulumi.export("disk_size", new_droplet.disk)
    pulumi.export("ram", new_droplet.memory)


def create_database_instance(size: str, version: str):
    """Creates a database instance"""

    credit_risk_spec = do.DatabaseCluster(
        resource_name="credit-risk-spec",
        engine="pg",
        node_count=1,
        region="ams3",
        size=size,
        version=version,
    )

    credit_risk_db = do.DatabaseDb(
        resource_name="credit-risk-db",
        cluster_id=credit_risk_spec.id,
        name=os.environ["DB_NAME"],
    )

    pulumi.export("resource_id_spec", credit_risk_spec.id)
    pulumi.export("resource_id_db", credit_risk_db.id)
    pulumi.export("db_user", credit_risk_spec.user)
    pulumi.export("db_port", credit_risk_spec.port)
    pulumi.export("db_name", credit_risk_db.name)


if __name__ == "__main__":

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

    create_droplet(
        kwargs, id=os.environ["DROPLET_ID"], user_data=install_gitlab
    )

    # resize_droplet(
    #     id=os.environ["DROPLET_ID"],
    #     size="s-4vcpu-8gb",
    #     droplet_name="new-gitlab-server",
    #     is_backed_up=True,
    # )

    create_database_instance(size="db-s-2vcpu-4gb", version="13")
