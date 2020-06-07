from car import *

class Truck(Car):
    HORN="Honk Honk"

    def __init__(self,color,max_speed, acceleration, tyre_friction, max_cargo_weight):
        super().__init__( max_speed, acceleration, tyre_friction,color)
        self.check_is_positive(max_cargo_weight,"max_cargo_weight")
        self._max_cargo_weight=max_cargo_weight
        self._cargo_weight=0

    @property
    def max_cargo_weight(self):
        return self._max_cargo_weight
    @property
    def cargo_weight(self):
        return self._cargo_weight


    def load(self,weight):
        if weight<=0:
            raise ValueError("Invalid value for cargo_weight")
        if not self._current_speed:
            if self._cargo_weight+weight>self._max_cargo_weight:
                print(f"Cannot load cargo more than max limit: {self._max_cargo_weight}")
            else:
                self._cargo_weight+=weight
        else:
            print("Cannot load cargo during motion")

    def unload(self,weight):
        if weight<=0:
            raise ValueError("Invalid value for cargo_weight")
        if not self._current_speed:
            if self._cargo_weight<weight:
                print("Cannot unload cargo less than min limit: 0")
            else:
                self._cargo_weight-=weight
        else:
            print("Cannot unload cargo during motion")
    



