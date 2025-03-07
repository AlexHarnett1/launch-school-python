class SignalMixin:
    def signal_left(self):
        print('Signalling left')

    def signal_right(self):
        print('Singalling right')

    def signal_off(self):
        print('Singal is now off')

class Vehicle:
    vehicle_count = 0

    def __init__(self):
        Vehicle.vehicle_count += 1

    @classmethod
    def vehicles(cls):
        return Vehicle.vehicle_count

class Car(SignalMixin, Vehicle):
    pass

class Truck(SignalMixin, Vehicle):
    pass

class Boat(Vehicle):
    pass


print(Car.vehicles())     # 0
car1 = Car()
print(Car.vehicles())     # 1
car2 = Car()
car3 = Car()
car4 = Car()
print(Car.vehicles())     # 4
truck1 = Truck()
truck2 = Truck()
print(Truck.vehicles())   # 6
boat1 = Boat()
boat2 = Boat()
print(Boat.vehicles())    # 8

car1.signal_left()       # Signalling left
truck1.signal_right()    # Signalling right
car1.signal_off()        # Signal is now off
truck1.signal_off()      # Signal is now off
# boat1.signal_left()
# AttributeError: 'Boat' object has no attribute
# 'signal_left'

print(Car.mro())