import os

import pulumi_digitalocean as do

import pulumi

from src.options import opts


def create_droplet(kwargs: dict):
    """Creates a virtual machine on Digital Ocean

    Args:
    ---
    kwargs: key-word arguments for Droplet params
    """

    vm = do.Droplet(
        **kwargs,
        opts=opts,
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
