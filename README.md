# About
This is a repo for setting up cloud infrastructure as code using Pulumi. Refer
to readmes in the sub-directories for detailed instructions on how to set up for
various cloud service providers.

## Common commands
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