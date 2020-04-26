from collections import defaultdict

def count_higher_orbits(orbit_dict, init, level, registry_orbits):
	orbiters = orbit_dict[init]
	num_orbits = 0
	higher_num_orbits = 0
	for orbiter in orbiters:
		# keep track of the orbits order
		registry_orbits[orbiter] = registry_orbits[init] + [init]

		#count orbits
		num_orbits += 1
		# Accumulate number of higher orders
		higher_num_orbits += count_higher_orbits(orbit_dict, orbiter, level + 1, registry_orbits)

	return (level+1) * num_orbits + higher_num_orbits

def calculate_jupms(registry_orbits, init_pos, final_pos):
	orbit_init = registry_orbits[init_pos]
	orbit_final = registry_orbits[final_pos]

	# find latests common orbit
	com_orb = [orbit for orbit in orbit_init if orbit in orbit_final]
	latest_com_orb = com_orb[-1]

	# Find distance to latest orbit
	dist_init = len(orbit_init) - 1 - orbit_init.index(latest_com_orb)
	dist_final = len(orbit_final) - 1 - orbit_init.index(latest_com_orb)

	#return number of jumps
	return dist_init + dist_final

f = open("data_6.txt","r")

#create a dictionary to store orbits
orbit_dict = defaultdict(list)
registry_orbits = {"COM":[]}

init_com = "COM"
for orbit in f:
    orbit = orbit.strip() # get rid of \n
    orbited, orbiter = orbit.split(")")

    orbit_dict[orbited].append(orbiter)

# Run the checksum recursively
num_orbits = count_higher_orbits(orbit_dict, init_com, 0, registry_orbits)
print("The number of orbits is: {}".format(num_orbits))

# Find the necessary orbit jums
init_pos = "YOU"
final_pos = "SAN"

jumps = calculate_jupms(registry_orbits, init_pos, final_pos)

print("The number of jumps is: {}".format(jumps))
