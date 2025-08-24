import sys

from .hamming_code import (
    encode_int, decode_int,
    encode_bit_array, decode_bit_array,
    encode_bits, decode_bits,
    calc_info_bits_count_from_code, calc_parity_bits_count,
    int_to_bits_array, bits_array_to_int,
    bitstr_to_bits_array, bits_array_to_bitstr,
    encode_str, decode_str,
    encode_bits_secded, decode_bits_secded,
    BE, LE
)

__all__ = [
    'encode_int', 'decode_int',
    'encode_bit_array', 'decode_bit_array',
    'encode_bits', 'decode_bits',
    'calc_info_bits_count_from_code', 'calc_parity_bits_count',
    'int_to_bits_array', 'bits_array_to_int',
    'bitstr_to_bits_array', 'bits_array_to_bitstr',
    'encode_str', 'decode_str',
    'encode_bits_secded', 'decode_bits_secded',
    'BE', 'LE'
    ]

if __name__ == '__main__':
    sys.exit()

