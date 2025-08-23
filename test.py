import random
from src.hamming_code import encode_int, decode_int
from src.hamming_code import encode_bit_array, decode_bit_array
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


bits_array_len = 32
info_word_size = 8
bits_array: list[int] = [random.randint(0, 1) for _ in range(bits_array_len)]
print(f'info bits array: {bits_array}')
encoded_array, code_word_size = encode_bit_array(bits_array, info_word_size)
print(f'encoded info bits array:  {encoded_array}')
error_bit_index = random.randint(0, len(encoded_array) - 1)
encoded_array[error_bit_index] ^= 1
print(f'encoded array with error: {encoded_array}')
print(f'error bit index: {error_bit_index}')
decoded_array = decode_bit_array(encoded_array, code_word_size)
print(f'decoded info bits array: {decoded_array}')
