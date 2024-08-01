import os

import pulumi_digitalocean as do
import yaml

import pulumi

with open("params.yaml", "r") as f:
    params = yaml.safe_load(f)

REGION = params["region"]


def create_postgres_db_cluster(size: str):
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
