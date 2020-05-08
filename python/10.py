from collections import defaultdict
from math import gcd
import numpy as np

f = open("data_10.txt","r")

# Create list with asteroids positions
y = 0
asteroids_list = []
count = 1
for line in f:
    line = line.strip() # get rid of \n
    [asteroids_list.append([pos,y]) for pos, char in enumerate(line) if char == "#"]

    count = 1
    y += 1

# for each asteroid find how many other asteroids it can see
number_of_visible_ast = []
for X_pos, Y_pos in asteroids_list:
	# find distance with every other asteroid and check for asteroids in the way
	count = 0
	for X_pos_prime, Y_pos_prime in asteroids_list:
		dist_vec = np.array([X_pos_prime - X_pos, Y_pos_prime - Y_pos])
		
		hidden = False
		if abs(dist_vec[0]) > 1 or abs(dist_vec[1]) > 1:
			# find greatest common divisor of that vector components
			GCD = gcd(abs(dist_vec[0]), abs(dist_vec[1]))

			# build minimun vector
			min_vec = np.array([x / GCD for x in dist_vec])

			length_times = 1
			while np.linalg.norm(min_vec*length_times) < np.linalg.norm(dist_vec):
				vec = min_vec*length_times
				
				if vec[0] == int(vec[0]) or vec[1] == int(vec[1]):
					if [int(X_pos + vec[0]), int(Y_pos + vec[1])] in asteroids_list:
						hidden = True
				# # checking if other asteroids are in the way
				# for i in range(2, GCD+1):
				# 	X_pos_check, Y_pos_check = [x / i for x in dist_vec]

				# 	if X_pos_check == int(X_pos_check) and Y_pos_check == int(Y_pos_check):
				# 		if [int(X_pos + X_pos_check), int(Y_pos + Y_pos_check)] in asteroids_list:
				# 			print(int(X_pos + X_pos_check),int(Y_pos + Y_pos_check))
				# 			hidden = True

				length_times += 1
		elif dist_vec[0] == 0 and dist_vec[1] == 0:
			hidden = True

		if not hidden:
			count += 1


	number_of_visible_ast.append(count)

print("The max is: {} from list {}".format(max(number_of_visible_ast), number_of_visible_ast))
