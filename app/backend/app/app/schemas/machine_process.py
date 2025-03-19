from typing import Optional

from pydantic import BaseModel, Field


# Shared properties
class MachineProcessBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    path: Optional[str] = None
    hash: Optional[str] = None
    is_hash_same: Optional[bool] = None


# Properties to receive on item creation
class MachineProcessCreate(MachineProcessBase):
    path: str
    hash: str
    is_hash_same: bool = True


# Properties to receive on item update
class MachineProcessUpdate(MachineProcessBase):
    pass


class MachineProcessFromClient(BaseModel):
    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    path: str = Field(alias="Path")
    hash: str = Field(alias="Hash")


# Properties shared by models stored in DB
class MachineProcessInDBBase(MachineProcessBase):
    id: int
    machine_id: int
    path: str
    hash: str
    is_hash_same: bool

    class Config:
        orm_mode = True


# Properties to return to client
class MachineProcess(MachineProcessInDBBase):
    pass


# Properties stored in DB
class MachineProcessInDB(MachineProcessInDBBase):
    pass
