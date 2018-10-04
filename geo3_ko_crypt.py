import collections

msg = [
    18, 7, 66, 2, 86, 93, 74, 89, 23, 101, 92, 42, 6, 3, 52, 82, 84, 76, 213,
    73, 13, 120, 54, 19, 81, 17, 89, 71, 91, 17, 105, 68, 81, 99, 36, 74, 2,
    80, 70, 82, 89, 26, 126, 64, 59, 82, 96, 21, 89, 71, 30, 116, 79, 68, 93,
    111, 82, 102, 3, 67, 19, 122, 89, 79, 85, 9, 7, 23, 68, 2, 222, 64, 30,
    120, 83, 85, 9, 21, 27, 81, 23, 66, 95, 91, 28, 110, 95, 70, 42, 1, 3, 51,
    82, 93, 74, 28, 105, 66, 64, 59, 19, 77, 4, 82, 30, 109, 85, 66]

# guess key length:
# * search repeated text patterns
# * key length divides the number of letters between occurrences
# => key length divides 11, 22, 55, 88 => key length == 11 

msg_length = len(msg)
key_length = 11
indents = range(key_length)
candidates = range(32, 128)
parts = [[msg[x] for x in range(indent, msg_length, key_length)] for indent in indents]

invalids = range(32) + range(123, 256) + [64, 96]
invalids = set(invalids) - {176, 224, 232, 233, 234, 249}
indent_keys = []
for indent in indents:
    keys = []
    for candidate in candidates:
        decrypteds = {x ^ candidate for x in parts[indent]}
        if not decrypteds & invalids:
            keys.append(candidate)
    indent_keys.append(keys)
    print indent, len(keys)

indent = 4
for key in indent_keys[indent]:
    print '%3d' % key, ''.join(chr(x ^ key).decode('iso-8859-1') for x in parts[indent])


keys = [
    94,  # 0
    98,  # 1
    0,   # 2
    0,   # 3
    55,  # 4
    0,   # 5
    0,   # 6
    0,   # 7
    0,   # 8
    0,   # 9
    0,   # 10
]

print ''.join(chr(x ^ keys[i % key_length]) for i, x in enumerate(msg)).decode('iso-8859-1')[:2]

# 0 =>
# 1 =>
# 2 =>
# 3 =>
# 4 => 55
# 5 =>
# 6 =>
# 7 =>
