from typing import Optional

from pydantic import BaseModel


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

    class Config:
        orm_mode = True


# Properties to return to client
class Machine(MachineInDBBase):
    pass


# Properties properties stored in DB
class MachineInDB(MachineInDBBase):
    pass
