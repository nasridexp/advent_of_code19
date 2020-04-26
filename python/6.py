import random

f = open("data_6.txt","r")

#create a dictionary to store count of orbits
orbit_dict = {}

for orbit in f:
    orbit = orbit.strip() # get rid of \n
    orbited, orbiter = orbit.split(")")

    orbit_dict[orbited] = orbiter

AUX = 'COM'
for i in range(700):
    AUX = orbit_dict[AUX]
    print(orbit_dict[AUX])
