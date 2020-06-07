import math

class Car:
    HORN="Beep Beep"
    def __init__(self, max_speed, acceleration, tyre_friction,color=None):
        self.check_is_positive(max_speed,"max_speed")
        self.check_is_positive(acceleration,"acceleration")
        self.check_is_positive(tyre_friction,"tyre_friction")
        self._max_speed=max_speed
        self._acceleration=acceleration
        self._tyre_friction=tyre_friction
        self._color=color
        self._is_engine_started=False
        self._current_speed=0

    @property
    def max_speed(self):
        return self._max_speed
    @property
    def acceleration(self):
        return self._acceleration
    @property
    def tyre_friction(self):
        return self._tyre_friction
    @property
    def color(self):
        return self._color
    @property
    def is_engine_started(self):
        return self._is_engine_started
    @property
    def current_speed(self):
        return self._current_speed


    @ staticmethod
    def check_is_positive(check_item,check_item_name):
        if check_item<=0:
            raise ValueError(f"Invalid value for {check_item_name}")

    def start_engine(self):
        self._is_engine_started=True

    def accelerate(self):
        if self._is_engine_started:
            self._current_speed+=self._acceleration
            if self._current_speed>=self._max_speed:
                self._current_speed=self._max_speed
        else:
            print("Start the engine to accelerate")

    def apply_brakes(self):
        self._current_speed-=self._tyre_friction
        if self._current_speed<=0:
            self._current_speed=0

    def sound_horn(self):
        if self._is_engine_started:
            print(self.HORN)
        else:
            print("Start the engine to sound_horn")

    def stop_engine(self):
            self._is_engine_started=False

