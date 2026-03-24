from aws_cdk import RemovalPolicy, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_efs as efs
from constructs import Construct


class DatabaseStack(Stack):
    """EFS file system for persistent SQLite storage."""

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            "Vpc",
            max_azs=2,
            nat_gateways=1,
        )

        self.app_security_group = ec2.SecurityGroup(
            self,
            "AppSecurityGroup",
            vpc=self.vpc,
            description="Security group for GBP Fargate service",
        )

        self.alb_security_group = ec2.SecurityGroup(
            self,
            "AlbSecurityGroup",
            vpc=self.vpc,
            description="Security group for GBP load balancer",
            allow_all_outbound=True,
        )
        self.alb_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80))
        self.app_security_group.add_ingress_rule(
            self.alb_security_group, ec2.Port.tcp(8000)
        )

        self.file_system = efs.FileSystem(
            self,
            "FileSystem",
            vpc=self.vpc,
            removal_policy=RemovalPolicy.RETAIN,
            performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,
            throughput_mode=efs.ThroughputMode.BURSTING,
        )

        self.file_system.connections.allow_default_port_from(self.app_security_group)

        self.access_point = self.file_system.add_access_point(
            "AccessPoint",
            path="/data",
            create_acl=efs.Acl(owner_uid="1000", owner_gid="1000", permissions="755"),
            posix_user=efs.PosixUser(uid="1000", gid="1000"),
        )
