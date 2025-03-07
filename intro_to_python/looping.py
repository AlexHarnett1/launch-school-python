my_list = [
    [1, 3, 6, 11],
    [4, 2, 4],
    [9, 17, 16, 0],
]

for arr in my_list:
    for number in arr:
        if number % 2 == 0:
            print(number)

my_set = {
    'Fluffy',
    'Butterscotch',
    'Pudding',
    'Cheddar',
    'Cocoa',
}

print({name: len(name)
       for name in my_set
       if len(name) % 2 == 1})

def factorial(num):
    result = 1
    while num > 0:
        result *= num
        num -= 1
    return result

print(factorial(1))   # 1
print(factorial(2))   # 2
print(factorial(3))   # 6
print(factorial(4))   # 24
print(factorial(5))   # 120
print(factorial(6))   # 720
print(factorial(7))   # 5040
print(factorial(8))   # 40320
print(factorial(25))  # 15511210043330985984000000