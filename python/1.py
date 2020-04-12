# Calculate necessary fuel

def calculate_fuel(mass):
    necessary_fuel = (mass // 3) - 2
    if necessary_fuel > 6:
        return necessary_fuel + calculate_fuel(necessary_fuel)
    else:
        return necessary_fuel

if __name__ == "__main__":
    modules = open("modules_1.txt","r")

    part_one = sum(calculate_fuel(int(module)) for module in modules)

    print("the necessary fuel is: {}".format(part_one))
