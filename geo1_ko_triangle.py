import it507544128ertools
import time

# c**2 == (b/2)**2 + h**2 => b is even
# c**2 == b**2/4 + (b +- 1)**2
# 4c**2 == b**2 + 4(b +- 1)**2
# 4c**2 - 4 == 5b**2 +- 8b
# 5b**2 ~= 4c**2
# b ~= sqrt(.8)c

# b = 2x
# c**2 == x**2 + (2x +- 1)**2
# c**2 == 5x**2 +- 4x + 1 => c is odd
# c = 2y + 1
# (2y + 1)** 2 == 5x**2 +- 4x + 1
# 4y**2 + 4y == 5x**2 +- 4x => x is even
# b = 2x = 4xx
# 4y**2 + 4y == 20xx**2 +- 8xx
# y**2 + y == 5xx**2 +- 2xx, y**2 + y is even so X is even
# b = 2x = 4xx = 8xxx
# y**2 + y == 20xxx**2 +- 4xxx
# y(y+1) == 4(5xxx**2 +- 1) so y = 4yy or y = 4yy - 1 so 5xxx**2 is even
# b = 2x = 16xxxx
# y(y+1) == 4(20xxx**2 +- 1)


# Found:
#17 16 15
#305 272 273
#5473 4896 4895
#98209 87840 87841
#1762289 1576240 1576239
#31622993 28284464 28284465
#567451585 507544128 507544127

# c == 12k + d + 1 with d = 0 or 4 or e = 0 or 1 
# (12k + d + 1)**2 == x**2 + (2x +- 1)**2
# 144k + 24k + 24kd + 2d + d**2 == 5x**2 +- 4x 
# 144k + 24k + 24kd + 2d + d**2 == 20xx**2 +- 8xx 
# 144k**2 + 24k + 96ke + 24e == 20xx**2 +- 8xx 
# 36k**2 + 6k + 24ke + 6e == 5xx**2 +- 2xx
# 36k**2 + 6k + 24ke + 6e == 20xxx**2 +- 4xxx
# 18k**2 + 3k + 12ke + 3e == 10xxx**2 +- 2xxx
# 18k**2 + 3k + 12ke + 3e == 20xxxx**2 +- 4xxxx
# so k + e = 2kk and k = 2kk - e




def run():
    start = time.time()
    index = 0
    count = itertools.count
    halfrate = .8 ** .5 /2
    for c in count(13, 4):
        left = 4 * c ** 2 - 4
        b0 = int(halfrate * c) * 2
        for b in count(b0, 2):
            right = 5 * b ** 2 - 8 * b
            if left == right:
                print index, c, b, b - 1, time.time() - start
                index += 1
                break
            right += 16 * b
            if left == right:
                print index, c, b, b + 1, time.time() - start
                index += 1
                break
            if left < right:
                break
        else:
            for b in count(b0, -2):
                right = 5 * b ** 2 + 8 * b
                if left == right:
                    print index, c, b, b + 1, time.time() - start
                    index += 1
                    break
                right -= 16 * b
                if left == right:
                    print index, c, b, b - 1, time.time() - start
                    index += 1
                    break
                if left > right:
                    break

run()


# x, y, z = n**2 - m**2, 2nm, n**2 + m**2
# x**2 + y**2 == z**2
# in our case:
# b +- 1 == n**2 - m**2 and b/2 == 2nm
# b == n**2 - m**2 +- 1 == 4nm
# c == n**2 + m**2 = n

