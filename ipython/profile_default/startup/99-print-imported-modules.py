from inspect import ismodule

importeds = [x for x, y in globals().items() if ismodule(y) and not x[0] == '_']
print('Imported modules: %s' % ' '.join(sorted(importeds)))
