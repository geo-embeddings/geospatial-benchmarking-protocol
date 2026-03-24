from pathlib import Path

from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_efs as efs
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from constructs import Construct


class AppStack(Stack):
    """Fargate service running the GBP backend API with SQLite on EFS."""

    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        vpc: ec2.IVpc,
        file_system: efs.IFileSystem,
        access_point: efs.IAccessPoint,
        app_security_group: ec2.ISecurityGroup,
        alb_security_group: ec2.ISecurityGroup,
        repo_root: Path,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        volume_name = "gbp-data"

        task_definition = ecs.FargateTaskDefinition(
            self,
            "TaskDef",
            cpu=256,
            memory_limit_mib=512,
        )

        task_definition.add_volume(
            name=volume_name,
            efs_volume_configuration=ecs.EfsVolumeConfiguration(
                file_system_id=file_system.file_system_id,
                transit_encryption="ENABLED",
                authorization_config=ecs.AuthorizationConfig(
                    access_point_id=access_point.access_point_id,
                    iam="ENABLED",
                ),
            ),
        )

        container = task_definition.add_container(
            "App",
            image=ecs.ContainerImage.from_asset(
                str(repo_root),
                file="Dockerfile.backend",
            ),
            logging=ecs.LogDrivers.aws_logs(stream_prefix="gbp"),
            environment={
                "PYTHONUNBUFFERED": "1",
                "DATABASE_URL": "sqlite:///data/gbp.db",
            },
            port_mappings=[ecs.PortMapping(container_port=8000)],
        )

        container.add_mount_points(
            ecs.MountPoint(
                container_path="/app/data",
                source_volume=volume_name,
                read_only=False,
            )
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

        file_system.grant_read_write(task_definition.task_role)

        service.target_group.configure_health_check(path="/api/health")
