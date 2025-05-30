# Setup Hetzner Cloud with Pulumi

**1. Create a new Pulumi project**

Because Pulumi does not have a template for Hetzner Cloud, we will use a generic Python template to create a project.

```bash
pulumi new python
```

**2. Authenticate with Hezner Cloud**

Assuming that your stack is called `dev`, authenticate with your token.

```bash
pulumi config set --secret dev:hetzner_token XXX
# your fully-qualified stack name will be: pulumi-username/hetzner/dev
```

**3. Configure the project**

Install Pulumi Hetzner's Python package and update`__main__.py` to define your infrastructure.

```bash
pip install pulumi-hcloud
```

**4. Update the Pulumi virtual environment**

This updates the Pulumi virtual environment with the requirements.txt

```bash
pip list --format=freeze > requirements.txt
pulumi install
```

**5. Create the infrastructure**

```bash
pulumi preview
pulumi up
```

**6. Setting up SSH keys**
```bash
ssh-keygen -R <server-ip>
ssh-copy-id -i ~/.ssh/id_rsa.pub <ssh-user>@<server-ip>
ssh <ssh-user>@<server-ip>
```

# References
* https://mclare.blog/posts/using-pulumi-with-hetzner/
* https://docs.hetzner.com/cloud/api/getting-started/generating-api-token/
* https://www.pulumi.com/registry/packages/hcloud/api-docs/server/
* https://www.pulumi.com/docs/iac/languages-sdks/python/
* https://community.hetzner.com/tutorials/security-ubuntu-settings-firewall-tools
* https://community.hetzner.com/tutorials/basic-cloud-config
* https://community.hetzner.com/tutorials/howto-ssh-key