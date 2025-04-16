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

# Setting up Digital Ocean
- Export your Digital Ocean Token: `$ export DIGITALOCEAN_TOKEN=XXXX`
- Alternative, create a config file: `pulumi config set digitalocean:token YOUR_TOKEN_HERE --secret`

# Common commands
- `pulumi whoami` - Show the current user and organization.
- `pulumi logout` - Log out of the current Pulumi account.
- `pulumi login` - Log in to a Pulumi account.
- `pulumi config env init` - Initialize a new environment from a config file.
- `pulumi preview` - Preview the changes that would be made by `pulumi up`.
- `pulumi up` - Create or update the resources defined in your Pulumi program.
- `pulumi refresh` - Refresh the stack's state to match the current state of the resources.
- `pulumi state delete` - Delete a resource from the stack's state.
---
- `pulumi destroy` - Destroy the resources defined in your Pulumi program.
- `pulumi stack ls` - List all stacks in the current project.
- `pulumi stack select <stack-name>` - Select a specific stack to work with.
- `pulumi config` - Manage configuration values for your stack.
- `pulumi logs` - View logs for your stack.
- `pulumi stack export` - Export the current stack's state to a file.
- `pulumi stack import` - Import a stack's state from a file.
- `pulumi stack output` - Show the outputs of the current stack.
- `pulumi stack history` - Show the history of changes to the current stack.
- `pulumi stack init <stack-name>` - Initialize a new stack.
- `pulumi stack rm <stack-name>` - Remove a stack.
- `pulumi config set <key> <value>` - Set a configuration value for the current stack.
- `pulumi config rm <key>` - Remove a configuration value for the current stack.
- `pulumi config get <key>` - Get a configuration value for the current stack.
- `pulumi config refresh` - Refresh the configuration values for the current stack.
- `pulumi config set-all` - Set multiple configuration values for the current stack.
- `pulumi config rm-all` - Remove all configuration values for the current stack.

# References
* https://mclare.blog/posts/using-pulumi-with-hetzner/
* https://docs.hetzner.com/cloud/api/getting-started/generating-api-token/
* https://www.pulumi.com/registry/packages/hcloud/api-docs/server/
* https://www.pulumi.com/docs/iac/languages-sdks/python/
* https://community.hetzner.com/tutorials/security-ubuntu-settings-firewall-tools
* https://community.hetzner.com/tutorials/basic-cloud-config
* https://community.hetzner.com/tutorials/howto-ssh-key