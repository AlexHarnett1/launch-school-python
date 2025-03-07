class Car:
    def __init__(self, id, year, color):
        self.id = id
        self.year = year
        self.color = color

    def __str__(self):
        return f'{self.color} {self.year} {self.id}'

    def __repr__(self):
        color = repr(self.color)
        year = repr(self.year)
        id = repr(self.id)
        return f'Car({id}, {year}, {color})'

vwbuzz = Car('ID.Buzz', 2024, 'red')
print(vwbuzz)        # Red 2024 ID.Buzz
print(repr(vwbuzz))  # Car('ID.Buzz', 2024, 'red')