import random
number = random.randint(-10, 10)
if number > 0:
    print("{0} is posative".format(number))
elif number == 0:
    print("{0} is zero".format(number))
else:
    print("{} is negative".format(number))