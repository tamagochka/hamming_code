import random
from src.hamming_code import encode_int, decode_int
from src.hamming_code import encode_bit_array, decode_bit_array
from src.hamming_code import encode_bits, decode_bits
from src.hamming_code import BE, LE
from src.hamming_code import bits_array_to_bitstr, bitstr_to_bits_array
from src.hamming_code import encode_str, decode_str
from src.hamming_code import encode_bits_secded, decode_bits_secded


# Тестирование кодирования и декодирования целых чисел
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

print(f'----------------------------------------------')
# Тестирование кодирования и декодирования массивов бит
bits_len = 8  # длинна информационных бит
bits = [random.randint(0, 1) for _ in range(bits_len)]  # случайные информационные биты
code = encode_bits(bits, endianness=BE)  # кодируем биты
parity = 0
for i in range(len(code)):
    parity ^= code[i]
error_bit = random.randint(0, len(code) - 1)  # выбираем случайный бит для ошибки
error_code = code.copy()
error_code[error_bit] ^= 1  # вносим ошибку
decoded_bits, error = decode_bits(error_code, endianness=BE)  # декодируем с ошибкой

print(f'bits:         {bits}')
print(f'encoded bits: {code}, parity: {parity}')
print(f'error code:   {error_code}')
print(f'error bit:    {error_bit + 1}')
print(f'decoded bits: {decoded_bits}, error: {error}')

print(f'----------------------------------------------')
# Тестирование кодирования и декодирования массивов бит с заданной длинной информационного слова
bits_array_len = 32
info_word_size = 8
bits_array = [random.randint(0, 1) for _ in range(bits_array_len)]
# кодируем массив бит
encoded_array, code_word_size = encode_bit_array(bits_array, info_word_size, endianness=LE)
# вносим ошибку в случайный бит
error_bit_index = random.randint(0, len(encoded_array) - 1)
encoded_array_with_error = encoded_array.copy()
encoded_array_with_error[error_bit_index] ^= 1
# декодируем массив бит с ошибкой
decoded_array = decode_bit_array(encoded_array_with_error, code_word_size, endianness=LE)
# ищем ошибки декодирования
errors = []
for i in range(0, len(bits_array)):
    if bits_array[i] != decoded_array[0][i]:
        errors.append(i)

print(f'info bits array:          {bits_array}')
print(f'encoded info bits array:  {encoded_array}')
print(f'encoded array with error: {encoded_array_with_error}')
print(f'error bit index:          {error_bit_index}')
print(f'decoded info bits array:  {decoded_array}')

if errors:
    print(f'Errors at bit indices: {errors}.')
else:
    print(f'No errors detected.')

print(f'----------------------------------------------')
# Тестирование кодирования и декодирования строк бит
bits_len = 16  # длинна информационных бит
bits = [random.randint(0, 1) for _ in range(bits_len)]  # случайные информационные биты
bitstr = bits_array_to_bitstr(bits)
code_str = encode_str(bitstr, endianness=LE)  # кодируем биты
code = encode_bits(bits, endianness=LE)
code_str_str = bits_array_to_bitstr(code)

decoded_bits_str, error = decode_str(code_str, endianness=LE)
decoded_bits, error2 = decode_bits(code, endianness=LE)
decoded_bits_str_str = bits_array_to_bitstr(decoded_bits)

print(f'bits:                 {bits}')
print(f'bitstr:               {bitstr}')
print(f'code_str:             {code_str}')
print(f'code_str_str:         {code_str_str}')
print(f'decoded_bits_str:     {decoded_bits_str}, error: {error}')
print(f'decoded_bits_str_str: {decoded_bits_str_str}, error2: {error2}')

print(f'----------------------------------------------')
# Тестирование кодирования и декодирования массивов бит с SECDED
bits_len = 16  # длинна информационных бит
bits = [random.randint(0, 1) for _ in range(bits_len)]  # случайные информационные биты
code = encode_bits_secded(bits, endianness=BE)  # кодируем биты
parity = 0
for bit in code:  # считаем четность полученного кода (всегда должна быть 0)
    parity ^= bit
error_bit1 = random.randint(0, len(code) - 1)  # выбираем два случайных бита для внесения ошибки
error_bit2 = random.randint(0, len(code) - 1)
error_code = code.copy()
error_code[error_bit1] ^= 1  # вносим 1ую ошибку
# если оба бита совпали, то вносим с вероятностью 50% будет либо 1 ошибка, либо без ошибок
if error_bit1 == error_bit2:
    if random.randint(0, 1):
        error_code[error_bit2] ^= 1
else:
    error_code[error_bit2] ^= 1
# декодируем с ошибкой
decoded_bits, error = decode_bits_secded(error_code, endianness=BE)
print(f'bits:         {bits}')
print(f'encoded bits: {code}, parity: {parity}')
print(f'error code:   {error_code}')
print(f'error bits:   {error_bit1 + 1}, {error_bit2 + 1}')
if error == -1:
    print(f'more than 2 errors detected, can\'t decode')
else:
    print(f'decoded bits: {decoded_bits}, error position: {error}')
# проверяем правильность декодирования
errors = []
for i in range(0, len(bits)):
    if bits[i] != decoded_bits[i]:
        errors.append(i)
if errors:
    print(f'Errors at bit indices: {errors}.')
else:
    print(f'No errors detected.')
