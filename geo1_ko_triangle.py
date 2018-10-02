from itertools import count

# b = 2x, b is odd, h = 2x +- 1
# c**2 == (b/2)**2 + h**2
# c**2 == b**2/4 + (b +- 1)**2
# c**2 == b**2/4 + b**2 + 1 +- 2b
# 4c**2 == 5b**2 + 4 +-8b
# 4c**2 - 4 = 5b**2 +- 8b
# 6b**2 > 4c**2 > 4b**2
# c > b > sqrt(2/3)c > .8c

# Found:
#17 16 15
#305 272 273
#5473 4896 4895
#98209 87840 87841

def run():
    # really slow after finding 3 tuples
    res = []
    deltas = [-1, 1]
    for c in count(2):
        sigma0 = 4 * c**2 - 4
        for b in range(2 * int(.4 * c), c, 2):
            sigma1 = 5 * b ** 2 - 8 * b
            if sigma1 == sigma0:
                print c, b, b - 1
                res.append((c, b, b - 1))
                if len(res) == 50:
                    return res
            sigma1 += 16 * b
            if sigma1 == sigma0:
                print c, b, b + 1
                res.append((c, b, b + 1))
                if len(res) == 50:
                    return res
print run()

# Perhaps better to assume:
# 5b**2 ~= 4c**2 
# b ~= sqrt(4/5) * c
# And search around this value
