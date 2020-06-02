from typing import List, Optional

from pydantic import BaseModel, Field


# Shared properties
class MachineBase(BaseModel):
    name: Optional[str] = None
    host: Optional[str] = None


# Properties to receive on item creation
class MachineCreate(MachineBase):
    host: str


# Properties to receive on item update
class MachineUpdate(MachineBase):
    pass


# Properties shared by models stored in DB
class MachineInDBBase(MachineBase):
    id: int
    name: str
    host: str
    last_online_timestamp: Optional[int]

    class Config:
        orm_mode = True


# Properties to return to client
class Machine(MachineInDBBase):
    pass


class MachineWithOnlineStatus(MachineInDBBase):
    was_recently_online: bool


# Properties stored in DB
class MachineInDB(MachineInDBBase):
    pass


class MachineActiveProcess(BaseModel):
    name: str = Field(alias="Name")
    id: int = Field(alias="Id")
    path: str = Field(alias="Path")
    hash: str = Field(alias="Hash")


class MachineInterface(BaseModel):
    interface_description: str = Field(alias="InterfaceDescription")
    ipv4_address: str = Field(alias="IPv4Address")
    ipv4_default_gateway: str = Field(alias="IPv4DefaultGateway")
    dns_server: str = Field(alias="DNSServer")
