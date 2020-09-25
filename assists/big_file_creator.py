import os
1/0
_chunk = 1024
_range = 1 * 1024 ** 3 // 1024
with open("sample.bin", "wb") as fp:
    for i in range(_range):
        fp.write(os.urandom(_chunk))