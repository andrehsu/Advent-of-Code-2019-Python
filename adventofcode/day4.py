import re

lo = 256310
hi = 732736


def is_increasing(num):
    last = -1
    for i in map(int, str(num)):
        if i < last:
            return False
        last = i
    return True


count = 0

for i in range(lo, hi + 1):
    if re.findall(r'(.)\1', str(i)) and is_increasing(i):
        count += 1

print(count)


def has_isolate_group(i):
    s = '_' + str(i) + '_'

    for i in range(1, len(s) - 1 - 1):
        if s[i] == s[i + 1] and s[i] != s[i - 1] and s[i] != s[i + 2]:
            return True

    return False


count = 0

for i in range(lo, hi + 1):
    if has_isolate_group(i) and is_increasing(i):
        count += 1

print(count)
