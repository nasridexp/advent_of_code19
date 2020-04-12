# Calculate necessary fuel
from math import trunc

def calculate_fuel(mass):
    necessary_fuel = trunc(mass/3)-2
    if necessary_fuel > 6:
        final_necessary_fuel = calculate_fuel(necessary_fuel)
        return necessary_fuel + final_necessary_fuel
    else:
        return necessary_fuel

if __name__ == "__main__":
    f = open("modules_1.txt","r")

    Sum = 0
    for module in f:
        Sum = Sum + calculate_fuel(int(module))

    print("the necessary fuel is: {}".format(Sum))
