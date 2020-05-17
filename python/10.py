from collections import defaultdict
from math import gcd
import numpy as np

# Finds the first asteorid between two points in space given the list of asteroids
def find_first_asteroid(centre, second_point, asteroids_list):
	X_pos, Y_pos = centre
	X_pos_prime, Y_pos_prime = second_point

	dist_vec = np.array([X_pos_prime - X_pos, Y_pos_prime - Y_pos])
		
	first_asteroid = None
	if abs(dist_vec[0]) > 1 or abs(dist_vec[1]) > 1:
		# find greatest common divisor of that vector components
		GCD = gcd(abs(dist_vec[0]), abs(dist_vec[1]))

		# build minimun vector
		min_vec = np.array([x / GCD for x in dist_vec])

		length_times = 1
		while np.linalg.norm(min_vec*length_times) <= np.linalg.norm(dist_vec):
			vec = min_vec*length_times

			if vec[0] == int(vec[0]) or vec[1] == int(vec[1]):
				check_point  = [int(X_pos + vec[0]), int(Y_pos + vec[1])]
				if check_point in asteroids_list:
					first_asteroid = check_point
					break

			length_times += 1
	elif dist_vec[0] == 0 and dist_vec[1] == 0:
		first_asteroid = centre
	# if it is at one unit of distance it's bound to be seen
	else:
		first_asteroid = second_point

	return first_asteroid

# Create list with asteroids positions

f = open("data_10.txt","r")

y = 0
asteroids_list = []
count = 1
X_loc = None
for line in f:
    line = line.strip() # get rid of \n
    [asteroids_list.append([pos,y]) for pos, char in enumerate(line) if char == "#"]

    # part 2 related quantities
    max_x = len(line)
    if "X" in line:
    	X_loc = [line.index("X"), y]

    count = 1
    y += 1
max_y = y

# for each asteroid find how many other asteroids it can see
number_of_visible_ast = []

for asteroid in asteroids_list:
	visible = 0
	for direction in asteroids_list:
		if direction != asteroid:
			first_asteroid = find_first_asteroid(asteroid, direction, asteroids_list)
			if first_asteroid == direction:
				visible += 1

	number_of_visible_ast.append(visible)


print("The max is: {} from list {}".format(max(number_of_visible_ast), number_of_visible_ast))		

# Part 2
def rotating_laser(X_loc, max_x, max_y, asteroids_list_original):
	asteroids_list = asteroids_list_original.copy()

	destroyed_asteroids_list = []
	while True:
		destroyed_asteroids = one_destruction_rotation(X_loc, max_x, max_y, asteroids_list)
		destroyed_asteroids_list + destroyed_asteroids
		if not destroyed_asteroids: break

def one_destruction_rotation(X_loc, max_x, max_y, asteroids_list):
	print(X_loc, max_x, max_y, asteroids_list)
	destroyed_asteroids = []
	# up-right wave of destruction
	for x in range(X_loc[0], max_x):
		destroyed_asteroid = find_first_asteroid(X_loc, [x, 0], asteroids_list)
		if find_first_asteroid:
			destroyed_asteroids.append(destroyed_asteroid)
			print("destroyed: {}".format(destroyed_asteroid))
			asteroids_list.remove(destroyed_asteroid)

	# down wave of destruction
	for y in range(0, max_y):
		destroyed_asteroid = find_first_asteroid(X_loc, [max_x-1, y], asteroids_list)
		if find_first_asteroid:
			destroyed_asteroids.append(destroyed_asteroid)
			asteroids_list.remove(destroyed_asteroid)

	# left wave of destruction
	for x in range(max_x - 1, -1, -1):
		destroyed_asteroid = find_first_asteroid(X_loc, [x, max_y-1], asteroids_list)
		if find_first_asteroid:
			destroyed_asteroids.append(destroyed_asteroid)
			asteroids_list.remove(destroyed_asteroid)

	# up wave of destruction
	for y in range(max_y -1, -1, -1):
		destroyed_asteroid = find_first_asteroid(X_loc, [0, y], asteroids_list)
		if find_first_asteroid:
			destroyed_asteroids.append(destroyed_asteroid)
			asteroids_list.remove(destroyed_asteroid)

	# up-left wave of destruction
	for x in range(0, X_loc[0]):
		destroyed_asteroid = find_first_asteroid(X_loc, [x, 0], asteroids_list)
		if find_first_asteroid:
			destroyed_asteroids.append(destroyed_asteroid)
			asteroids_list.remove(destroyed_asteroid)

	return destroyed_asteroids

destroyed_asteroids = rotating_laser(X_loc, max_x, max_y, asteroids_list)
print(destroyed_asteroids)