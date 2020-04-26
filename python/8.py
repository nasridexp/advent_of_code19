import numpy as np
import matplotlib.pyplot as plt

def define_colour(array):
    first_0 = np.where(array == '0')[0]
    first_1 = np.where(array == '1')[0]
    found_0 = False
    found_1 = False

    if len(first_0)>0:
        first_0 = first_0[0]
        found_0 = True

    if len(first_1)>0:
        first_1 = first_1[0]
        found_1 = True

    if found_0 and found_1:
        if first_0 < first_1:
            return 0
        else:
            return 1
    elif found_0:
        return 0
    elif found_1:
        return 1
    else:
        return 2


f = open("data_8.txt","r")

height = 6
width = 25

elems = height*width

for line in f:
    num_layer = int(len(line.strip())/(elems))

    layer_mat = np.reshape(list(line.strip()),[num_layer, height, width])

fewest_0 = min(layer_mat, key=lambda _: sum(sum( _ == '0')))

# Initial method. changed by lambda function above 
# min_0 = elems
# min_0_ind = 0
# for layer in range(num_layer):
#     # evalate contents
#     num_0 = sum(sum(layer_mat[layer] == '0'))

#     if num_0 < min_0:
#         min_0 = num_0
#         min_0_ind = layer

# for layer with less 0 calculate:
print("Answer to day 8 part 1 is: {}".format(sum(sum(fewest_0 == '1')) * sum(sum(fewest_0 == '2'))))


# finsing the image
image = np.apply_along_axis(define_colour, 0, layer_mat)

print(layer_mat)
print(image)

plt.imshow(image)
plt.show()
