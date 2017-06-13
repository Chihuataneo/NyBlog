function decode_str(string) {
    string = Base64.decode(string);
    key = 'nyloner';
    len = key.length;
    code = '';
    for (i = 0; i < string.length; i++) {
        var k = i % len;
        code += String.fromCharCode(string.charCodeAt(i) ^ key.charCodeAt(k))
    }
    return Base64.decode(code)
}