# Pulumi Infrastructure as Code
Steps:
- Export your DigitalOcean Token: `$ export DIGITALOCEAN_TOKEN=XXXX`
- Alternative: `pulumi config set digitalocean:token YOUR_TOKEN_HERE --secret`
- Preview for errors: `$ pulumi preview`
- Create resources: `$ pulumi up`