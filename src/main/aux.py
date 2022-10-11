import os
import chardet
from Crypto.Cipher import AES

# from bitstring import BitArray

__SYSTEM_BYTEORDER = "little"
__MIN = '100000'
_MAX = '111010'
__CHUNK_SIZE = 6
__PAD_FILLING = '0'
__PAD_LENGTH = 2
__ASCII_PAD_00 = '00'
__ASCII_PAD_01 = '01'
__TMP_ENCRYPTED_FILE = "encrypted.bin"


def verify_pw(s):
    # 3 possible key lengths: 16B (128 bits), 24B (192 bits), 32B (256 bits),
    length = len(s)
    if length == 16 or length == 24 or length == 32:
        return bytes(s, 'utf-8')
    else:
        print(f'[ERROR] Incorrect AES key length ({len(s)} bytes). It should have 16, 24 or 32 bytes')
        exit(111)


def encrypt(raw, pw):
    # pw = get_random_bytes(16)
    cipher = AES.new(pw, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(raw)

    file_out = open(__TMP_ENCRYPTED_FILE, "wb")
    # [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
    for x in (cipher.nonce, tag, ciphertext):
        file_out.write(x)
        # TODO: write in binary
        print(f'[class {type(x)}] {x}')
    file_out.close()


def decrypt(encrypted_file, pw):
    file_in = open(__TMP_ENCRYPTED_FILE, "rb")
    nonce, tag, ciphertext = [file_in.read(x) for x in (AES.block_size, AES.block_size, -1)]

    # let's assume that the key is somehow available again
    cipher = AES.new(pw, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)


def decrypt_and_print(encrypted_file, pw, encoding='UTF-8'):
    return decrypt(encrypted_file, pw).decode(encoding)


def is_printable_ascii(c):
    return min(c, __MIN) == __MIN


def trim_binary_string(s, step, pad_filling, debug=False):
    """
    :returns an array contained the trimmed string. In the last position contains the padding length of the last
    trimmed substring
    """

    # Sanitize input
    __step = int(step)
    __pad_filling = str(pad_filling)

    # Auxiliary variables
    file_ptr = counter = 0
    input_len = len(s)
    trims = []

    while file_ptr < input_len:
        # If true this is the last block, which may needs padding
        substring = s[file_ptr:file_ptr + __step]
        pad_length = 0
        if len(substring) < __step:
            # The padding length must be stored within the secret in order to decode
            # pad_length between [0, __step - 1]
            pad_length = __step - len(substring)
            padding = __pad_filling * pad_length
            substring = padding + substring
            if debug:
                print(f'WARNING: Substring {counter} NEEDS Padding [{pad_length}]')
        if debug:
            print(f'Substring #{counter}: {substring}')
        trims.append(substring)
        # If it is the last chunk append the padding
        if file_ptr + __step >= input_len:
            trims.append(pad_length)
        file_ptr += __step
        counter += 1
    return trims


def assemble_binary(bin_array):
    """ the last element does not need to be encoded, it is translated directly to the secret """
    ret = ""
    last_elem_pad = bin_array.pop()

    for index, elem in enumerate(bin_array):
        if index == len(bin_array) - 1:
            ret += elem[last_elem_pad:]
        else:
            ret += elem

    return ret


# tengo q coger los bits de 6 en 6 y hacer padding a la izquierda, asi pueden ser ascii
# ascii del \x20 al \x7A, del 32 al 122, del 00100000 al 01111010, seria lo ideal, para usar solo printable ascii
# IF chunk <= 100000 => pad 01 ELSE IF chunk > 100000 => pad 00
# 00100000 -> 00 100000 -> pad 01 => 01100000
# 01111010 -> 01 111010 ->  pad 00 => 00111010

# min: 00100001 -> 33 -> !
# max: 00111111 -> 63 -> ?
# min: 01000000 -> 64 -> @
# max: 01100000 -> 96 -> `

# [0x30, 0x39] -> [00 110000, 00 111001] -> [0, 9] => __MIN = 110000
# [0x41, 0x5A] -> [01 000001, 01 011010] -> [A, Z]

# Also 63 items
# min: 00 110000 -> 48 -> 0
# max: 00 111111 -> 63 -> ?
# min: 01 000000 -> 64 -> @
# max: 01 101111 -> 111 -> o

def format_as_printable_ascii(array, debug=False):
    max_chunk_length = 6
    desired_length = 8
    pad_length = array.pop()
    padded_array = []

    if debug:
        print(f'INFO: last item\'s pad_length = {pad_length}')
    for index, item in enumerate(array):
        if len(item) >= desired_length:
            print(f'ERROR: elem {item} cannot be padded. Max length ({max_chunk_length}) exceeded')
        else:
            # save the new element padded
            if is_printable_ascii(item):
                actual_padding = __ASCII_PAD_00
            else:
                actual_padding = __ASCII_PAD_01

            padded_array.append(actual_padding + item)
            if debug:
                print(
                    f'#{index}: {item} [{len(item)} bits] -> '
                    f'{actual_padding + item} [{len(item) + len(actual_padding)} bits]')

    padded_array.append(pad_length)
    return padded_array


def add_padding(array, desired_length, pad_filling, debug=False):
    pad_length = array.pop()
    padded_array = []
    if debug:
        print(f'INFO: last item\'s pad_length = {pad_length}')
    for index, item in enumerate(array):
        if len(item) >= desired_length:
            print(f'ERROR: elem {item} cannot be padded. Desired length ({desired_length}) exceeded')
        else:
            # save the new element padded
            actual_padding = (desired_length - len(item)) * pad_filling
            padded_array.append(actual_padding + item)
            if debug:
                print(
                    f'#{index}: {item} [{len(item)} bits] -> '
                    f'{actual_padding + item} [{len(item) + len(actual_padding)} bits]')

    padded_array.append(pad_length)
    return padded_array


def remove_padding(array, desired_length, debug=False):
    pad_length = array.pop()
    not_padded_array = []
    if debug:
        print(f'INFO: last item\'s pad_length = {pad_length}')
    for index, item in enumerate(array):
        if len(item) <= desired_length:
            print(f'ERROR: Padding cannot be removed from elem {item}. Desired length ({desired_length}) exceeded')
        else:
            # save the new element not padded
            actual_padding = len(item) - desired_length
            not_padded_array.append(item[actual_padding:])
            if debug:
                print(
                    f'#{index}: {item} [{len(item)} bits] -> '
                    f'{item[actual_padding:]} [{len(item) - actual_padding} bits]')

    not_padded_array.append(pad_length)
    return not_padded_array


def unshadow_ascii(array, debug=False):
    last_item_padding = int(array.pop())
    res = ""
    for index, item in enumerate(array):
        bits = to_bitstring(item)
        if index == len(array) - 1:
            #if __SYSTEM_BYTEORDER == 'little':
                # res = bits[last_item_padding + __PAD_LENGTH:] + res
            # elif __SYSTEM_BYTEORDER == 'big':
            res += bits[last_item_padding + __PAD_LENGTH:]
        else:
            # if __SYSTEM_BYTEORDER == 'little':
            #     res = bits[__PAD_LENGTH:] + res
            # elif __SYSTEM_BYTEORDER == 'big':
            res += bits[__PAD_LENGTH:]
    if debug:
        print(f'DEBUG: aux.unshadow_ascii() returned {res} [len {len(res)}]')
    return res


def to_bitstring(s, encoding='utf-8', debug=False):
    """
    Obtains the binary representation of the object s
    :param s: Object
    :param encoding: Encoding of the given object. Only needed when s is str
    :param debug: True to show debug logs. False to hide them
    :return: The bits representing the given structure, wrapped in a string (str) made of 0's and 1's
    """
    ret = __get_bits(s, encoding, debug)
    # assert len(s) * 8 == len(ret)
    if debug:
        print(f'[DEBUG] to_bitstring: input [{s}] -> output [{ret}]')
    return ret


def __get_bits(s, encoding='utf-8', debug=False):
    if type(s) == str:
        iterable = bytearray(s, encoding=encoding)
    elif type(s) == bytes:
        iterable = s
    else:
        print(f'[ERROR] Unsupported encoding. The object {s} cannot be converted to bits.')
        iterable = []
    # If debug traces are not needed, the loop can be written as follows:
    # return ''.join(format(i, '08b') for i in iterable
    ret = ''
    counter = 0
    for i in iterable:
        if debug:
            print(f'[DEBUG] ({counter}) byte: {i} -> {i.to_bytes(1, __SYSTEM_BYTEORDER)} -> {format(i, "08b")}')
        ret += ''.join(format(i, '08b'))
        counter += 1
    return ret


def invert_string(s):
    ret = ""
    for c in s:
        ret = c + ret
    return ret

def binary_to_byte(s):
    # If len(s) is guaranteed to be a multiple of 8, then the first arg of .to_bytes can be simplified:
    # return int(s, 2).to_bytes(len(s) // 8, byteorder='big')
    # It always be true. ASCII characters are 8 bits, unicode are 16 bits
    # Opposite to __SYSTEM_BYTEORDER since we created the binary string like following big endian order
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')


def binary_array_to_ascii_array(bin_array):
    ascii_array = []
    last_elem_pad = bin_array.pop()

    for index, elem in enumerate(bin_array):
        ascii_array.append(binary_to_byte(elem).decode("ascii"))

    # The last element is not binary is the decimal representation of the last element's padding
    ascii_array.append(str(last_elem_pad))
    return ascii_array


def remove_files(file_list, debug=False):
    assert type(file_list) == dict
    for f_name, f_path in file_list.items():
        if os.path.exists(f'./{f_path}'):
            os.remove(f_path)
        elif debug:
            print("The file does not exist")


def clean_runtime_env():
    remove_files({"output_file": "encoded.java", "tmp_file": "encrypted.bin"})


def clean_tmp_files():
    remove_files({"tmp_file": "encrypted.bin"})


def detect_encoding(filepath):
    with open(filepath, 'rb') as file:
        print(chardet.detect(file.read()))
