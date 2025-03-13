import dataclasses


@dataclasses.dataclass
class Config:
    SECRET_KEY: str
    JWT_SECRET: str
