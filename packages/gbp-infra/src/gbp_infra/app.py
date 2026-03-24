from pathlib import Path

import aws_cdk as cdk

from gbp_infra.app_stack import AppStack
from gbp_infra.config import Config
from gbp_infra.database_stack import DatabaseStack

REPO_ROOT = Path(__file__).resolve().parents[4]

config = Config()
app = cdk.App()
env = cdk.Environment(region=config.aws_region)

for key, value in config.tags.items():
    cdk.Tags.of(app).add(key, value)

database_stack = DatabaseStack(app, config.stack_name("database"), env=env)

AppStack(
    app,
    config.stack_name("app"),
    env=env,
    vpc=database_stack.vpc,
    file_system=database_stack.file_system,
    access_point=database_stack.access_point,
    app_security_group=database_stack.app_security_group,
    alb_security_group=database_stack.alb_security_group,
    repo_root=REPO_ROOT,
)

app.synth()
