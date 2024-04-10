"""Spins resources on Digital Ocean"""

import os
from functools import reduce

import pulumi_digitalocean as do
from dotenv import load_dotenv

import pulumi

load_dotenv()

REGION = "ams3"


def create_droplet(kwargs: dict):
    """Creates a virtual machine on Digital Ocean

    Args:
    ---
    kwargs: key-word arguments for Droplet params
    """

    vm = do.Droplet(**kwargs)

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
    """Resizes an existing virtual machine and retains the IPv4 address.

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


def create_postgres_db(size: str):
    """Creates a Postgres database"""

    pg13_cluster = do.DatabaseCluster(
        resource_name="pg13-cluster",
        engine="pg",
        version="13",
        region=REGION,
        node_count=1,
        size=size,
    )

    crdb = do.DatabaseDb(
        resource_name="crdb",
        cluster_id=pg13_cluster.id,
        name=os.environ["CR_DB_NAME"],
    )

    pulumi.export("resource_id_spec", pg13_cluster.id)
    pulumi.export("resource_id_db", crdb.id)
    pulumi.export("db_user", pg13_cluster.user)
    pulumi.export("db_port", pg13_cluster.port)
    pulumi.export("db_name", crdb.name)
    pulumi.export("db_engine", pg13_cluster.engine)
    pulumi.export("db_version", pg13_cluster.version)


def create_bucket(bucket_params: dict):
    """Creates a Spaces bucket.

    Args
    ---
    bucket_params: a dictionary of values to pass to do.SpacesBucket()
    """

    provider = do.Provider(
        resource_name="bucket-provider",
        spaces_access_id=os.environ["SPACES_ACCESS_KEY_ID"],
        spaces_secret_key=os.environ["SPACES_SECRET_ACCESS_KEY"],
    )

    # ref: https://www.pulumi.com/registry/packages/digitalocean/api-docs/spacesbucket/
    outsystems_bucket = do.SpacesBucket(
        **bucket_params, opts=pulumi.ResourceOptions(provider=provider)
    )

    outsystems_bucket_cors = do.SpacesBucketCorsConfiguration(
        resource_name="outsystems-bucket-cors",
        bucket=outsystems_bucket.id,
        region=REGION,
        cors_rules=[
            do.SpacesBucketCorsConfigurationCorsRuleArgs(
                allowed_headers=["*"],
                allowed_methods=["POST", "PUT", "DELETE"],
                allowed_origins=["*"],
                max_age_seconds=3000,
            ),
            do.SpacesBucketCorsConfigurationCorsRuleArgs(
                allowed_headers=["*"],
                allowed_methods=["GET"],
                allowed_origins=["*"],
                max_age_seconds=3000,
            ),
        ],
    )

    pulumi.export("outsystems_bucket_id", outsystems_bucket.id)
    pulumi.export("outsystems_bucket_cors_id", outsystems_bucket_cors.id)
    pulumi.export("os_bucket_domain", outsystems_bucket.bucket_domain_name)
    pulumi.export("outsystems_bucket_endpoint", outsystems_bucket.endpoint)


def main(main_params: dict):
    """Create Digital Ocean resources.

    Args:
    ---
    main_params: the parameters to use
    """

    create_droplet(kwargs=main_params.get("gitlab_droplet_params"))

    droplet_to_resize = reduce(dict.get, ["resize_gitlab", "id"], main_params)
    if droplet_to_resize is not None:
        resize_droplet(**main_params.get("resize_gitlab"))

    pg_size = reduce(dict.get, ["pg_db_params", "size"], main_params)
    create_postgres_db(size=pg_size)

    create_bucket(bucket_params=main_params.get("outsystems_bucket_params"))


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
        "name": "outsystems-backups",
        "region": REGION,
        "acl": "private",
        "force_destroy": False,
    }

    main_params = {
        "gitlab_droplet_params": gitlab_droplet_params,
        "resize_gitlab": resize_gitlab,
        "pg_db_params": pg_db_params,
        "outsystems_bucket_params": outsystems_bucket_params,
    }

    main(main_params)
