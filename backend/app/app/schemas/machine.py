from typing import Optional

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
    last_online_timestamp: Optional[int] = None

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


class NewAdapter(BaseModel):
    new_adapter: str = Field(alias="NewAdapter")
