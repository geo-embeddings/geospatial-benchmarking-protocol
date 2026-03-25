from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """GBP infrastructure settings."""

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="STACK_", extra="ignore"
    )

    name: str = "gbp"
    stage: str = "development"
    owner: str = "gadomski"
    project: str = "gbp"
    release: str = "dev"
    aws_region: str = "us-west-2"

    def stack_name(self, name: str) -> str:
        """Generate consistent stack name."""
        return f"{self.name}-{self.stage}-{name}"

    @property
    def tags(self) -> dict[str, str]:
        """Generate consistent tags for resources."""
        return {
            "Project": self.project,
            "Owner": self.owner,
            "Stage": self.stage,
            "Name": self.name,
            "Release": self.release,
        }
