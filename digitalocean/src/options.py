"""Defines standard options across resources"""

import pulumi

opts=pulumi.ResourceOptions(retain_on_delete=True, protect=True)
