r = range(0,25,3)
print(r[6])

print('Launch School'[4:10])

tup = tuple(range(1,6))
print(tup[-2:-5:-1])

pets = {
    'Cat':  'Meow',
    'Dog':  'Bark',
    'Bird': 'Tweet',
}
print(pets['Dog'])
print(pets['Lizard'] if 'Lizard' in pets else None)


info = 'xyz:*:42:42:Lee Kim:/home/xyz:/bin/zsh'
print(info.replace(':', '+'))
