from pathlib import Path

from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_rds as rds
from constructs import Construct


class AppStack(Stack):
    """Fargate service running the GBP backend API with PostgreSQL on RDS."""

    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        vpc: ec2.IVpc,
        database: rds.DatabaseInstance,
        app_security_group: ec2.ISecurityGroup,
        alb_security_group: ec2.ISecurityGroup,
        repo_root: Path,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        task_definition = ecs.FargateTaskDefinition(
            self,
            "TaskDef",
            cpu=256,
            memory_limit_mib=512,
        )

        db_secret = database.secret
        assert db_secret is not None

        task_definition.add_container(
            "App",
            image=ecs.ContainerImage.from_asset(
                str(repo_root),
                file="Dockerfile.backend",
            ),
            logging=ecs.LogDrivers.aws_logs(stream_prefix="gbp"),
            environment={
                "PYTHONUNBUFFERED": "1",
            },
            secrets={
                "DB_HOST": ecs.Secret.from_secrets_manager(db_secret, field="host"),
                "DB_PORT": ecs.Secret.from_secrets_manager(db_secret, field="port"),
                "DB_USERNAME": ecs.Secret.from_secrets_manager(
                    db_secret, field="username"
                ),
                "DB_PASSWORD": ecs.Secret.from_secrets_manager(
                    db_secret, field="password"
                ),
                "DB_NAME": ecs.Secret.from_secrets_manager(db_secret, field="dbname"),
            },
            port_mappings=[ecs.PortMapping(container_port=8000)],
        )

        alb = elbv2.ApplicationLoadBalancer(
            self,
            "Alb",
            vpc=vpc,
            internet_facing=True,
            security_group=alb_security_group,
        )

        service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "Service",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=1,
            load_balancer=alb,
            security_groups=[app_security_group],
            open_listener=False,
        )

        service.target_group.configure_health_check(path="/api/health")
