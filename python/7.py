from itertools import permutations

class IntComputer:
	output_val = None
	def __init__(self, inst_list_or):
	    #make copy
	    self.inst_list = inst_list_or[:]
	    #variable to keep track of self.pointer
	    self.pointer = 0

	def run_programme(self, input_list):
	    #input counter
	    input_count = 0
        # obtain values and run instructiondepending on code
	    while self.inst_list[self.pointer] != 99:

	    	# Obtain the specific instruction and the modes (starting with the first parameter onwards)
	    	inst, modes = self.divide_inst_and_modes(self.inst_list[self.pointer])

	    	# todo: apply factory pattern
	    	# Sum two numbers, store in third
	    	if inst == "01":
	            #paddig modes with necessary 0
	            modes = "{:<02s}".format(modes)

	            pos_1, pos_2, final_pos = self.inst_list[self.pointer+1:self.pointer+4]
	            self.inst_list[final_pos] = self.apply_mode(pos_1, modes[0]) + self.apply_mode(pos_2, modes[1])

	            self.pointer += 4

	        # mutiply two numbers, store in third
	    	elif inst == "02":
	            #paddig modes with necessary 0
	            modes = "{:<02s}".format(modes)

	            pos_1, pos_2, final_pos = self.inst_list[self.pointer+1:self.pointer+4]
	            self.inst_list[final_pos] = self.apply_mode(pos_1, modes[0]) * self.apply_mode(pos_2, modes[1])

	            self.pointer += 4

	        # insert input, save it to parameter place
	    	elif inst == "03":
	            final_pos = self.inst_list[self.pointer+1]
	            self.inst_list[final_pos] = input_list[input_count]
	            input_count += 1
	            self.pointer += 2

	        # output value in parameter place
	    	elif inst == "04":
	            #paddig modes with necessary 0
	            modes = modes = "{:<01s}".format(modes)

	            pos_1 = self.inst_list[self.pointer+1]

	            self.output_val = self.apply_mode(pos_1 , modes[0])
	            print("Output value: {}".format(self.output_val))
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
	            modes = "{:<02s}".format(modes)

	            pos_1, pos_2, final_pos = self.inst_list[self.pointer+1:self.pointer+4]
	            if self.apply_mode(pos_1, modes[0]) < self.apply_mode(pos_2, modes[1]):
	                self.inst_list[final_pos] = 1
	            else:
	                self.inst_list[final_pos] = 0

	            self.pointer += 4

	        # store 1 in third parameter if first parameter == second parameter, else store 0
	    	elif inst == "08":
	            #paddig modes with necessary 0
	            modes = "{:<02s}".format(modes)

	            pos_1, pos_2, final_pos = self.inst_list[self.pointer+1:self.pointer+4]
	            if self.apply_mode(pos_1, modes[0]) == self.apply_mode(pos_2, modes[1]):
	                self.inst_list[final_pos] = 1
	            else:
	                self.inst_list[final_pos] = 0

	            self.pointer += 4
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
		if mode == "0":
		    return self.inst_list[pos]
		elif mode == "1":
		    return pos
		else:
		    raise Exception("run: unknown mode: {}".format(mode))

if __name__ == "__main__":
    with open("data_7.txt","r") as data:
        instruction_list_string = data.read().split(",")
        # eliminate \n in last element
        instruction_list_string[-1] = instruction_list_string[-1].split("\n")[0]
        #convert to int
        instruction_list = list(map(int, instruction_list_string))

        # phase setting sequence
        phase_seq = [0,1,2,3,4]

        # find permutations
        pers = list(permutations(phase_seq, 5))

        max_thrust = 0
        for per in pers:
        	thruster = IntComputer(instruction_list)
        	output = thruster.run_programme([per[0], 0])
	        for phase in per[1:]:
	            thruster = IntComputer(instruction_list)
	            print("phase: {} output: {}".format(phase, output))
	            output = thruster.run_programme([phase, output])
	            print("output is {}".format(output))
	        if output > max_thrust: max_thrust = output
        print("Max_thrust is: {}".format(max_thrust))


