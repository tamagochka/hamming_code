from hamming_code import encode, decode

print(f'----------------------------------------------')
print(f'|{'num':<5}| {'bit':<4}| {'code':<6}| {'bit':<4}| {'rest':<5}| {'err':<4}| {'bit':<4}|')
print(f'----------------------------------------------')

for i in range(1, 2048):

    if i % 100 == 0:
        print(f'----------------------------------------------')
        print(f'|{'num':<5}| {'bit':<4}| {'code':<6}| {'bit':<4}| {'rest':<5}| {'err':<4}| {'bit':<4}|')
        print(f'----------------------------------------------')

    code = encode(i)
    info = decode(code[0])
    print(f'|{i:<5}| {i.bit_length():<4}| {code[0]:<6}| {code[1]:<4}| {info[0]:<5}| {info[1]:<4}| {info[2]:<4}|', end=' ')

    if i != info[0]:
        print('- error')
    else:
        print()
