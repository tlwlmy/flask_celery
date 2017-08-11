#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016.05.07 tlwlmy
#

import base64
import urllib.parse
from time import time
from app.module.AESCipher import AESCipher

class StatCrypt(AESCipher):
    def encrypt_str(self, s):
        # 加密一串字符
        return urllib.parse.quote_plus(self.encrypt(s))

    def decrypt_str(self, encrypted):
        # 解密一串字符
        decrypted = self.decrypt(encrypted)
        return decrypted

    """

    def decrypt_params(self, encrypted):
        # 解密参数
        encrypted = encrypted.replace(' ', '+')
        decrypted = self.decrypt(encrypted)
        # decrypted = self.decrypt(base64.b64decode(encrypted))
        return parse_str(decrypted)

    def encrypt_params(self, params):
        # 加密参数
        decrypted = '&'.join(['{0}={1}'.format(key, str(value)) for key, value in params.items()])
        # return urllib.quote_plus(base64.b64encode(self.encrypt(decrypted)))
        return self.encrypt(decrypted)
    """

if __name__ == '__main__':
    stat_crypt = StatCrypt('098f6bcd4621d373cade4e832627b4f6')

    encrypted = stat_crypt.encrypt_str('test')

    import urllib.parse
    encrypted = urllib.parse.unquote(encrypted)
    print(encrypted)

    print(stat_crypt.decrypt_str(encrypted))
