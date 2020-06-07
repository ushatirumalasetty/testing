from car import *
class RaceCar(Car):
    HORN="Peep Peep\nBeep Beep"
    def __init__(self,color, max_speed, acceleration, tyre_friction):
        super().__init__( max_speed, acceleration, tyre_friction,color)
        self._nitro=0

    @property
    def nitro(self):
        return self._nitro


    def apply_brakes(self):
        if self._current_speed>int((self._max_speed*0.5)):
            self._nitro+=10
            super().apply_brakes()
        else:
            super().apply_brakes()

    def accelerate(self):
        if self._nitro:
            if self._is_engine_started:
                     self._current_speed+=(math.ceil(1.3*self._acceleration))
                     self._nitro-=10
                     if self._current_speed>=self._max_speed:
                         self._current_speed=self._max_speed

            else:
               print("Start the engine to accelerate")
        else:
            super().accelerate()



