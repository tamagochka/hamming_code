from math import log2, ceil
from sys import exit

import argparse


DEBUG = False


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


def encode(info: int) -> tuple[int, int]:
    """
    Генерация кода Хэмминга для заданных информационных бит

    Parameters
    ----------
    info: int
        информационные биты, которые необходимо закодировать

    Returns
    -------
        tuple[int, int]
            код Хэмминга, размер кода в битах
    """
    info_bits_count = info.bit_length()  # сколько бит занимает info (информационные биты)
    parity_bits_count = calc_parity_bits_count(info_bits_count)  # сколько необходимо добавить бит четности
    code_bits_count = info_bits_count + parity_bits_count  # общая длинна кода Хэмминга
    if DEBUG: print(f'info_bits_count: {info_bits_count}')
    if DEBUG: print(f'parity_bits_count: {parity_bits_count}')
    if DEBUG: print(f'code_bits_count: {code_bits_count}')
    code = 0  # код Хэмминга
    info_pos = 0  # позиция в которую будут вставлены информационные биты
    # вставляем нули в позиции контрольных бит (первый разряд справа!)
    for i in range(1, code_bits_count + 1):
        if DEBUG: print(f'i & (i - 1) != 0   <=>   {i:b} & {i - 1:b} = {i & (i - 1):b}', end='')
        # если не степень двойки то вставляем данные
        if i & (i - 1) != 0:  # == 0 если i == степени 2
            if DEBUG: print(f'   <=>   (info >> info_pos) & 1   <=>   ({info:b} >> {info_pos}) & 1 = {(info >> info_pos) & 1:b}', end='')
            # получаем из info разряд в позиции info_pos, если он == 1
            if (info >> info_pos) & 1:
                if DEBUG: print(f'   <=>   (info >> info_pos) & 1   <=>   {code:b} | {1 << (i - 1):b}', end=' = ')
                # сдвигаем 1 на ее позицию в коде Хэмминга и добавляем ее в код
                code |= 1 << (i - 1)
                if DEBUG: print(f'code: {code:b}')
            # переходим к следующему разряду info
            info_pos += 1
        if DEBUG: print()
    # устанавливаем биты четности
    for i in range(parity_bits_count):
        # определяем позицию в которую будем ставить бит четности
        parity_pos = 1 << i
        if DEBUG: print(f'parity_pos: {parity_pos} = {parity_pos:b}')
        # подсчитываем четность
        parity = 0
        for j in range(1, code_bits_count + 1):
            # определяем биты, которые будут подсчитываться для определения четности
            # если позиция бита == степени 2
            if j & parity_pos:
                if DEBUG: print(f'j: {j:b}', end=' ')
                if DEBUG: print(f'code >> (j - 1) & 1   <=>   {code:b} >> {j - 1} = {code >> (j - 1):b} & 1 = {code >> (j - 1) & 1:b}')
                # определяем значеине бита в найденной позиции
                if code >> (j - 1) & 1:
                    # если бит == 1, то XOR с parity
                    parity ^= 1  
        if parity:  #  если кол-во бит нечетное
            # то устанавливаем в заданную позицию 1
            code |= 1 << (parity_pos - 1)
    if DEBUG: print(f'info: {info:b}')
    if DEBUG: print(f'code: {code:b}')
    return code, code_bits_count


def decode(code: int) -> tuple[int, int, int]:
    """
    Восстановление информационных бит из кода Хэмминга

    Parameters
    ----------
    code: int
        код Хэмминга

    Returns
    -------
        tuple[int, int, int]
            восстановленные информационные биты, позиция ошибки или 0 если ошибки не было, количество информационных бит
    """
    code_bits_count = code.bit_length()  # сколько бит занимает code (код Хэмминга)
    info_bits_count = calc_info_bits_count_from_code(code_bits_count)
    parity_bits_count = code_bits_count - info_bits_count
    if DEBUG: print(info_bits_count)
    if DEBUG: print(parity_bits_count)
    if DEBUG: print(code_bits_count)
    error_pos = 0
    for i in range(parity_bits_count):
        parity_pos = 1 << i
        if DEBUG: print(f'parity_pos: {parity_pos} = {parity_pos:b}')
        # подсчитываем четность
        parity = 0
        for i in range(1, code_bits_count + 1):
            if DEBUG: print(f'i & parity_pos = ({i}){i:b} & {parity_pos:b}({parity_pos}) = {i & parity_pos:b}', end='')
            if i & parity_pos:
                if DEBUG: print(f'   <=>   parity ^= code >> (i - 1) & 1   <=>   {parity ^ (code >> (i - 1) & 1)} = {parity} ^ {code:b} >> {(i - 1)} & 1')
                parity ^= code >> (i - 1) & 1
            else:
                if DEBUG: print()
        if parity:
            error_pos += parity_pos
    # коррекция ошибки
    if error_pos != 0 and error_pos <= code_bits_count:
        code ^= 1 << (error_pos - 1)
    # декодируем информационные биты
    info = 0
    info_pos = 0
    for i in range(1, code_bits_count + 1):
        if i & (i - 1) != 0:
            bit = code >> (i - 1) & 1
            info |= bit << info_pos
            info_pos += 1
    return info, error_pos, info_bits_count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Кодирование/декодирование данных в код Хэмминга')
    parser.add_argument('action', help='encode или decode')
    parser.add_argument('data', help='данные для кодирования')
    parser.add_argument('-d', '--debug', help='debug', action='store_true')
    args = parser.parse_args()

    if args.debug: DEBUG = True

    function_map = {
        'encode': encode,
        'decode': decode
    }
    selected_function = function_map.get(args.action)
    if selected_function:
        print(selected_function(int(args.data)))

    exit()
    