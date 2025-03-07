class Car:
    def __init__(self, model, year, color):
        self.model = model
        self.year = year
        self._color = color
        self.speed = 0

    @classmethod
    def print_gas_mileage(cls, distance_traveled, fuel_burned):
        print(distance_traveled/fuel_burned)

    def turn_on_engine(self):
        print('Engine is on')

    def turn_off_engine(self):
        print('Engine is off')

    def accelerate(self):
        self.speed += 5
        print('Accelerating')

    def brake(self):
        self.speed -= 3
        print('Braking')

    def current_speed(self):
        print(f'The {self.color} {self.year} {self.model} is ' +
              f'going {self.speed} mph.')
        
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, new_color):
        if(not isinstance(new_color, str)):
            raise TypeError('New color must be a string')
        self._color = new_color
        
porsche = Car('Porsche', 2023, 'black')
porsche.turn_on_engine()
porsche.accelerate()
porsche.accelerate()
porsche.current_speed()
porsche.brake()
porsche.current_speed()
print(porsche.color)
porsche.color = 'Silver'
print(porsche.color)
#porsche.color = 67
#print(porsche.color)

Car.print_gas_mileage(60,2)