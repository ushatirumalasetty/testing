import pytest
from truck import Truck
@pytest.fixture
def car():  # Our Fixture function
    from truck import Truck
    car_obj= Truck(color="Red", max_speed=30, acceleration=10, tyre_friction=3,max_cargo_weight=30)
    return car_obj

@pytest.fixture
def car2():  # Our Fixture function
    from truck import Truck
    car_obj= Truck(color="blue", max_speed=50, acceleration=20, tyre_friction=4,max_cargo_weight=40)
    return car_obj

@pytest.fixture
def car3():  # Our Fixture function
    from truck import Truck
    car_obj= Truck(color="blue", max_speed=30, acceleration=3, tyre_friction=3,max_cargo_weight=20)
    return car_obj


def test_car_constructor_when_single_object_is_given(car):

    #arrange

    color="Red"
    max_speed=30
    acceleration=10
    tyre_friction=3

    #assert

    assert car.max_speed==max_speed
    assert car.acceleration==acceleration
    assert car.tyre_friction==tyre_friction
    assert car.color==color

def test_car_constructor_when_multiple_objects_are_given(car,car2):

    #arrange

    color="Red"
    max_speed=30
    acceleration=10
    tyre_friction=3

    #assert

    assert car.max_speed==max_speed
    assert car.acceleration==acceleration
    assert car.tyre_friction==tyre_friction
    assert car.color==color

    #arrange

    color="blue"
    max_speed=50
    acceleration=20
    tyre_friction=4

    #assert

    assert car2.max_speed==max_speed
    assert car2.acceleration==acceleration
    assert car2.tyre_friction==tyre_friction
    assert car2.color==color


def test_max_speed_when_invalid_input_negitive_for_max_speed_is_given():
    with pytest.raises(Exception) as e  :
         assert Truck(color="Red", max_speed=-1, acceleration=10, tyre_friction=3,max_cargo_weight=10)
    assert str(e.value)=="Invalid value for max_speed"

def test_max_speed_when_invalid_input_zero_for_max_speed_is_given():
    with pytest.raises(Exception) as e  :
         assert Truck(color="Red", max_speed=0, acceleration=10, tyre_friction=3,max_cargo_weight=10)
    assert str(e.value)=="Invalid value for max_speed"

def test_max_speed_when_valid_for_max_speed_is_given():
    car=Truck(color="Red", max_speed=1, acceleration=1, tyre_friction=1,max_cargo_weight=10)
    assert car.color=="Red"
    assert car.max_speed==1
    assert car.acceleration==1
    assert car.tyre_friction==1

def test_acceleration_when_invalid_input_negitive_for_acceleration_is_given():
    with pytest.raises(Exception) as e:
         assert Truck(color="Red", max_speed=10, acceleration=-1, tyre_friction=3,max_cargo_weight=10)
    assert str(e.value)=="Invalid value for acceleration"

def test_acceleration_when_invalid_input_for_zero_acceleration_is_given():
    with pytest.raises(Exception) as e:
         assert Truck(color="Red", max_speed=10, acceleration=0, tyre_friction=3,max_cargo_weight=10)
    assert str(e.value)=="Invalid value for acceleration"

def test_tyre_friction_when_invalid_input_negitive_for_tyre_friction_is_given():
    with pytest.raises(Exception) as e:
         assert Truck(color="Red", max_speed=10, acceleration=10, tyre_friction=-1,max_cargo_weight=10)
    assert str(e.value)=="Invalid value for tyre_friction"

def test_tyre_friction_when_invalid_input_zero_for_tyre_friction_is_given():
    with pytest.raises(Exception) as e:
         assert Truck(color="Red", max_speed=10, acceleration=10, tyre_friction=0,max_cargo_weight=10)
    assert str(e.value)=="Invalid value for tyre_friction"

def test_start_engine(car):
    car.start_engine()
    is_engine_started=True
    assert car.is_engine_started==is_engine_started

def test_start_engine_when_engine_is_started_twice(car):
    car.start_engine()
    car.start_engine()
    is_engine_started=True
    assert car.is_engine_started==is_engine_started

def test_start_engine_when_multiple_objects_are_present(car,car2):
    car.start_engine()
    is_engine_started=False
    assert car2.is_engine_started==is_engine_started


def test_current_speed_before_engine_is_started(car):
    current_speed=0
    assert car.current_speed==current_speed


def test_current_speed_after_engine_is_started(car):
    car.start_engine()
    current_speed=0
    assert car.current_speed==current_speed

