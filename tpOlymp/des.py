import random


def ip(block):
    permute = (1, 5, 2, 0, 3, 7, 4, 6)
    return [block[i] for i in permute]


def F(sub_block, sk):
    permute = (3, 0, 1, 2, 1, 2, 3, 0)
    ep = [sub_block[i] for i in permute]
    p = [int(x) ^ int(y) for x, y in zip(ep, sk)]
    s0 = (
        (1, 0, 3, 2),
        (3, 2, 1, 0),
        (0, 2, 1, 3),
        (3, 1, 3, 2)
    )
    s1 = (
        (0, 1, 2, 3),
        (2, 0, 1, 3),
        (3, 0, 1, 0),
        (2, 1, 0, 3)
    )
    x, y = int(str(p[0])+str(p[3]), 2), int(str(p[1])+str(p[2]), 2)
    l = list(str(bin(s0[x][y])))[2:]
    l = [0]*(2 - len(l)) + l
    x, y = int(str(p[4])+str(p[7]), 2), int(str(p[5])+str(p[6]), 2)
    r = list(str(bin(s1[x][y])))[2:]
    r = [0]*(2 - len(r)) + r
    bits = l + r
    permute = (1, 3, 2, 0)
    return [bits[i] for i in permute]


def f(block, k):
    return [int(x) ^ int(y) for x, y in zip(block[:4], F(block[4:], k))] + block[4:]


def sw(block):
    return block[4:] + block[:4]


def ip_rew(block):
    permute = (3, 0, 2, 4, 6, 1, 7, 5)
    return [int(block[i]) for i in permute]


def p8(k):
    permute = (5, 2, 6, 3, 7, 4, 9, 8)
    return [k[i] for i in permute]


def p10(k):
    permute = (2, 4, 1, 6, 3, 9, 0, 8, 7, 5)
    return [k[i] for i in permute]


def shift(k, positions):
    mask = [x for x in xrange(positions, 5)] + [x for x in xrange(0, positions)]
    l = k[:6]
    r = k[5:]
    return [l[i] for i in mask] + [r[i] for i in mask]


def encrypt(block, key):
    k1 = p8(shift(p10(key), 1))
    k2 = p8(shift(p10(key), 3))
    return [str(x) for x in ip_rew(f(sw(f(ip(block), k1)), k2))]


def decrypt(block, key):
    k1 = p8(shift(p10(key), 1))
    k2 = p8(shift(shift(p10(key), 1), 2))
    return [str(x) for x in ip_rew(f(sw(f(ip(block), k2)), k1))]


def encrypt_3des(block, key):
    return encrypt(encrypt(encrypt(block, key), key), key)


def decrypt_3des(block, key):
    return decrypt(decrypt(decrypt(block, key), key), key)


def encrypt_block(block, key):
    block = [list(str(bin(x)))[2:] for x in block]
    block = [['0']*(8 - len(x)) + x for x in block]
    print 'Inputted block: ', block
    vec = list(str(bin(random.randint(0, 255)))[2:])
    vec = ['0'] * (8 - len(vec)) + vec
    inp = vec
    res = []
    for v in block:
        inp = encrypt_3des(inp, key)
        res.append([int(x) ^ int(y) for x, y in zip(v, inp)])
    for i in xrange(len(res)):
        for j in xrange(len(res[0])):
            res[i][j] = str(res[i][j])
    return {'initial': vec, 'encrypt': res}


def decrypt_block(block, vec, key):
    inp = vec
    res = []
    for v in block:
        inp = encrypt_3des(inp, key)
        res.append([int(x) ^ int(y) for x, y in zip(v, inp)])
    for i in xrange(len(res)):
        for j in xrange(len(res[0])):
            res[i][j] = str(res[i][j])
    return ''.join([chr(int(''.join(x), 2)) for x in res])


key = tuple(raw_input('Input the key: '))
input_str = [ord(x) for x in tuple(raw_input('Input data for encryption: '))]

en = encrypt_block(input_str, key)
print 'Initial vector is: ', en['initial']
print 'Encrypted data is: ', en['encrypt']
print 'Decrypted value is: ', decrypt_block(en['encrypt'], en['initial'], key)


# input 01000001
# key 1010000010
# result 00010101

#00110110