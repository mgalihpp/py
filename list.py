drinks = ['soda', 'water', 'milk', 'coffee']
food = ['hamburger', 'pizza', 'fried rice', 'noodle']

serve = [drinks, food]

# print(serve[1][2]) # array start from 0 likes javascript


# set 

hello = {'world', 'people', 'friend'}
animal = {'anjing', 'babi', 'kucing'}

# hello.add('buddy')
# hello.remove('buddy')
# hello.clear()

# hello.update(animal)
aa = hello.union(animal)
aa = hello.difference(animal) # do not print if there has same value
aa = hello.intersection(animal) # do print if there has same value only

# for i in aa:
#     print(i)


capitals = {
    "Ibu kota": "Jakarta",
    "Provinsi": "Banten",
    "Kabupaten": "Tangerang",
    "Kecamatan": "Legok"
}

# print(capitals['Ibu kota'])
# print(capitals.get('Ibu kota'))
# print(capitals.keys())
# print(capitals.values())
# print(capitals.items())
capitals.update({"Code": "224443"})
capitals.pop('Code') #remove a key and the value 
capitals.clear()

for key, value in capitals.items():
    print(key, value)