def test_accelerate_when_engine_is_not_started(car):
    car.accelerate()
    current_speed=0
    assert car.current_speed==current_speed

def test_accelerate_with_different_acceleration_when_engine_is_not_started(car):
    car.accelerate()
    car.accelerate()
    current_speed=0
    assert car.current_speed==current_speed

def test_accelerate(car):
    car.start_engine()
    car.accelerate()
    current_speed=10
    assert car.current_speed==current_speed

def test_accelerate_with_different_acceleration(car):
    car.start_engine()
    car.accelerate()
    car.accelerate()
    current_speed=20
    assert car.current_speed==current_speed


def test_accelerate_while_current_speed_exceed_max_Speed(car):
    car.start_engine()
    car.accelerate()
    car.accelerate()
    car.accelerate()
    car.accelerate()
    current_speed=30
    assert car.current_speed==current_speed

def test_accelerate_while_current_speed_equal_to_max_Speed(car):
    car.start_engine()
    car.accelerate()
    car.accelerate()
    car.accelerate()
    current_speed=30
    assert car.current_speed==current_speed

def test_accelerate_with_different_acceleration_more_than_max_limit(car):
    car.start_engine()
    car.accelerate()
    car.accelerate()
    car.accelerate()
    car.accelerate()
    current_speed=30
    assert car.current_speed==current_speed


def apply_brake_when_car_is_at_rest(car):
    car.apply_brakes()
    current_speed=0
    assert car.current_speed==current_speed

def apply_brake_when_car_is_at_motion(car):
    car.start_engine()
    car.accelerate()
    car.apply_brakes()
    car.apply_brakes()
    car.apply_brakes()
    current_speed=1
    assert car.current_speed==current_speed


def test_apply_brake_while_current_speed_falls_less_than_zero(car):
    car.start_engine()
    car.accelerate()
    car.apply_brakes()
    car.apply_brakes()
    car.apply_brakes()
    car.apply_brakes()
    car.apply_brakes()
    current_speed=0
    assert car.current_speed==current_speed

def test_apply_brake_while_current_speed_equal_to_zero(car3):
    car3.start_engine()
    car3.accelerate()
    car3.apply_brakes()
    current_speed=0
    assert car3.current_speed==current_speed

def test_sound_horn_when_car_is_at_rest(car,capfd):
    car.sound_horn()
    output=capfd.readouterr()
    assert output.out=="Start the engine to sound_horn\n"


def test_sound_horn_when_car_is_at_motion(car,capfd):
    car.start_engine()
    car.sound_horn()
    output=capfd.readouterr()
    assert output.out=="Honk Honk\n"


def test_stop_engine_when_engine_is_started(car):
    car.start_engine()
    car.stop_engine()
    is_engine_started=False
    assert car.is_engine_started==is_engine_started

def test_stop_engine_when_engine_is_already_stopped(car):
    car.stop_engine()
    is_engine_started=False
    assert car.is_engine_started==is_engine_started

def test_stop_engine_when_multiple_object_engines_are_started(car,car2):

    #arrange

    car2.start_engine( )
    car.start_engine()

    #act

    car.stop_engine()
    is_engine_started=True

    #assert

    assert car2.is_engine_started==is_engine_started

def test_stop_engine_when_engine_is_in_motion(car):

    #arrange

    car.start_engine()
    car.accelerate()

    #act

    car.stop_engine()
    is_engine_started=False

    #assert

    assert car.is_engine_started==is_engine_started


def test_encapsulation_for_max_speed(car):

    #act

    with pytest.raises(Exception) as e:
         car.max_speed=100

    #assert

    assert str(e.value)=="can't set attribute"


def test_encapsulation_for_acceleration(car):

    #act

    with pytest.raises(Exception) as e:
         car.acceleration=100

    #assert

    assert str(e.value)=="can't set attribute"


def test_encapsulation_for_tyre_friction(car):

    #act

    with pytest.raises(Exception) as e:
         car.tyre_friction=100

    #assert

    assert str(e.value)=="can't set attribute"


def test_encapsulation_for_color(car):

    #act

    with pytest.raises(Exception) as e:
         car.color="brown"

    #assert

    assert str(e.value)=="can't set attribute"

def test_encapsulation_for_is_engine_started(car):

    #arrange

    car.start_engine()

    #act

    with pytest.raises(Exception) as e:
         car.is_engine_started=False

    #assert

    assert str(e.value)=="can't set attribute"


