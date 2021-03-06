""" Module for interactive entity models. """

from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from data.enums import StructureType

from models import Base

from data import UnitType, Action


class Unit(Base):
    """ Model for tracking automated units. """

    __tablename__ = "Unit"
    id = Column(Integer, primary_key=True)

    type = Column(Enum(UnitType), nullable=False)

    ship_id = Column(Integer, ForeignKey("Ship.id"), nullable=False, index=True)
    ship = relationship("Ship")

    routine_start_id = Column(
        Integer, ForeignKey("Routine.id"), nullable=False, index=True
    )
    routine_start = relationship(
        "Routine",
        cascade="all, delete-orphan",
        foreign_keys=[routine_start_id],
        single_parent=True,
        uselist=False,
    )

    routine_current_id = Column(
        Integer, ForeignKey("Routine.id"), nullable=False, index=True
    )
    current_step = relationship(
        "Routine", foreign_keys=[routine_current_id], single_parent=True, uselist=False
    )

    def __str__(self) -> str:
        return f"{self.type} at {self.location}"

    def __repr__(self) -> str:
        return (
            "Unit("
            f"id={self.id}, "
            f"type={self.type}, "
            f"location_id={self.location_id}, "
            f"ship_id={self.ship_id}, "
            f"routine_start_id={self.routine_start_id}, "
            f"routine_current_id={self.routine_current_id})"
        )


class Routine(Base):
    """ Model for tracking unit routines. """

    __tablename__ = "Routine"
    id = Column(Integer, primary_key=True)

    action = Column(Enum(Action), nullable=False)

    unit_id = Column(Integer, ForeignKey("Unit.id"), nullable=False, index=True)
    unit = relationship("Unit", foreign_keys=[unit_id])

    location_id = Column(Integer, ForeignKey("Location.id"), nullable=False, index=True)
    location = relationship("Location")

    next_id = Column(Integer, ForeignKey("Routine.id"), index=True, unique=True)
    next = relationship(
        "Routine",
        uselist=False,
    )

    def __str__(self) -> str:
        return f"{self.action} at {self.location} for {self.unit}"

    def __repr__(self) -> str:
        return (
            "Routine("
            f"id={self.id}, "
            f"action={self.action}, "
            f"unit_id={self.unit_id}, "
            f"location_id={self.location_id}, "
            f"next_id={self.next_id}"
        )


class Structure(Base):
    """ Model for structures in the game world. """

    __tablename__ = "Structure"
    id = Column(Integer, primary_key=True)

    type = Column(Enum(StructureType), nullable=False)
    level = Column(Integer, default=1, nullable=False)

    location_id = Column(Integer, ForeignKey("Location.id"), nullable=False, index=True)
    location = relationship("Location")

    owner_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    owner = relationship("User")

    def __str__(self) -> str:
        return (
            f"Level {self.level} {self.type} at {self.location} owned by {self.owner}"
        )

    def __repr__(self) -> str:
        return (
            "Structure("
            f"id={self.id}, "
            f"type={self.type}, "
            f"level={self.level}, "
            f"location_id={self.location_id}, "
            f"owner_id={self.owner_id})"
        )
