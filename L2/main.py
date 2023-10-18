import math
import numpy as np
from string import ascii_lowercase
import itertools

letterFrequency = {
'e' : 12.0,
't' : 9.10,
'a' : 8.12,
'o' : 7.68,
'i' : 7.31,
'n' : 6.95,
's' : 6.28,
'r' : 6.02,
'h' : 5.92,
'd' : 4.32,
'l' : 3.98,
'u' : 2.88,
'c' : 2.71,
'm' : 2.61,
'f' : 2.30,
'y' : 2.11,
'w' : 2.09,
'g' : 2.03,
'p' : 1.82,
'b' : 1.49,
'v' : 1.11,
'k' : 0.69,
'x' : 0.17,
'q' : 0.11,
'j' : 0.10,
'z' : 0.07 
}

def entropy(bytes):
    e = 0
    ps = {}
    for byte in bytes:
        p = ps.get(byte)
        if p is None:
            ps[byte] = 1
        else:
            ps[byte] = p + 1
    for v in ps.values():
        prob = v / len(bytes)
        e -= prob * math.log(prob, 2)
    return e

def RC4(input, key):
    s = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) % 256
        s[i], s[j] = s[j], s[i]
    i = j = 0
    output = []
    for byte in input:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        key = s[(s[i] + s[j]) % 256]
        output.append(byte ^ key)
    return bytes(output)

def try_keys(encrypted):
    for key in itertools.product(ascii_lowercase, repeat=3):
        bKey = "".join(key).encode()
        decrypted = RC4(encrypted, bKey)
        e = entropy(decrypted)
        if e < 6:
            return bKey

def compare_with_shift(v1, v2, shift):
    diff = 0
    for i in range(len(v1)):
        diff += abs(v1[i] - v2[(i + shift) % len(v2)])
    return diff

def guess_shift(text):
    statistical = np.zeros(26)
    for k, v in letterFrequency.items():
        statistical[ord(k) - 97] = v / 100
    real = np.zeros(26)
    lower_count = 0
    for c in text:
        if c.islower():
            real[ord(c) - 97] += 1
            lower_count += 1
    real = [v / lower_count for v in real]
    best_diff = np.inf
    best_shift = 0
    for shift in range(26):
        diff = compare_with_shift(statistical, real, shift)
        if diff < best_diff:
            best_diff = diff
            best_shift = shift
    return best_shift

def shift_text(text, shift):
    res = ""
    for c in text:
        if c.isalpha():
            if c.islower():
                res += chr((ord(c) - 97 - shift) % 26 + 97)
            else:
                res += chr((ord(c.lower()) - 97 - shift) % 26 + 97).upper()
        else:
            res += c
    return res

def decypher(path):
    with open(path, "rb") as f:
        encrypted = f.read()
    key = try_keys(encrypted)
    print("RC4 key: ", key.decode("utf-8"))
    text = RC4(encrypted, key).decode("utf-8")
    shift = guess_shift(text)
    print("Shift: ", shift)
    print(shift_text(text, shift))

decypher("crypto4.rc4")