# Setting up Digital Ocean
Export your Digital Ocean Token
```bash
export DIGITALOCEAN_TOKEN=XXXX
```
Alternative, create a config file
```bash
pulumi config set digitalocean:token YOUR_TOKEN_HERE --secret
```