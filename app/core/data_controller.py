from typing import List
from pydantic import BaseModel

class UpdatableModel(BaseModel):
    """Abstract model for updating db objects"""
    def updatable_attributes(self) -> List[str]:
        pass


class ControlCombiner:
    def set_combiner(self):
        for ctrl in vars(self):
            setattr(getattr(self, ctrl), "combiner", self)
