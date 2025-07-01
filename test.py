from hamming_code import encode, decode

for i in range(1, 2048):
    code = encode(i)
    info = decode(code[0])
    print(f'{i}:{i.bit_length()} - {code[0]}:{code[1]} - {info[0]}:{info[1]}:{info[2]}', end=' ')
    if i != info[0]:
        print('- error')
    else:
        print()
