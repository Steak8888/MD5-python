import math


s = [
    7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
    5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
    4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
    6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21
]



def K(i):
    return math.floor(2**32 * abs(math.sin(i + 1)))


i = 0
ge = 0

A = 0x67452301
B = 0xEFCDAB89
C = 0x98BADCFE
D = 0x10325476
Aint = 0x67452301
Bint = 0xEFCDAB89
Cint = 0x98BADCFE
Dint = 0x10325476
def f(B,C,D):
    return (B & C) | (~B & D)

def g(B,C,D):
    return (B & D) | (C & ~D)

def h(B,C,D):
    return B ^ C ^ D

def ii(B,C,D):
    return C ^ (B | ~D)


message = input("Text to hash: ")

message = message.encode("utf-8")

original_length = len(message) * 8  

message += b"\x80"

while len(message) % 64 != 56:
    message += b"\x00"

message += original_length.to_bytes(8, "little")


for chunk_start in range(0, len(message), 64):
    chunk = message[chunk_start:chunk_start + 64]

    M = []

    for x in range(16):
        word = chunk[x*4:(x+1)*4]
        M.append(int.from_bytes(word, byteorder="little"))


for r1 in range(0,16):
    interim = f(B,C,D)
    A = (A + interim + K(i) + M[ge]) & 0xFFFFFFFF
    A = ((A << s[i]) | (A >> (32 - s[i]))) & 0xFFFFFFFF
    b_old = B
    B = (B + A) & 0xFFFFFFFF
    A, B, C, D = D, B, C, b_old
    i = i + 1
    ge = ge + 1



for r2 in range(16,32):
    ge = (5 * i + 1) % 16
    interim = g(B,C,D)
    A = (A + interim + K(i) + M[ge]) & 0xFFFFFFFF
    A = ((A << s[i]) | (A >> (32 - s[i]))) & 0xFFFFFFFF
    b_old = B
    B = (B + A) & 0xFFFFFFFF
    A, B, C, D = D, B, C, b_old
    i = i + 1

for r3 in range(32,48):
    ge = (3 * i + 5) % 16
    interim = h(B,C,D)
    A = (A + interim + K(i) + M[ge]) & 0xFFFFFFFF
    A = ((A << s[i]) | (A >> (32 - s[i]))) & 0xFFFFFFFF
    b_old = B
    B = (B + A) & 0xFFFFFFFF
    A, B, C, D = D, B, C, b_old
    i = i + 1

for r4 in range(48,64):
    ge = (7 * i) % 16
    interim = ii(B,C,D)
    A = (A + interim + K(i) + M[ge]) & 0xFFFFFFFF
    A = ((A << s[i]) | (A >> (32 - s[i]))) & 0xFFFFFFFF
    b_old = B
    B = (B + A) & 0xFFFFFFFF
    A, B, C, D = D, B, C, b_old
    i = i + 1

print("HASH FINISHED")
print()
print()
A = (A + Aint) & 0xFFFFFFFF
B = (B + Bint) & 0xFFFFFFFF
C = (C + Cint) & 0xFFFFFFFF
D = (D + Dint) & 0xFFFFFFFF

a_bytes = A.to_bytes(4, byteorder='little')
b_bytes = B.to_bytes(4, byteorder='little')
c_bytes = C.to_bytes(4, byteorder='little')
d_bytes = D.to_bytes(4, byteorder='little')


raw_digest = a_bytes + b_bytes + c_bytes + d_bytes

hex_digest = raw_digest.hex()

input(hex_digest)