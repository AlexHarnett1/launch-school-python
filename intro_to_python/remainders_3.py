def remainders_3(numbers):
    return [number % 3 for number in numbers]

numbers_1 = [0, 1, 2, 3, 4, 5, 6]
numbers_2 = [1, 2, 4, 5]
numbers_3 = [0, 3, 6]
numbers_4 = []

print(any(number == 0 for number in remainders_3(numbers_1)))
print(any(number == 0 for number in remainders_3(numbers_2)))
print(any(number == 0 for number in remainders_3(numbers_3)))
print(any(number == 0 for number in remainders_3(numbers_4)))
