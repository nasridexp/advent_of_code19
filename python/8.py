import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

def define_colour(array):
    first_0 = np.where(array == '0')[0]
    first_1 = np.where(array == '1')[0]
    first_2 = np.where(array == '2')[0]

    if len(first_0)>0:
        first_0 = first_0[0]

    if len(first_1)>0:
        first_1 = first_1[0]

    if first_0 < first_1:
        return 0
    else:
        return 1


f = open("data_8.txt","r")

height = 6
width = 25

elems = height*width

for line in f:
    num_layer = len(line)/(elems)

    layer_mat = np.reshape(list(line.strip()),[num_layer, width, height])

    min_0 = elems
    min_0_ind = 0
    for layer in range(num_layer):
        # evalate contents
        num_0 = sum(sum(layer_mat[layer] == '0'))

        if num_0 < min_0:
            min_0 = num_0
            min_0_ind = layer

    # for layer with less 0 calculate:
    desired_layer = layer_mat[min_0_ind]
    print("Answer to day 8 part 1 is: {}".format(sum(sum(desired_layer == '1')) * sum(sum(desired_layer == '2'))))


# finsing the image
image = np.apply_along_axis(define_colour, 0, layer_mat)

print(image)

plt.plot(image)
plt.show()
