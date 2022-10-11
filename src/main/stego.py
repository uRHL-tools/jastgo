# Do not install PyCrypto (deprecated)
# Use CryptoDome library instead
# pip3 install -U PyCryptodome

import sys
import os
from Crypto.Random import get_random_bytes
from src import aux
from src import javaClassMapper

# TODO: search for module 'bitstring'

javaclass = f'{os.getcwd()}/ptil-stegotool/db/java_lang_String.json'
__CURRENT_DICT = javaClassMapper.map_to_dict(f'{javaclass}')

# How could we read this from the system?
__SYSTEM_BYTEORDER = "little"
__output_file = 'encoded.java'

__MIN = '100000'
_MAX = '111010'
__CHUNK_SIZE = 6
__PAD_FILLING = '0'
__PAD_LENGTH = 2
__ASCII_PAD_00 = '00'
__ASCII_PAD_01 = '01'

# pad = lambda s: s + (__AES_BLOCK_SIZE - len(s) % __AES_BLOCK_SIZE) * chr(__AES_BLOCK_SIZE - len(s) % __AES_BLOCK_SIZE)
# unpad = lambda s: s[:-ord(s[len(s) - 1:])]

# txt(UTF-8) -> bin -> AES(bin, key) -> encrypted_bin ->
# trim in chunks of 6 bits -> Format to ascii (padding) -> encode each letter with a method

__DEFAULT_OUT_FILE = 'encoded.java'


def encode(input_utf8, debug=False):
    aux.clean_runtime_env()
    f = open(__output_file, "a")
    # 1. Read input (UTF-8)
    # 2. Input to binary
    input_bin = aux.to_bitstring(input_utf8, 'utf-8')
    if debug:
        print(f'binary: {input_bin} [len {len(input_bin)}]')
    # 3. Encrypt the whole byte stream (save in a temporal file)

    # 4. Open the encrypted output file ("RB" mode)
    # 5. Trim the encrypted bin in chunks of 6 bits
    trimmed_bitstring = aux.trim_binary_string(input_bin, __CHUNK_SIZE, __PAD_FILLING)
    # 6. Pad the chunks until 8 bits
    padded_binary_array = aux.format_as_printable_ascii(trimmed_bitstring)
    # 7. Encode each chunk as ascii
    ascii_array = aux.binary_array_to_ascii_array(padded_binary_array)
    if debug:
        print(f'input: {input_utf8} -> {ascii_array}')
    # 8. Map each ascii char to a method
    f.write("public class String {\n")
    for c in ascii_array:
        to_write = __CURRENT_DICT[c]
        f.write(f'\t{to_write};\n')
    f.write("}\n")
    # 9. Clean temporal files
    aux.clean_tmp_files()
    print(f'Your result is in the file {__output_file}')
    return 0


def decode(stego_file=__DEFAULT_OUT_FILE, debug=False):
    # 1. Open the cover "class.java"
    ascii_array = []
    with open(stego_file, "r") as coverContent:
        lines = coverContent.readlines()
        for i, line in enumerate(lines):
            # 2. Map each method with the ascii character ORDER IS VERY IMPORTANT: FROM TOP TO BOTTOM
            if 0 < i < len(lines) - 1:
                clean_line = line.replace(';\n', '').replace('\t', '')

                for char, method in __CURRENT_DICT.items():
                    if method == clean_line:
                        if debug:
                            print(f'#{i} {clean_line} -> {char}')
                        ascii_array.append(char)
                        break
            # else:
                # Ignore class name declaration and closing bracket
        coverContent.close()
    # 3. convert the ascii array to binary
    # 4. Remove the padding
    # 5. Concat the elements of the binary array
    secret_bin = aux.unshadow_ascii(ascii_array)
    # 6. decrypt with AES
    # 7. Decode binary to utf-8
    readable_secret = aux.binary_to_byte(secret_bin).decode("utf-8")
    return readable_secret
