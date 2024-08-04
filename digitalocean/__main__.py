"""Spins resources on Digital Ocean"""

from functools import reduce

import pulumi_digitalocean as do
from dotenv import load_dotenv
from src.buckets import create_bucket
from src.databases import create_postgres_db_cluster
from src.droplets import create_droplet, resize_droplet
from src.projects import project as jmwangi

load_dotenv()

# creating the config: https://www.pulumi.com/docs/cli/commands/pulumi_config/
# creating an environment: https://www.pulumi.com/docs/cli/commands/pulumi_config_env/
# https://www.pulumi.com/docs/cli/commands/pulumi_env/


def create_first_project(main_params: dict):
    """Create Digital Ocean resources.

    Args:
    ---
    main_params: the parameters to use
    """

    # ================================================
    # Create resources here...
    # ================================================

    # VIRTUAL MACHINES
    gitlab_droplet, gitlab_ip = create_droplet(
        kwargs=main_params.get("gitlab_droplet_params")
    )

    droplet_to_resize = reduce(dict.get, ["resize_gitlab", "id"], main_params)
    if droplet_to_resize is not None:
        resize_droplet(**main_params.get("resize_gitlab"))

    # DATABASES
    pg_size = reduce(dict.get, ["pg_db_params", "size"], main_params)
    pg_cluster = create_postgres_db_cluster(size=pg_size)

    # BUCKETS
    # import_bucket("pyxis-bucket")
    os_bucket, os_cors = create_bucket(
        bucket_params=main_params.get("outsystems_bucket_params")
    )
    py_bucket, py_cors = create_bucket(
        bucket_params=main_params.get("pyxis_bucket_params")
    )

    # project = do.Project(
    #     resource_name="first-project",
    #     name="first-project",
    #     description="Update your project information under Settings",
    #     environment="Production",
    #     purpose="Operational / Developer tooling",
    #     is_default=True,
    #     resources=[
    #         gitlab_droplet.droplet_urn,
    #         gitlab_ip,
    #         pg_cluster.cluster_urn,
    #         os_bucket.bucket_urn,
    #         os_cors.urn,
    #         py_bucket.bucket_urn,
    #         py_cors.urn,
    #     ],
    # )

    # return project


if __name__ == "__main__":
    import yaml

    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)

    REGION = params["region"]

    create_first_project(params)
    jmwangi
