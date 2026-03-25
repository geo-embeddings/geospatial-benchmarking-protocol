from pathlib import Path

from aws_cdk import App, Environment, Tags

from gbp.infra.app_stack import AppStack
from gbp.infra.config import Config
from gbp.infra.database_stack import DatabaseStack

REPO_ROOT = Path(__file__).resolve().parents[5]

config = Config()
app = App()
env = Environment(region=config.aws_region)

for key, value in config.tags.items():
    Tags.of(app).add(key, value)

database_stack = DatabaseStack(app, config.stack_name("database"), env=env)

AppStack(
    app,
    config.stack_name("app"),
    env=env,
    vpc=database_stack.vpc,
    database=database_stack.database,
    app_security_group=database_stack.app_security_group,
    alb_security_group=database_stack.alb_security_group,
    repo_root=REPO_ROOT,
)

app.synth()
