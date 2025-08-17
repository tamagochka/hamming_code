import random
from src.hamming_code import encode_int, decode_int
from src.hamming_code import encode_bit_array
from src.hamming_code import encode_bits, decode_bits
from src.hamming_code import BE, LE
from src.hamming_code import int_to_bits_array, bits_array_to_int


print(f'----------------------------------------------')
print(f'|{'num':<5}| {'bit':<4}| {'code':<6}| {'bit':<4}| {'rest':<5}| {'err':<4}| {'bit':<4}|')
print(f'----------------------------------------------')

for i in range(1, 2048):

    if i % 100 == 0:
        print(f'----------------------------------------------')
        print(f'|{'num':<5}| {'bit':<4}| {'code':<6}| {'bit':<4}| {'rest':<5}| {'err':<4}| {'bit':<4}|')
        print(f'----------------------------------------------')

    code = encode_int(i, endianness=LE)
    info = decode_int(code[0], endianness=LE)
    print(f'|{i:<5}| {i.bit_length():<4}| {code[0]:<6}| {code[1]:<4}| {info[0]:<5}| {info[1]:<4}| {info[2]:<4}|', end=' ')

    if i != info[0]:
        print('- error')
    else:
        print()


# bits_array_len = 8
# code_word_size = 8

# bits_array: list[int] = [random.randint(0, 1) for _ in range(bits_array_len)]
# # bits_array = [0, 1, 0, 1, 0, 1, 1, 0, 0]

# print(bits_array)
# code = encode_bits(bits_array, endianness=LE)
# print(code)

# code[random.randint(0, len(code) - 1)] ^= 1
# print(code)

# info = decode_bits(code, endianness=LE)
# print(info)


# # hamming_encoded_array = encode_bit_array(bit_array, code_word_size)


