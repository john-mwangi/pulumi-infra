"""A Python Pulumi program for Hetzner Cloud"""

import os

import pulumi
from dotenv import load_dotenv
from pulumi import ResourceOptions
from pulumi_hcloud import Provider, Server

load_dotenv()

SSH_PORT = os.environ["SSH_PORT"]
SSH_USER = os.environ["SSH_USER"]
SSH_PWD = os.environ["SSH_PWD"]
ALLOWED_PORTS = os.environ["ALLOWED_PORTS"]
ufw_allow = [f"sudo ufw allow {port.strip()}" for port in ALLOWED_PORTS.split(",")]

# pulumi config set --secret dev:hetzner_token XXX
config = pulumi.Config(name="dev")
hcloud = Provider("hcloud", token=config.require_secret("hetzner_token"))

# ref: https://community.hetzner.com/tutorials/security-ubuntu-settings-firewall-tools
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
    user_data=f"""#!/bin/bash
curl -fsSL https://get.docker.com/ | sh

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install -y ufw cron fail2ban
    
sed -i -e '/^\\(#\\|\\)PermitRootLogin/s/^.*$/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i -e '/^\\(#\\|\\)PasswordAuthentication/s/^.*$/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i -e '/^\\(#\\|\\)PubkeyAuthentication/s/^.*$/PubkeyAuthentication yes/' /etc/ssh/sshd_config
sed -i -e '/^\\(#\\|\\)Port/s/^.*$/Port {SSH_PORT}/' /etc/ssh/sshd_config
sed -i -e '/^\\(#\\|\\)KbdInteractiveAuthentication/s/^.*$/KbdInteractiveAuthentication no/' /etc/ssh/sshd_config
sed -i -e '/^\\(#\\|\\)ChallengeResponseAuthentication/s/^.*$/ChallengeResponseAuthentication no/' /etc/ssh/sshd_config
# sed -i -e '/^\\(#\\|\\)MaxAuthTries/s/^.*$/MaxAuthTries 2/' /etc/ssh/sshd_config
sed -i -e '/^\\(#\\|\\)AllowTcpForwarding/s/^.*$/AllowTcpForwarding yes/' /etc/ssh/sshd_config
sed -i -e '/^\\(#\\|\\)GatewayPorts/s/^.*$/GatewayPorts yes/' /etc/ssh/sshd_config
sed -i -e '/^\\(#\\|\\)X11Forwarding/s/^.*$/X11Forwarding no/' /etc/ssh/sshd_config
sed -i -e '/^\\(#\\|\\)AllowAgentForwarding/s/^.*$/AllowAgentForwarding no/' /etc/ssh/sshd_config
sed -i -e '/^\\(#\\|\\)AuthorizedKeysFile/s/^.*$/AuthorizedKeysFile .ssh/authorized_keys/' /etc/ssh/sshd_config
sed -i '$a AllowUsers {SSH_USER}' /etc/ssh/sshd_config

sudo systemctl stop ssh.socket
sudo systemctl restart ssh.service
sudo systemctl status ssh

sudo useradd -m -s /bin/bash {SSH_USER}
echo "{SSH_USER}:{SSH_PWD}" | sudo chpasswd
sudo usermod -aG sudo {SSH_USER}

sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow https
sudo ufw allow https
sudo ufw allow OpenSSH
{"\n".join(ufw_allow)}
    
sudo ufw enable
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
""",
)

pulumi.export("server01_ip", server01.ipv4_address)

with open("./README.md") as f:
    pulumi.export("readme", f.read())
