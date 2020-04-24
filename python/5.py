def int_computer(inst_list_original):
    #make copy
    inst_list = inst_list_original[:]
    #variable to keep track of pointer
    pointer = 0

    # obtain values and run instructiondepending on code
    while inst_list[pointer] != 99:

        full_inst = str(inst_list[pointer])
        if len(full_inst) == 1:
            inst = "0" + full_inst
            modes = ""
        else:
            inst = full_inst[-2:]
            modes = full_inst[-3::-1]

        # Sum two numbers, store in third
        if inst == "01":
            #paddig modes with necessary 0
            modes = "{:<02s}".format(modes)

            pos_1, pos_2, final_pos = inst_list[pointer+1:pointer+4]
            inst_list[final_pos] = apply_mode(inst_list, pos_1, modes[0]) + apply_mode(inst_list, pos_2, modes[1])

            pointer += 4

        # mutiply two numbers, store in third
        elif inst == "02":
            #paddig modes with necessary 0
            modes = "{:<02s}".format(modes)

            pos_1, pos_2, final_pos = inst_list[pointer+1:pointer+4]
            inst_list[final_pos] = apply_mode(inst_list, pos_1, modes[0]) * apply_mode(inst_list, pos_2, modes[1])

            pointer += 4

        # insert input, save it to parameter place
        elif inst == "03":
            user_input = int(input("Insert input: "))
            final_pos = inst_list[pointer+1]
            inst_list[final_pos] = user_input
            pointer += 2

        # output value in parameter place
        elif inst == "04":
            #paddig modes with necessary 0
            modes = modes = "{:<01s}".format(modes)

            pos_1 = inst_list[pointer+1]
            print("Output value: {}".format(apply_mode(inst_list, pos_1 , modes[0])))
            pointer += 2

        # jump pointer to value from second parameter if first parameter != 0
        elif inst == "05":
            #paddig modes with necessary 0
            modes = "{:<02s}".format(modes)

            pos_1, pos_2, = inst_list[pointer+1:pointer+3]
            if apply_mode(inst_list, pos_1, modes[0]) != 0:
                pointer = apply_mode(inst_list, pos_2 , modes[1])
            else:
                pointer += 3

        # jump pointer to value from second parameter if first parameter == 0
        elif inst == "06":
            #paddig modes with necessary 0
            modes = "{:<02s}".format(modes)

            pos_1, pos_2, = inst_list[pointer+1:pointer+3]
            if apply_mode(inst_list, pos_1, modes[0]) == 0:
                pointer = apply_mode(inst_list, pos_2 , modes[1])
            else:
                pointer += 3

        # store 1 in third parameter if first parameter < second parameter, else store 0
        elif inst == "07":
            #paddig modes with necessary 0
            modes = "{:<02s}".format(modes)

            pos_1, pos_2, final_pos = inst_list[pointer+1:pointer+4]
            if apply_mode(inst_list, pos_1, modes[0]) < apply_mode(inst_list, pos_2, modes[1]):
                inst_list[final_pos] = 1
            else:
                inst_list[final_pos] = 0

            pointer += 4

        # store 1 in third parameter if first parameter == second parameter, else store 0
        elif inst == "08":
            #paddig modes with necessary 0
            modes = "{:<02s}".format(modes)

            pos_1, pos_2, final_pos = inst_list[pointer+1:pointer+4]
            if apply_mode(inst_list, pos_1, modes[0]) == apply_mode(inst_list, pos_2, modes[1]):
                inst_list[final_pos] = 1
            else:
                inst_list[final_pos] = 0

            pointer += 4
        else:
            raise Exception("run: unknown instruction: {}".format(inst))

    return inst_list

def apply_mode(inst_list, pos, mode):
    if mode == "0":
        return inst_list[pos]
    elif mode == "1":
        return pos
    else:
        raise Exception("run: unknown mode: {}".format(mode))

if __name__ == "__main__":
    with open("data_5.txt","r") as data:
        instruction_list_string = data.read().split(",")
        # eliminate \n in last element
        instruction_list_string[-1] = instruction_list_string[-1].split("\n")[0]
        #convert to int
        instruction_list = map(int, instruction_list_string)

        # print(instruction_list)
        computed_list = int_computer(instruction_list)
