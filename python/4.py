
import time
import re
import itertools

# my answer for part 1 is much fast (0.02s)

count_part_1 = 0
count_part_2 = 0

regex = r"^(?!.*(.)\1{2,}).*$"

begin = time.time()

for dig_1 in range(1,7):
    for dig_2 in range(dig_1, 10):
        for dig_3 in range(dig_2, 10):
            for dig_4 in range(dig_3, 10):
                for dig_5 in range(dig_4, 10):
                    for dig_6 in range(dig_5, 10):
                        num = dig_1*1e5 + dig_2*1e4 + dig_3*1e3 + dig_4*1e2 + dig_5*1e1 + dig_6
                        if num > 136818 and num < 685980:
                            if dig_1 <= dig_2 <= dig_3 <= dig_4 <= dig_5 <= dig_6:
                                # find possible repeats
                                candidates = (re.findall(r'([0-9])\1', str(num)))
                                if candidates:
                                    count_part_1 += 1

                                    # now find the actual repeated blocks
                                    repeats = itertools.chain(*[re.findall(r"({0}{0}+)".format(c), str(num)) for c in candidates])
                                    for x in repeats:
                                        if len(x) == 2:
                                            count_part_2 +=1
                                            break

print("Possible passwords part 1: {}".format(count_part_1))
print("Possible passwords part 2: {}".format(count_part_2))
print("elapsed time: {}".format(time.time() - begin))

# =============================================
#              internet solution
# =============================================
# This solution is probably clearer but much less eficient

begin = time.time()

init = 136818
end = 685979

count = 0

for num in range(init, end):
    num = str(num)

    asc = True
    equal = False
    second = False

    for p in range(5):
        if num[p] > num[p+1]:
            asc = False
            break
        elif num[p] == num[p+1]:
            equal = True

            if p == 4 and num[p] or num[p] != num[p+2]:
                if p == 0 or num[p] != num[p-1]:
                    second = True

    if asc and equal and second:
        count += 1


print("(internet) Possible passwords: {}".format(count))
print("(internet) elapsed time: {}".format(time.time() - begin))

