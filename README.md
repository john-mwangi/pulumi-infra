# Pulumi Infrastructure as Code
- Export your Digital Ocean Token: `$ export DIGITALOCEAN_TOKEN=XXXX`
- Alternative, create a config file: `pulumi config set digitalocean:token YOUR_TOKEN_HERE --secret`
- Preview for errors: `$ pulumi preview`
- Create resources: `$ pulumi up`
- Refresh Pulumi after creating resources manually: `$ pulumi refresh`
- If there is an error with pulumi refresh: `$ pulumi state delete`
- Create an environment from a config file: `pulumi config env init`