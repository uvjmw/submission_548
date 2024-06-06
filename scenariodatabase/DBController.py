import os
from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Query
from pathlib import Path
from scenariodatabase.Entities.Base import Base
from scenariodatabase.Entities.Entities import Scenario, Routing, Lane, Signal, RSUResult


class DBController():

    def __init__(self, file: Path):
        super().__init__()
        self.database_file = file
        self.session = None
        self.create_session()


    def delete_database(self):
        if self.database_file.exists():
            os.remove(self.database_file)

    def create_session(self):
        engine = create_engine(f"sqlite:///{self.database_file}", echo=False)
        Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()

    def get_session(self):
        return self.session

    def close_session(self):
        self.session.close()

    def insert_object(self, object):
        self.session.add(object)
        self.session.commit()

    def get_scenario_by_id(self, id):
        return self.session.query(Scenario).filter(Scenario.id == id).one()

    def get_all_scenarios(self):    #request all scenarios, handle with care
        return self.session.query(Scenario).all()

    def get_scenarios_by_type(self, type:str):
        return self.session.query(Scenario).filter(Scenario.type==type).all()

    def get_lanes(self):
        return self.session.query(Lane).all()

    def get_routing_by_id(self, routing_id:int):
        return self.session.query(Routing).filter(Routing.routing_id == routing_id).one_or_none()

    def get_routing_by_lanes(self, start_lane:int, end_lane:int):
        try:
            return self.session.query(Routing).filter(Routing.start_lane==start_lane, Routing.end_lane==end_lane).one_or_none()
        except:
            return None

    def get_routings(self):
        return self.session.query(Routing).all()

    def get_signal_by_id(self, signal_group_id:int):
        return self.session.query(Signal).filter(Signal.signal_id==signal_group_id).one()

    def get_scenarios_by_routing_id(self, routing_id:int):
        return self.session.query(Scenario).filter(Scenario.ego_routing==routing_id).all()

    def get_rsuresult_by_scenario_id(self, scenario_id:int):
        return self.session.query(RSUResult).filter(RSUResult.scenario_id==scenario_id).all()

    def get_rsuresults(self):
        return self.session.query(RSUResult).all()