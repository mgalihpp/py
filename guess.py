import random

random_number = random.randint(1, 10)  # Generate a random number between 1 and 10
close_values = [random_number - 3, random_number - 2, random_number - 1, random_number + 1, random_number + 2, random_number + 3]

step = 0

while True:
    print('langkah : '+ str(step))
    playernumber = int(input("Guess Number: "))
    step+=1

    if playernumber == random_number:
        print('Kamu benar!')
        print('kamu berhasil menyelesaikan dengan : ' + str(step) + ' langkah')
        break
    elif playernumber in close_values:
        print('Coba lagi, kamu hampir benar.')
    else:
        print('Coba lagi.')

# The loop will continue until the player guesses the correct number or gets within 3 units of the random number.
