#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright jitui 17-5-22
#
# @author: chenyongjian@jituia.com
#


class GrayCipher(object):
    def __init__(self, iv=100000000):
        """
        格雷码
        :param iv: int，初始值向量，用于混淆原始数据
        """
        self.iv = iv

    def encrypt_gray(self, base_num):
        """
        格雷码加密
        :param base_num: int 原始数值
        :return: int，格雷码十进制数值
        """

        base_num += self.iv
        a = bin(base_num)[2:]
        c = ''
        first = a[0]
        for i, k in enumerate(a):
            if i != 0:
                o = str(int(k) ^ int(first))
                c += o
            else:
                c += first

        return int(c, 2)

    def decrypt_gray(self, gray_num):
        """
        格雷码解密
        :param gray_num: int，十进制格雷码数值
        :return: int，原始数值
        """

        gray_num = bin(gray_num)[2:]
        first = gray_num[0]
        c = ''
        for i, k in enumerate(gray_num):
            if i != 0:
                o = str(int(k) ^ int(first))
                c += o
            else:
                c += first

        c = int(c, 2)
        c -= self.iv
        return c
