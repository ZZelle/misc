sudoku = [
    [0, 0, 3, 0, 0, 0, 0, 4, 0],
    [0, 0, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 0, 6, 2, 0, 3, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 9, 0],
    [3, 0, 4, 2, 0, 8, 5, 0, 1],
    [0, 8, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 8, 0, 6, 9, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0, 0],
    [7, 3, 0, 0, 0, 0, 6, 0, 0],
]

r3 = range(3)
r9 = range(9)
s9 = set(range(1, 10))


def get_candidates(sudomap, (x, y)):
    useds = {sudomap[x, yy] for yy in r9}
    useds |= {sudomap[xx, y] for xx in r9}
    x0 = x - x % 3
    y0 = y - y % 3
    useds |= {sudomap[x0 + xx, y0 + yy] for xx in r3 for yy in r3}
    return s9 - useds

def is_xsudoku(sudomap):
    if len({sudomap[x, x] for x in r9} - {0}) == 9:
        if len({sudomap[x, 8-x] for x in r9} - {0}) == 9:
            return True
    return False


sudomap = {(x, y): v for y, vv in enumerate(sudoku) for x, v in enumerate(vv)}
unknowns = sorted(k for k, v in sudomap.items() if not v)

a = 0
b = 0
c = 0
d = 0
def visit(sudomap, unknowns):
    k = unknowns.pop()
    for v in get_candidates(sudomap, k):
        sudomap[k] = v
        if unknowns:
            visit(sudomap, unknowns)
        else:
            global a, b, c, d
            a += 1
            b += sudomap[0, 0]
            if is_xsudoku(sudomap):
                c += 1
                d += sudomap[8, 0]
    sudomap[k] = 0
    unknowns.append(k)

visit(sudomap, unknowns)
print a, b, c, d
one = (c * (b + a * d)) % 1000
two = (c * b + a -d) % 1000
print "N48 46.%s" % one
print "E 2 10.%s" % two
