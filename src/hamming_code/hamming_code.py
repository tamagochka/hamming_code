from sys import exit

import argparse


DEBUG = False

BE = 1
"""
порядок бит big-endian от старшего бита к младшему слева на право
"""

LE = 0
"""
порядок бит little-endian от младшего бита к старшему слева на право
"""


def calc_info_bits_count_from_code(code_bits_count: int) -> int:
    """
    Вычисление количества информационных бит, которое было использовано при генерации кода Хэмминга заданной длинны

    Parameters
    ----------
    code_bits_count: int
        количество бит кода Хэмминга

    Returns
    -------
    int
        количество информационных бит
    """
    for parity_bits_count in range(code_bits_count):
        info_bits_count = code_bits_count - parity_bits_count
        if 2 ** parity_bits_count >= info_bits_count + parity_bits_count + 1:
            return info_bits_count
    raise ValueError('Некорректная длинна кода Хэмминга')


def calc_parity_bits_count(info_bits_count: int) -> int:
    """
    Вычисление количества бит четности, которое необходимо для кодирования заданного количества информационных бит

    Parameters
    ----------
    info_bits_count: int
        количетво инфомрационных бит

    Returns
    -------
    int
        количество бит четности
    """
    parity_bits_count = 0
    while 1 << parity_bits_count < info_bits_count + parity_bits_count + 1:
        parity_bits_count += 1
    return parity_bits_count


def int_to_bits_array(num: int, endianness=BE) -> list[int]:
    """
    Преобразует число в массив бит

    Parameters
    ----------
    num: int
        число

    Returns
    -------
    list[int]
        массив бит
    """
    bits = [num >> i & 1 for i in range(num.bit_length() - 1,-1,-1)]
    if not endianness:
        bits.reverse()
    return bits


def bits_array_to_int(bits: list[int], endianness=BE) -> int:
    """
    Преобразует массив бит в число

    Parameters
    ----------
    bits: list[int]
        массив бит

    Returns
    -------
    int
        число
    """

    if not endianness:
        bits.reverse()
    num = 0
    for bit in bits:
        num = (num << 1) | bit
    return num


def encode_bits(info: list[int], endianness: int = BE, cut_ins = False) -> list[int]:
    """
    Генерация кода Хэмминга для заданного массива информационных бит

    Parameters
    ----------
    info: list[int]
        массив информационных бит, который необходимо закодировать

    Returns
    -------
    list[int]
        код Хэмминга
    """

    if cut_ins:  # отрезаем незначащие нули
        if endianness:
            while not info[0]: del info[0]
        else:
            while not info[-1]: del info[-1]
    # если порядок байтов big-endian, то переворачиваем массив бит
    if endianness: info.reverse()
    info_bits_count = len(info)  # сколько бит занимает info (информационные биты)
    parity_bits_count = calc_parity_bits_count(info_bits_count)  # сколько необходимо добавить бит четности
    code_bits_count = info_bits_count + parity_bits_count  # общая длинна кода Хэмминга
    if DEBUG: print(f'info_bits_count: {info_bits_count}')
    if DEBUG: print(f'parity_bits_count: {parity_bits_count}')
    if DEBUG: print(f'code_bits_count: {code_bits_count}')
    code = [0] * code_bits_count  # код Хэмминга
    info_pos = 0  # позиция в которую будут вставлены информационные биты
    # вставляем нули в позиции контрольных бит (первый разряд справа!)
    for i in range(1, code_bits_count + 1):
        if DEBUG: print(f'i & (i - 1) != 0   <=>   {i:b} & {i - 1:b} = {i & (i - 1):b}')
        # если не степень двойки то вставляем данные
        if i & (i - 1) != 0:  # == 0 если i == степени 2
            # получаем из info разряд в позиции info_pos, если он == 1
            if info[info_pos]:
                code[i - 1] = 1
                if DEBUG: print(f'code: {code}')
            info_pos += 1
    # устанавливаем биты четности
    for i in range(parity_bits_count):
        # определяем позицию в которую будем ставить бит четности
        parity_pos = 1 << i
        if DEBUG: print(f'parity_pos: {parity_pos} = {parity_pos:b}')
        # подсчитываем четность
        parity  = 0
        for j in range(1, code_bits_count + 1):
            # определяем биты, которые будут подсчитываться для определения четности
            # если позиция бита == степени 2
            if j & parity_pos:
                if DEBUG: print(f'j: {j:b} & parity_pos: {parity_pos:b} = {j & parity_pos:b} = {j & parity_pos}')
                # определяем значеине бита в найденной позиции
                if code[j - 1]:
                    # если бит == 1, то XOR с parity
                    parity ^= 1
        if parity:  #  если кол-во бит нечетное
            # то устанавливаем в заданную позицию 1            
            code[parity_pos - 1] = 1
    # если порядок байтов big-endian, то переворачиваем массив
    if endianness: code.reverse()
    if DEBUG: print(f'info: {info}')
    if DEBUG: print(f'code: {code}')
    return code


