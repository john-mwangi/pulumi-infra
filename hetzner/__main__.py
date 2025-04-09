"""A Python Pulumi program for Hetzner Cloud"""

import pulumi
from pulumi import ResourceOptions
from pulumi_hcloud import Provider, Server

# pulumi config set dev:token XXX --secret
config = pulumi.Config(name="dev")
hcloud = Provider("hcloud", token=config.require_secret("token"))

# Create a new server
server01 = Server(
    "server01",
    name="server01",
    image="ubuntu-24.04",
    server_type="cx32",
    delete_protection=True,
    rebuild_protection=True,
    keep_disk=True,
    location="fsn1",
    public_nets=[
        {
            "ipv4_enabled": True,
            "ipv6_enabled": True,
        }
    ],
    opts=ResourceOptions(provider=hcloud),
)

pulumi.export("server_ip", server01.ipv4_address)
