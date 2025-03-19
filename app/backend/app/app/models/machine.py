from typing import TYPE_CHECKING

from app.db.base_class import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from .machine_process import MachineProcess  # noqa: F401


class Machine(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    host = Column(String, index=True)
    last_online_timestamp = Column(Integer, index=True)

    processes = relationship("MachineProcess", back_populates="machine")
