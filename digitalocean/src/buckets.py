import pulumi_digitalocean as do
import yaml

import pulumi

with open("params.yaml", "r") as f:
    params = yaml.safe_load(f)

REGION = params["region"]


def create_bucket(bucket_params: dict):
    """Creates a Spaces bucket.

    Args
    ---
    bucket_params: a dictionary of values to pass to do.SpacesBucket()
    """

    # ref: https://www.pulumi.com/docs/concepts/resources/providers/ (doesnt seem to work)
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
