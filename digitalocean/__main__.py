"""Spins resources on Digital Ocean"""

import os
from functools import reduce

import pulumi_digitalocean as do
from dotenv import load_dotenv

import pulumi

load_dotenv()


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

    # ref: https://www.pulumi.com/registry/packages/digitalocean/api-docs/spacesbucket/
    bucket = do.SpacesBucket(**bucket_params)

    bucket_name = bucket_params.get("name")

    bucket_cors = do.SpacesBucketCorsConfiguration(
        resource_name=f"{bucket_name}-cors",
        bucket=bucket.id,
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

    pulumi.export("bucket_id", bucket.id)
    pulumi.export("bucket_cors_id", bucket_cors.id)
    pulumi.export("bucket_domain", bucket.bucket_domain_name)
    pulumi.export("bucket_endpoint", bucket.endpoint)


def import_bucket(bucket_name: str):
    """Imports a bucket into the Pulumi stack that was created via the Digital
    Ocean console"""

    bucket = do.SpacesBucket(
        bucket_name,
        name=bucket_name,
        region=REGION,
        opts=pulumi.ResourceOptions(import_=f"{REGION},{bucket_name}"),
    )

    pulumi.export("bucket_id", bucket.id)


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

    # import_bucket("pyxis-bucket")
    create_bucket(bucket_params=main_params.get("outsystems_bucket_params"))
    create_bucket(bucket_params=main_params.get("pyxis_bucket_params"))


if __name__ == "__main__":
    import yaml

    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)

    REGION = params["region"]

    main(params)
