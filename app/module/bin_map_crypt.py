#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright jitui 17-5-22
#
# @author: chenyongjian@jituia.com
#

import string


class BinMapCrypt(object):
    def __init__(self, length=6, letter_num=64, map_letters=string.ascii_letters + string.digits + '_!'):
        """
        进制密码表
        :param length: int，所需转换成密码的个数
        :param letter_num: int，密码进制数
        :param map_letters: string，自定义的密码字符串
        """

        self.map_letters = map_letters
        self.length = length
        self.letter_num = letter_num

    def mapped(self, number):
        """
        加密
        :param number: int，所需转换成密码的数值
        :return: string，返回转换的密码
        """
        value = ''
        c = number
        for i in range(self.length):
            value += self.map_letters[c % self.letter_num]
            c = int(c / self.letter_num)
        return value

    def unmapped(self, map_string):
        """
        解密
        :param map_string: string，所需解密的密码
        :return: int，原始数值
        """
        map_string = map_string[::-1]

        m = 0
        for i in range(self.length):
            if self.map_letters.find(map_string[i]) == -1:
                raise Exception('s_decrypt_error')
            m = m * self.letter_num + self.map_letters.find(map_string[i])

        return m
