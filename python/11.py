import numpy as np
import matplotlib.pyplot as plt
from time import sleep

class IntComputer:
    def __init__(self, inst_list_or):
        #Create an array of 0 10 times longer that the actual list with the
        # actual list in the beggining
        self.inst_list = inst_list_or[:] + [0] * (9*len(inst_list_or))
        #variable to keep track of self.pointer
        self.pointer = 0
        #relative base
        self.rel_base = 0

    def next_step(self, intcode_input):
        input_used = False
        output_val = []
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
                if not input_used:
                    #paddig modes with necessary 0
                    modes = modes = "{:<01s}".format(modes)

                    final_pos = self.inst_list[self.pointer+1]
                    user_input = intcode_input
                    self.save_val(final_pos, modes[0], user_input)

                    self.pointer += 2
                    input_used = True
                else: break

            # output value in parameter place
            elif inst == "04":
                #paddig modes with necessary 0
                modes = modes = "{:<01s}".format(modes)

                pos_1 = self.inst_list[self.pointer+1]

                output_val.append(self.apply_mode(pos_1 , modes[0]))
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

        return output_val

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


class painting_robot:
	def __init__(self, instructions, map_dim, position):
	    #starting orientation
	    self.orientation = 2

	    # starting robot brain
	    self.brain = IntComputer(instructions)

	    # initialising map
	    self.map = np.zeros([map_dim, map_dim], dtype=int)

	   	#starting position
	    self.position = position

	    # part 2: initial point is white
	    self.map[position] = 1

	    #list of position
	    self.list_positions = []

	def perform_one_step(self):
		panel_colour = self.check_camera()
		self.list_positions.append(self.position)
		output = self.brain.next_step(panel_colour)
		if output:
			new_panel_colour, turn = output
			self.paint_panel(new_panel_colour)
			self.advance(turn)
			return False
		else:
			return True

	def run_robot(self):
		finished = False

		while not finished:
			finished = self.perform_one_step()

		return self.map, self.list_positions

	def check_camera(self):
		return self.map[self.position]

	def paint_panel(self, new_panel_colour):
		self.map[self.position] = new_panel_colour

	# 0: down
	# 1: left
	# 2: up
	# 3: right
	def advance(self, turn):
		if turn:
			self.orientation = (self.orientation + 1) % 4
		else:
			self.orientation = (self.orientation - 1) % 4
		if self.orientation == 0:
			self.position = (self.position[0], self.position[1] - 1)
		elif self.orientation == 1:
			self.position = (self.position[0] - 1, self.position[1])
		elif self.orientation == 2:
			self.position = (self.position[0], self.position[1] + 1)
		elif self.orientation == 3:
			self.position = (self.position[0] + 1, self.position[1])

if __name__ == "__main__":
	#read line
    file = open('data_11.txt', "r")
    line = (file.readlines()[0]).strip().split(",")
    #convert to int
    instruction_list = list(map(int, line))

    # run the robot given the instructions and the dimension of the map to paint
    map_dim = 200
    PaintingRobot = painting_robot(instruction_list, map_dim, (map_dim // 2, map_dim // 2))
    output_map, list_positions = PaintingRobot.run_robot()

    print(len(set(list_positions)))

    plt.matshow(output_map)
    plt.show()