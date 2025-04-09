# Setup Hetzner Cloud with Pulumi

**1. Create a new Pulumi project**

Because Pulumi does not have a template for Hetzner Cloud, we will use a generic Python template to create a project.

```bash
pulumi new python
```

**2. Authenticate with Hezner Cloud**

Assuming that your stack is called `dev`, authenticate with your token.

```bash
pulumi config set dev:token XXX --secret
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

# Setting up Digital Ocean
- Export your Digital Ocean Token: `$ export DIGITALOCEAN_TOKEN=XXXX`
- Alternative, create a config file: `pulumi config set digitalocean:token YOUR_TOKEN_HERE --secret`
- Preview for errors: `$ pulumi preview`
- Create resources: `$ pulumi up`
- Refresh Pulumi after creating resources manually: `$ pulumi refresh`
- If there is an error with pulumi refresh: `$ pulumi state delete`
- Create an environment from a config file: `pulumi config env init`

# References
* https://mclare.blog/posts/using-pulumi-with-hetzner/
* https://docs.hetzner.com/cloud/api/getting-started/generating-api-token/
* https://www.pulumi.com/registry/packages/hcloud/api-docs/server/
* https://www.pulumi.com/docs/iac/languages-sdks/python/