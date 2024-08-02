"""Spins resources on Digital Ocean"""

from functools import reduce

from dotenv import load_dotenv
from src.buckets import create_bucket
from src.databases import create_postgres_db_cluster
from src.droplets import create_droplet, resize_droplet

load_dotenv()

# creating the config: https://www.pulumi.com/docs/cli/commands/pulumi_config/
# creating an environment: https://www.pulumi.com/docs/cli/commands/pulumi_config_env/
# https://www.pulumi.com/docs/cli/commands/pulumi_env/


def main(main_params: dict):
    """Create Digital Ocean resources.

    Args:
    ---
    main_params: the parameters to use
    """

    # Create resources here...
    # ================================================
    
    # VIRTUAL MACHINES
    create_droplet(kwargs=main_params.get("gitlab_droplet_params"))

    droplet_to_resize = reduce(dict.get, ["resize_gitlab", "id"], main_params)
    if droplet_to_resize is not None:
        resize_droplet(**main_params.get("resize_gitlab"))

    # DATABASES
    pg_size = reduce(dict.get, ["pg_db_params", "size"], main_params)
    create_postgres_db_cluster(size=pg_size)

    # BUCKETS
    # import_bucket("pyxis-bucket")
    create_bucket(bucket_params=main_params.get("outsystems_bucket_params"))
    create_bucket(bucket_params=main_params.get("pyxis_bucket_params"))


if __name__ == "__main__":
    import yaml

    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)

    REGION = params["region"]

    main(params)
