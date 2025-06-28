import filecmp
import os
import subprocess

from dotenv import load_dotenv

load_dotenv()

SSH_PORT = os.environ["SSH_PORT"]


def create_script(filepath):
    bash_script = f"""#!/bin/bash
    sed -i -e 's/^#*PermitRootLogin .*/PermitRootLogin no/' sshd_config
    sed -i -e 's/^#*PasswordAuthentication .*/PasswordAuthentication no/' sshd_config
    sed -i -e 's/^#*PubkeyAuthentication .*/PubkeyAuthentication yes/' sshd_config
    sed -i -e 's/^#*Port .*/Port {SSH_PORT}/' sshd_config
    sed -i -e 's/^#*KbdInteractiveAuthentication .*/KbdInteractiveAuthentication no/' sshd_config
    sed -i -e 's/^#*ChallengeResponseAuthentication .*/ChallengeResponseAuthentication no/' sshd_config
    # sed -i -e 's/^#*MaxAuthTries .*/MaxAuthTries 2/' sshd_config
    sed -i -e 's/^#*AllowTcpForwarding .*/AllowTcpForwarding yes/' sshd_config
    sed -i -e 's/^#*GatewayPorts .*/GatewayPorts yes/' sshd_config
    sed -i -e 's/^#*X11Forwarding .*/X11Forwarding no/' sshd_config
    sed -i -e 's/^#*AllowAgentForwarding .*/AllowAgentForwarding no/' sshd_config
    # sed -i -e 's/^#*AuthorizedKeysFile .*/AuthorizedKeysFile .ssh\\/authorized_keys .ssh\\/authorized_keys2/' sshd_config
    """

    with open(filepath, "w") as f:
        f.write(bash_script)


def execute_script(filepath):
    subprocess.run(["chmod", "+x", filepath])
    result = subprocess.run(
        ["bash", filepath], capture_output=True, text=True, check=True
    )
    print(f"script {filepath} executed successfully")


if __name__ == "__main__":
    script_path = "./update_ssh.sh"
    create_script(script_path)
    execute_script(script_path)
    assert filecmp.cmp("./sshd_config.bak", "./sshd_config")
