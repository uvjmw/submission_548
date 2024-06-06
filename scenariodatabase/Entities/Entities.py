from typing import List

from sqlalchemy import Column, Integer, ForeignKey, String, Float, Table, Boolean, JSON, BigInteger
from sqlalchemy import event
from sqlalchemy.orm import declarative_base, object_session, relationship, Mapped, mapped_column
from scenariodatabase.Entities.Base import Base


class Scenario(Base):
    __tablename__ = "scenarios"
    # Attributes
    scenario_id = Column(Integer, primary_key=True)
    track_id = Column(Float, nullable=True)
    ego_routing = Column(Integer, ForeignKey('routings.routing_id'))
    start_time = Column(Float, nullable=True)
    end_time = Column(Float, nullable=True)
    file = Column(String, nullable=True)
    signal_file = Column(String, nullable=True)
    type = Column(String, nullable=True)
    # cluster_id = Column(Integer, ForeignKey('clusters.cluster_id'))
    # relationships:
    routing = relationship('Routing', back_populates="scenario")
    # cluster = relationship('Cluster', back_populates="scenario")

class Routing(Base):
    __tablename__ = "routings"
    routing_id = Column(Integer, primary_key=True)
    start_lane = Column(Integer, ForeignKey('lanes.lane_id'))
    end_lane = Column(Integer, ForeignKey('lanes.lane_id'))
    rel_signal = Column(Integer, ForeignKey("signals.signal_id"))
    # relationships:
    scenario = relationship('Scenario', back_populates="routing")
    lane_1 = relationship('Lane', foreign_keys=[start_lane])
    lane_2 = relationship('Lane', foreign_keys=[end_lane])
    #signal_to_routing = relationship('SignalToRouting', back_populates='routing')
    signal = relationship('Signal', back_populates='routing')

class Lane(Base):
    __tablename__ = "lanes"
    lane_id = Column(Integer, primary_key=True)
    x_min = Column(Float, nullable=True)
    x_max = Column(Float, nullable=True)
    y_min = Column(Float, nullable=True)
    y_max = Column(Float, nullable=True)
    # relationships:
    # signal = relationship('Signal', back_populates='lane')
    # routing: Mapped[List["Routing"]] = relationship(back_populates="lane")
    # routing = relationship('Routing', back_populates='lane')
    #signal_to_routing = relationship('SignalToRouting', back_populates='lane')

class Signal(Base):
    __tablename__ = "signals"
    signal_id = Column(Integer, primary_key=True)
    signal_position_x = Column(Float, nullable=True)
    signal_position_y = Column(Float, nullable=True)
    # relationships:
    # lane = relationship('Lane', back_populates="signal")
    routing = relationship('Routing', back_populates="signal")


class RSUResult(Base):
    __tablename__ = "rsuresults"
    id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer, ForeignKey('scenarios.scenario_id'))
    vru_present_ground_truth = Column(Boolean, nullable=True)
    vru_present = Column(Boolean, nullable=True)
    vru_located = Column(Boolean, nullable=True)
    transmission_successful = Column(Boolean, nullable=True)
    detection_radius = Column(Float, nullable=True)
    signal_state = Column(String, nullable=True)

