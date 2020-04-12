#implement intcode computer
from itertools import product

def int_computer(inst_list_original):
    #make copy
    inst_list = inst_list_original[:]
    #variable to keep track of pointer
    pointer = 0

    # obtain values and run instructiondepending on code
    while inst_list[pointer] != 99:
        inst = inst_list[pointer]
        if inst == 1:
            pos_1, pos_2, final_pos = inst_list[pointer+1:pointer+4]
            inst_list[final_pos] = inst_list[pos_1] + inst_list[pos_2]
            pointer += 4
        elif inst == 2:
            pos_1, pos_2, final_pos = inst_list[pointer+1:pointer+4]
            inst_list[final_pos] = inst_list[pos_1] * inst_list[pos_2]
            pointer += 4
        else:
            raise Exception("run: unknown instruction: {}".format(inst))

    return inst_list

if __name__ == "__main__":
    with open("data_2.txt","r") as data:
        instruction_list_string = data.read().split(",")
        # eliminate \n in last element
        instruction_list_string[-1] = instruction_list_string[-1].split("\n")[0]
        #convert to int
        instruction_list = map(int, instruction_list_string)

    #substitution
    instruction_list[1] = 12
    instruction_list[2] = 2

    computed_list = int_computer(instruction_list)
    if -1 not in computed_list:
        print("The computed list is: {}".format(computed_list))
    else:
        print("An error occurred. Instruction not recognised.")

    for noun, verb in product(range(100), range(100)):
        instruction_list[1] = noun
        instruction_list[2] = verb

        result = int_computer(instruction_list)
        if result[0] == 19690720:
            print("The solution is (noun, verb)=({},{})".format(noun, verb))
            break

