from typing import TYPE_CHECKING

from app.db.base_class import Base
from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from .machine import Machine  # noqa: F401


class MachineProcess(Base):
    machine_id = Column(Integer, ForeignKey("machine.id"), primary_key=True)
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, index=True)
    path = Column(String)
    hash = Column(String)
    is_hash_same = Column(Boolean, index=True)

    machine = relationship("Machine", back_populates="processes")
