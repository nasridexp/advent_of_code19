import numpy as np 
import re
import itertools
import math

class moon:
	def __init__(self, pos):
		self.pos = pos
		self.vel = np.zeros(3, dtype=int)

	def get_pos(self):
		return self.pos

	def set_pos(self, pos):
		self.pos = pos

	def get_vel(self):
		return self.vel

	def set_vel(self, vel):
		self.vel = vel

	def print_state(self):
		print("pos = {} vel = {} Energy = {}"
			  .format(self.pos, self.vel, self.get_energy()))

	def apply_velocity(self):
		self.pos = self.pos + self.vel

	def get_energy(self):
		return sum(abs(self.pos))*sum(abs(self.vel))

def apply_gravity(moon_1, moon_2):
	pos_1 = moon_1.get_pos()
	pos_2 = moon_2.get_pos()

	vel_1 = moon_1.get_vel()
	vel_2 = moon_2.get_vel()

	for dim in range(len(pos_1)):
		if pos_1[dim] < pos_2[dim]:
			vel_1[dim] += 1
			vel_2[dim] += -1
		elif pos_1[dim] > pos_2[dim]:
			vel_1[dim] += -1
			vel_2[dim] += 1

	#new vels
	moon_1.set_vel(vel_1)
	moon_2.set_vel(vel_2)

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

if __name__ == "__main__":
#=================== PART 1 =================
	# #read file
 #    file = open('data_12.txt', "r")
 #    extract_re = re.compile("<x=(.*), y=(.*), z=(.*)>")
 #    moons_vec = []
 #    for line in file:
 #    	moon_data = line.strip("\n")
 #    	re_match = extract_re.match(moon_data)
 #    	vec = np.array([re_match[1],re_match[2],re_match[3]], dtype=int)
 #    	moons_vec.append(moon(vec))

 #    print("Step 0:")
 #    for moon in moons_vec:
 #    	moon.print_state()

 #    # apply steps
 #    num_steps = 2772
 #    for step in range(num_steps):

	#     # apply gravity
	#     possible_pairs = list(itertools.combinations(range(len(moons_vec)), 2))
	#     for pos_pair in possible_pairs:
	#     	apply_gravity(moons_vec[pos_pair[0]], moons_vec[pos_pair[1]])

	#     # apply velocity
	#     for moon in moons_vec:
 #    		moon.apply_velocity()

 #    print("Step {}:".format(num_steps))
 #    Total_energy = 0
 #    for moon in moons_vec:
 #    	moon.print_state()
 #    	Total_energy += moon.get_energy()
 #    print("Total Energy is: ", Total_energy)

 # =================== PART 2 =================
 # We are going to calculate the period in every dimension and then
 # claculate the lcm of those periods to find the solution
 	# read file
    file = open('data_12.txt', "r")
    extract_re = re.compile("<x=(.*), y=(.*), z=(.*)>")
    moons_vec = []
    for line in file:
    	moon_data = line.strip("\n")
    	re_match = extract_re.match(moon_data)
    	vec = np.array([re_match[1],re_match[2],re_match[3]], dtype=int)
    	moons_vec.append(moon(vec))

    print("Step 0:")
    for moon in moons_vec:
    	moon.print_state()

    # Registering initial state
    initial_x = []
    initial_y = []
    initial_z = [] 

    for moon in moons_vec:
    	aux_pos = moon.get_pos()
    	initial_x.append(aux_pos[0])
    	initial_y.append(aux_pos[1])
    	initial_z.append(aux_pos[2])

    	aux_vel = moon.get_vel()
    	initial_x.append(aux_vel[0])
    	initial_y.append(aux_vel[1])
    	initial_z.append(aux_vel[2])

    # Evolve orbit until the periods for each dimesions are found
    periods = []
    periods_found = [False, False, False]
    counter = 0
    while len(periods)<3:
    	counter += 1
    	# apply gravity
    	possible_pairs = list(itertools.combinations(range(len(moons_vec)), 2))
    	for pos_pair in possible_pairs:
    		apply_gravity(moons_vec[pos_pair[0]], moons_vec[pos_pair[1]])

    	# apply velocity
    	for moon in moons_vec:
    		moon.apply_velocity()

    	aux_x = []
    	aux_y = []
    	aux_z = []
    
    	for moon in moons_vec:
    		aux_pos = moon.get_pos()
    		aux_x.append(aux_pos[0])
    		aux_y.append(aux_pos[1])
    		aux_z.append(aux_pos[2])

    		aux_vel = moon.get_vel()
    		aux_x.append(aux_vel[0])
    		aux_y.append(aux_vel[1])
    		aux_z.append(aux_vel[2])

    	# dim X
    	if aux_x == initial_x and not periods_found[0]:
    		periods_found[0] = True
    		periods.append(counter)
    		print("X period found: ", periods[-1])

    	# dim Y
    	if aux_y == initial_y and not periods_found[1]:
    		periods_found[1] = True
    		periods.append(counter)
    		print("Y period found: ", periods[-1])

    	# dim Z
    	if aux_z == initial_z and not periods_found[2]:
    		periods_found[2] = True
    		periods.append(counter)
    		print("Z period found: ", periods[-1])    	


    print("The periods are: ", periods)
    print("The lcm of those periods is: ", (lcm(periods[2], lcm(periods[0], periods[1])) ))
