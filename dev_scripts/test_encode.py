import base64


def from_char_code(a, *b):
    return chr(a % 65536) + ''.join([chr(i % 65536) for i in b])


def encode_str(string):
    secret_key = 'nyloner'
    key_length = len(secret_key)
    string = base64.b64encode(string.encode('utf-8')).decode('utf-8')
    code = ''
    for i in range(len(string)):
        index = i % key_length
        code += from_char_code(ord(string[i]) ^ ord(secret_key[index]))
    result = base64.b64encode(code.encode('utf-8')).decode('utf-8')
    return result


def decode_str(string):
    secret_key = 'nyloner'
    key_length = len(secret_key)
    string = base64.b64decode(string).decode('utf-8')
    code = ''
    for i in range(len(string)):
        index = i % key_length
        code += from_char_code(ord(string[i]) ^ ord(secret_key[index]))
    result = base64.b64decode(code).decode('utf-8')
    return result


print(encode_str('test'))
print(decode_str('Cj46FQokT1M='))
