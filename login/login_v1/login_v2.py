#!/usr/bin/env python3
# Author: He yingqin

import shelve
import time
import getpass
import os

def user_info_read():
    with shelve.open('.user_info') as f:
        user_info = dict(f)
    return user_info


def register_time():
    # 使用time模块生成一个yyyy-mm-dd HH:MM:SS格式的日期字符串作为注册时间
    register_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return register_time


def register_username_check():
    # 用户注册时，做用户名校验
    username = input('\n请输入您的用户名（只能是字母与数字的组合，长度为6~15个字符）：')
    while True:
        if username in user_info_read():
            username = input('\n\033[31m用户名已存在，请重新输入：\033[0m')
            continue
        elif not username.isalnum() or not 6 <= len(username) <= 15:
            username = input('\n\033[31m用户名只能是字母与数字的组合，长度为6~15个字符，请重新输入：\033[0m')
            continue
        else:
            break
    return username


def login_username_check():
    username = input('\n请输入您的用户名：')
    while True:
        if username in user_info_read() and user_info_read()[username][state] == 'normal':
            break
        elif username in user_info_read() and user_info_dict[user_account][1] == 'locked':
            username = input('\n\033[31m该用户已被锁定，请重新输入：\033[0m')
            continue
        else:
            username = input('\n\033[31m用户名不存在，请重新输入：\033[0m')
            continue
    return username