def decode_bits(code: list[int], endianness: int = BE) -> tuple[list[int], int]:
    """
    Восстановление массива информационных бит из кода Хэмминга

    Parameters
    ----------
    code: list[int]
        массив бит кода Хэмминга

    Returns
    -------
    list[int]
        восстановленный массив информационных бит, позиция ошибки или 0 если ошибки не было
    """

    # если порядок байтов big-endian, то переворачиваем массив бит
    if endianness: code.reverse()
    code_bits_count = len(code)  # сколько бит занимает code (код Хэмминга)
    info_bits_count = calc_info_bits_count_from_code(code_bits_count)
    parity_bits_count = code_bits_count - info_bits_count
    if DEBUG: print(f'info_bits_count: {info_bits_count}')
    if DEBUG: print(f'parity_bits_count: {parity_bits_count}')
    if DEBUG: print(f'code_bits_count: {code_bits_count}')
    error_pos = 0
    for i in range(parity_bits_count):
        # определяем позицию бита четности
        parity_pos = 1 << i
        if DEBUG: print(f'parity_pos: {parity_pos} = {parity_pos:b}')
        parity = 0
        # подсчитываем четность
        for j in range(1, code_bits_count + 1):
            if DEBUG: print(f'i & parity_pos = ({j}){j:b} & {parity_pos:b}({parity_pos}) = {j & parity_pos:b}', end='')
            if j & parity_pos:
                if DEBUG: print(f'   <=>   parity ^= code[j - 1]   <=>   {parity ^ code[j - 1]} = {parity} ^ {code[j - 1]}')
                parity ^= code[j - 1]
            else:
                if DEBUG: print()
        if parity:
            error_pos += parity_pos
    # коррекция ошибки
    if error_pos != 0 and error_pos <= code_bits_count:
        code[error_pos - 1] ^= 1
    # декодируем информационные биты
    info = [0] * info_bits_count
    info_pos = 0
    for i in range(1, code_bits_count + 1):
        if i & (i - 1) != 0:
            info[info_pos] = code[i - 1]
            info_pos += 1
    # если порядок байтов big-endian, то переворачиваем массив
    if endianness: info.reverse()
    return info, error_pos


def encode_int(info_num: int, endianness: int = BE) -> tuple[int, int]:
    """
    Генерация кода Хэмминга для заданных информационных бит в виде целого числа

    Parameters
    ----------
    info: int
        информационные биты, которые необходимо закодировать, в виде целого числа
    endianness: int = BE
        порядок бит big-endian (BE = 1) или little-endian (LE = 0)

    Returns
    -------
    tuple[int, int]
        код Хэмминга в виде целого числа, размер кода в битах
    """

    info_bits = int_to_bits_array(info_num, endianness=endianness)
    code_bits = encode_bits(info_bits, endianness=endianness)
    code_num = bits_array_to_int(code_bits, endianness=endianness)
    return code_num, len(code_bits)


def decode_int(code_num: int, endianness: int = BE) -> tuple[int, int, int]:
    """
    Восстановление информационных бит из кода Хэмминга в виде целого числа

    Parameters
    ----------
    code: int
        код Хэмминга в виде целого числа
    endianness: int = BE
        порядок бит big-endian (BE = 1) или little-endian (LE = 0)

    Returns
    -------
    tuple[int, int, int]
        восстановленные информационные биты в виде целого числа, позиция ошибки или 0 если ошибки не было, количество информационных бит
    """

    code_bits = int_to_bits_array(code_num, endianness=endianness)
    info_bits, error = decode_bits(code_bits, endianness=endianness)
    info_num = bits_array_to_int(info_bits, endianness=endianness)
    return info_num, error, len(info_bits)


# def encode_bit_array(bit_array: list[int], code_word_size: int) -> list[int]:
#     tmp = []
#     for i in range(len(bit_array)):
#         # отделяем code_word_size бит от массива
#         tmp.append(bit_array[i])
#         if not(i + 1) % code_word_size:
#             val = 0
#             # преобразуем биты в число
#             for b in tmp:
#                 val = (val << 1) | b
#             print(f'code word: {tmp}, val: {val}', end=', ')
#             # кодируем число
#             code, code_len = encode_int(val)
#             print(f'code: {code}, code_len: {code_len}')
#             val = code
#             for j in range(code_len):
#                 b = (val >> j) & 1
#                 print(b)
#             print()
#             tmp = []
#     return []


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Кодирование/декодирование данных в код Хэмминга')
    parser.add_argument('action', help='encode или decode')
    parser.add_argument('data', help='данные для кодирования')
    parser.add_argument('-d', '--debug', help='debug', action='store_true')
    args = parser.parse_args()

    if args.debug: DEBUG = True

    function_map = {
        'encode': encode_int,
        'decode': decode_int
    }
    selected_function = function_map.get(args.action)
    if selected_function:
        print(selected_function(int(args.data)))

    exit()
    