def test_encapsulation_for_current_speed(car):

    #arrange

    car.start_engine()
    car.accelerate()

    #act

    with pytest.raises(Exception) as e:
         car.current_speed=0

    #assert

    assert str(e.value)=="can't set attribute"

@pytest.fixture
def truck():  # Our Fixture function
    from truck import Truck
    truck_obj= Truck(color="Red", max_speed=30, acceleration=10, tyre_friction=3,max_cargo_weight=30)
    return truck_obj


def test_loading_cargo_less_than_max_limit_when_truck_is_at_rest(truck):
    truck.load(1)
    cargo_weight=1
    assert truck.cargo_weight==cargo_weight


def test_loading_cargo_equal_to_zero_when_truck_is_at_rest(truck):
    with pytest.raises(Exception) as e:
        assert truck.load(0)
    assert str(e.value)=="Invalid value for cargo_weight"

def test_loading_cargo_more_than_max_limit_when_truck_is_at_rest(truck,capfd):
    truck.load(50)
    output=capfd.readouterr()
    assert output.out=="Cannot load cargo more than max limit: 30\n"


def test_loading_cargo_when_truck_is_at_motion(truck,capfd):
    truck.start_engine()
    truck.accelerate()
    truck.load(1)
    output=capfd.readouterr()
    assert output.out=="Cannot load cargo during motion\n"

def test_load_cargo_when_truck_is_started_and_at_rest(truck):
    truck.start_engine()
    truck.load(1)
    cargo_weight=1
    assert truck.cargo_weight==cargo_weight

def test_load_cargo_when_truck_is_stopped_and_current_speed_equal_to_zero(truck):
    truck.start_engine()
    truck.stop_engine()
    truck.load(1)
    cargo_weight=1
    assert truck.cargo_weight==cargo_weight

def test_load_cargo_when_truck_is_stopped_and_current_speed_not_equal_to_zero(truck,capfd):
    truck.start_engine()
    truck.accelerate()
    truck.stop_engine()
    truck.load(1)
    output=capfd.readouterr()
    assert output.out=="Cannot load cargo during motion\n"


def test_load_invalid_cargo_weight(truck):
    with pytest.raises(Exception) as e:
        assert truck.load(-1)
    assert str(e.value)=="Invalid value for cargo_weight"

def test_unload_invalid_cargo_weight(truck):
    with pytest.raises(Exception) as e:
        assert truck.unload(-1)
    assert str(e.value)=="Invalid value for cargo_weight"


def test_unloading_cargo_less_than_min_limit_zero_when_truck_is_at_rest(truck,capfd):
    truck.unload(1)
    output=capfd.readouterr()
    assert output.out=="Cannot unload cargo less than min limit: 0\n"


def test_unloading_cargo_more_than_min_limit_when_truck_is_at_rest(truck):
    truck.load(20)
    truck.unload(1)
    cargo_weight=19
    assert truck.cargo_weight==cargo_weight

def test_unloading_cargo_equal_to_zero_when_truck_is_at_rest(truck):
    with pytest.raises(Exception) as e:
        assert truck.unload(0)
    assert str(e.value)=="Invalid value for cargo_weight"


def test_unloading_cargo_when_truck_is_at_motion(truck,capfd):
    truck.load(10)
    truck.start_engine()
    truck.accelerate()
    truck.unload(1)
    output=capfd.readouterr()
    assert output.out=="Cannot unload cargo during motion\n"

def test_unload_cargo_when_truck_is_started_and_at_rest(truck):
    truck.start_engine()
    truck.load(10)
    truck.unload(1)
    cargo_weight=9
    assert truck.cargo_weight==cargo_weight

def test_unload_cargo_when_truck_is_stopped_and_current_speed_equal_to_zero(truck):
    truck.start_engine()
    truck.stop_engine()
    truck.load(10)
    truck.unload(1)
    cargo_weight=9
    assert truck.cargo_weight==cargo_weight

def test_unload_cargo_when_truck_is_stopped_and_current_speed_not_equal_to_zero(truck,capfd):
    truck.load(10)
    truck.start_engine()
    truck.accelerate()
    truck.stop_engine()
    truck.unload(1)
    output=capfd.readouterr()
    assert output.out=="Cannot unload cargo during motion\n"




def test_loading_cargo_equal_to_max_limit_when_truck_is_at_rest(truck):
    truck.load(30)
    cargo_weight=30
    assert truck.cargo_weight==cargo_weight
