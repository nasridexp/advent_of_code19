class IntComputer:
    output_val = None
    def __init__(self, inst_list_or):
        #Create an array of 0 10 times longer that the actual list with the
        # actual list in the beggining
        self.inst_list = inst_list_or[:] + [0] * (9*len(inst_list_or))
        #variable to keep track of self.pointer
        self.pointer = 0
        #relative base
        self.rel_base = 0

    def run_programme(self):
        # obtain values and run instructiondepending on code
        while self.inst_list[self.pointer] != 99:
            # Obtain the specific instruction and the modes (starting with the first parameter onwards)
            inst, modes = self.divide_inst_and_modes(self.inst_list[self.pointer])
            # Sum two numbers, store in third
            if inst == "01":
                #paddig modes with necessary 0
                modes = "{:<03s}".format(modes)

                pos_1, pos_2, final_pos = self.inst_list[self.pointer+1:self.pointer+4]
                val_to_save = self.apply_mode(pos_1, modes[0]) + self.apply_mode(pos_2, modes[1])
                self.save_val(final_pos, modes[2], val_to_save)

                self.pointer += 4

            # mutiply two numbers, store in third
            elif inst == "02":
                #paddig modes with necessary 0
                modes = "{:<03s}".format(modes)

                pos_1, pos_2, final_pos = self.inst_list[self.pointer+1:self.pointer+4]
                val_to_save = self.apply_mode(pos_1, modes[0]) * self.apply_mode(pos_2, modes[1])
                self.save_val(final_pos, modes[2], val_to_save)

                self.pointer += 4

            # insert input, save it to parameter place
            elif inst == "03":
                #paddig modes with necessary 0
                modes = modes = "{:<01s}".format(modes)

                final_pos = self.inst_list[self.pointer+1]
                user_input = int(input("Insert input: "))
                self.save_val(final_pos, modes[0], user_input)

                self.pointer += 2

            # output value in parameter place
            elif inst == "04":
                #paddig modes with necessary 0
                modes = modes = "{:<01s}".format(modes)

                pos_1 = self.inst_list[self.pointer+1]

                self.output_val = self.apply_mode(pos_1 , modes[0])
                print("Output value: {}, pointer: {}".format(self.output_val, self.pointer))
                self.pointer += 2

            # jump self.pointer to value from second parameter if first parameter != 0
            elif inst == "05":
                #paddig modes with necessary 0
                modes = "{:<02s}".format(modes)

                pos_1, pos_2, = self.inst_list[self.pointer+1:self.pointer+3]
                if self.apply_mode(pos_1, modes[0]) != 0:
                    self.pointer = self.apply_mode(pos_2 , modes[1])
                else:
                    self.pointer += 3

            # jump self.pointer to value from second parameter if first parameter == 0
            elif inst == "06":
                #paddig modes with necessary 0
                modes = "{:<02s}".format(modes)

                pos_1, pos_2, = self.inst_list[self.pointer+1:self.pointer+3]
                if self.apply_mode(pos_1, modes[0]) == 0:
                    self.pointer = self.apply_mode(pos_2 , modes[1])
                else:
                    self.pointer += 3

            # store 1 in third parameter if first parameter < second parameter, else store 0
            elif inst == "07":
                #paddig modes with necessary 0
                modes = "{:<03s}".format(modes)

                pos_1, pos_2, final_pos = self.inst_list[self.pointer+1:self.pointer+4]
                if self.apply_mode(pos_1, modes[0]) < self.apply_mode(pos_2, modes[1]):
                    self.save_val(final_pos, modes[2], 1)
                else:
                    self.save_val(final_pos, modes[2], 0)

                self.pointer += 4

            # store 1 in third parameter if first parameter == second parameter, else store 0
            elif inst == "08":
                #paddig modes with necessary 0
                modes = "{:<03s}".format(modes)

                pos_1, pos_2, final_pos = self.inst_list[self.pointer+1:self.pointer+4]
                if self.apply_mode(pos_1, modes[0]) == self.apply_mode(pos_2, modes[1]):
                    self.save_val(final_pos, modes[2], 1)
                else:
                    self.save_val(final_pos, modes[2], 0)

                self.pointer += 4

            #relative base offset
            elif inst == "09":
                #paddig modes with necessary 0
                modes = modes = "{:<01s}".format(modes)

                pos_1 = self.inst_list[self.pointer+1]

                #print("rel_base before {} - {}".format(self.rel_base, self.apply_mode(pos_1 , modes[0])))
                self.rel_base += self.apply_mode(pos_1 , modes[0])
                self.pointer += 2
            else:
                raise Exception("run: unknown instruction: {}".format(inst))

        return self.output_val

    def divide_inst_and_modes(self, instruction):
        full_inst = str(instruction)

        if len(full_inst) == 1:
            inst = "0" + full_inst
            modes = ""
        else:
            inst = full_inst[-2:]
            modes = full_inst[-3::-1]

        return inst, modes

    def apply_mode(self, pos, mode):
        #position mode
        if mode == "0":
            return self.inst_list[pos]
        #immediate mode
        elif mode == "1":
            return pos
        #relative mode
        elif mode == "2":
            return self.inst_list[self.rel_base + pos]
        else:
            raise Exception("run: unknown mode: {}".format(mode))

    def save_val(self, pos, mode, val):
        #position mode
        if mode == "0":
            self.inst_list[pos] = val
        elif mode == "2":
            self.inst_list[self.rel_base + pos] = val
        else:
            raise Exception("run: unknown mode: {}".format(mode))

if __name__ == "__main__":
    instructions = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]

    #read line
    file = open('data_9.txt', "r")
    line = (file.readlines()[0]).strip().split(",")
    #convert to int
    instruction_list = list(map(int, line))

    # create a computer and run instructions
    Computer = IntComputer(instruction_list)
    output = Computer.run_programme()

    # print(instruction_list[45:52])
