import sys

import aux
import stego


def print_separator(run_id):
    print(f'------------------------------------\n---------- NEW RUN: {run_id} ------------\n')


def run_001():
    print_separator('001')
    caca = 'a'

    aaa = '0123456789abcdef0123456789abcdef'
    pw = aux.verify_pw(aaa)

    in_bin = aux.to_bitstring(caca)
    in_bytes = aux.binary_to_byte(in_bin)
    print(f'Input (utf-8): {caca} = {in_bin} = {in_bytes}')
    aux.encrypt(in_bytes, pw)
    print(f'Encryption completed (./encrypted.bin)')
    aux.decrypt("", pw)
    # out_bytes = aux.decrypt("", pw)
    # readable_out = out_bytes.decode('UTF-8')
    readable_out = aux.decrypt_and_print("", pw)
    print(f'Decrypting ...')
    print(f'Output: {readable_out}')


def run_002():
    print_separator('002')
    secret = input("Type something:\t")
    stego.encode(secret)
    a = ['X', 'V', 'E', '!', '0']
    stego.decode(a)


def run_003():
    print_separator('003')
    bbb = b'@\x8e\x01\xc7UG\x8a\x88\xde\xeb\x1a\xf3A\xbc\xccN'
    hex_bytes = input("Type something:\t")

    print(f'Bytes (array): {hex_bytes} [len {len(hex_bytes)}]')
    bits = aux.to_bitstring(hex_bytes)
    print(f'Bits (str): {bits} [len {len(bits)}]')


if __name__ == '__main__':
    # run_001()
    # run_002()
    run_003()

