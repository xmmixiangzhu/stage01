#!/usr/bin/env python3
# Author: He yingqin

import shelve
import time
import getpass
import os


def register_time():
    # 生成一个yyyy-mm-dd HH:MM:SS格式的日期字符串作为注册时间
    register_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return register_time


def user_account_valid(user_account):
    # 判断用户输入的用户名否仅由字母和数字组成，且长度为5~10个字符
    while True:
        with shelve.open('.user_info') as user_info_dict:
            if user_account in user_info_dict:
                user_account = input('\n\033[31m用户名已存在，请重新输入：\033[0m')
                continue
            elif not user_account.isalnum():
                user_account = input('\n\033[31m用户名只能是字母与数字的组合，请重新输入：\033[0m')
                continue
            elif len(user_account) < 5 or len(user_account) > 10:
                user_account = input('\n\033[31m用户名的长度必须为5~10个字符，请重新输入：\033[0m')
                continue
            else:
                break
    return user_account


def user_password_valid(user_password):
    # 判断用户输入的密码是否仅由字母与数字组成，且长度为5~10个字符
    while True:
        if not user_password.isalnum():
            user_password = getpass.getpass('\n\033[31m密码只能是字母与数字的组合，请重新输入：\033[0m')
            continue
        elif len(user_password) < 5 or len(user_password) > 10:
            user_password = getpass.getpass('\n\033[31m密码的长度必须为5~10个字符，请重新输入：\033[0m')
            continue
        else:
            break
    return user_password


def user_choice_valid(user_choice, *args):
    # 判断用户输入的选择是否合理
    while True:
        if user_choice not in args:
            user_choice = input('\n\033[31m您的输入有误，请重新输入：\033[0m')
            continue
        else:
            break
    return user_choice


# 程序开始运行时，判断用户信息文件.user_info.db是否存在，不存在则创建该文件，并将管理员账户信息添加至该文件
if not os.path.exists('.user_info.db'):
    with shelve.open('.user_info') as user_info_dict:
        user_info_dict['superuser'] = ['superuser', 'normal', register_time()]

while True:
    # 打印功能选项，提示用户输入自己的选择
    print('\n\033[34m*************\n1.注册\n2.登录\n3.查询账户信息\n4.解锁\n5.退出\n*************\033[0m')
    user_choice = input('\n请输入您的选择：')
    user_choice = user_choice_valid(user_choice, '1', '2', '3', '4', '5')

    # 用户选择注册
    if user_choice == '1':
        # 判断用户输入的用户名是否合理（仅由字母和数字组成，长度为5~10个字符，且不存在）
        user_account = input('\n请输入您的用户名：')
        user_account_valid(user_account)
        while True:
            # 判断用户输入的密码是否仅由字母和数字组成
            user_password1 = getpass.getpass('\n请输入您的密码：')
            user_password1 = user_password_valid(user_password1)
            user_password2 = getpass.getpass('\n请再次输入您的密码：')
            # 判断两次输入的密码是否一致，一致则注册成功，注册信息写入文件，进行下一步操作；不一致则提示用户重新输入
            if user_password1 == user_password2:
                with shelve.open('.user_info') as user_info_dict:
                    user_info_dict[user_account] = [user_password1, 'normal', register_time()]
                print('\n\033[32m注册成功，请继续进行其他操作！\033[0m')
                break
            else:
                print('\n\033[31m两次输入的密码不一致，请重新输入！\033[0m')
                continue

    # 用户选择登录
    elif user_choice == '2':
        # 判断用户输入的用户名是否存在，是否被锁定
        user_account = input('\n请输入您的用户名：')
        while True:
            with shelve.open('.user_info') as user_info_dict:
                if user_account in user_info_dict and user_info_dict[user_account][1] == 'normal':
                    break
                elif user_account in user_info_dict and user_info_dict[user_account][1] == 'locked':
                    user_account = input('\n\033[31m该用户已被锁定，请重新输入：\033[0m')
                    continue
                else:
                    user_account = input('\n\033[31m用户名不存在，请重新输入：\033[0m')
                    continue
        # 判断用户输入的密码是否正确，如果连续输错3次，则锁定账号，退出程序
        COUNT = 1
        user_password = getpass.getpass('\n请输入您的密码：')
        while True:
            with shelve.open('.user_info', writeback=True) as user_info_dict:
                if user_password != user_info_dict[user_account][0] and COUNT != 3:
                    user_password = getpass.getpass('\n\033[31m密码输入错误，您还可以尝试%s次，请重新输入您的密码：' % (3 - COUNT))
                    COUNT += 1
                    continue
                elif user_password != user_info_dict[user_account][0] and COUNT == 3:
                    user_info_dict[user_account][1] = 'locked'
                    print('\n\033[31m密码输入错误次数达到3次，用户被锁定，请联系管理员解锁！\n')
                    exit()
                else:
                    print('\n\033[32m登录成功，请继续继续其它操作！\033[0m')
                    break
        # 用户登录成功后的操作
        while True:
            print('\n\033[34m**********\n1.修改密码\n2.注销\n3.返回主菜单\n4.退出\n**********\033[0m')
            user_choice = input('\n请输入您的选择：')
            user_choice = user_choice_valid(user_choice, '1', '2', '3', '4')
            # 用户选择修改密码
            if user_choice == '1':
                while True:
                    user_password1 = getpass.getpass('\n请输入您的密码：')
                    user_password1 = user_password_valid(user_password1)
                    user_password2 = getpass.getpass('\n请再次输入您的密码：')
                    if user_password1 == user_password2:
                        with shelve.open('.user_info', writeback = True) as user_info_dict:
                            user_info_dict[user_account][0] = user_password1
                            print('\n\033[32m密码修改成功，请继续进行其它操作！\033[0m')
                            break
                    else:
                        print('\n\033[31m两次输入的密码不一致，请重新输入！\033[0m')
                        continue
            # 用户选择注销
            elif user_choice == '2':
                user_choice = input('\n确认要注销该用户？（y/n）')
                user_choice = user_choice_valid(user_choice, 'Y', 'y', 'N', 'n')
                if user_choice == 'Y' or user_choice == 'y':
                    with shelve.open('.user_info') as user_info_dict:
                        user_info_dict.pop(user_account)
                        print('\n\033[32m注销成功，请继续进行其它操作！\033[0m')
                        break
                if user_choice == 'N' or user_choice == 'n':
                    continue
            # 用户选择返回主菜单
            elif user_choice == '3':
                break
            # 用户选择退出
            else:
                print('\n\033[32m感谢您的使用，再见！\033[0m\n')
                exit()

    # 用户选择查询账户信息
    elif user_choice == '3':
        user_account = input('\n请输入您要查询的用户名：')
        while True:
            with shelve.open('.user_info') as user_info_dict:
                if user_account in user_info_dict:
                    print('\n\033[32m用户名：%s\n状态：%s\n注册时间：%s\033[0m'
                          % (user_account, user_info_dict[user_account][1], user_info_dict[user_account][2]))
                    break
                else:
                    print('\n\033[31m用户名不存在，请继续进行其它操作！\033[0m')
                    break

    # 用户选择解锁
    elif user_choice == '4':
        # 判断用户输入的管理员用户名是否正确
        user_account = input('\n请输入管理员的用户名：')
        while True:
            if user_account != 'superuser':
                user_account = input('\n\033[31m您的输入用户名不正确，请重新输入：\033[0m')
                continue
            else:
                break
        # 判断用户输入的管理员密码是否正确
        COUNT = 1
        user_password = getpass.getpass('\n请输入管理员的密码：')
        while True:
            with shelve.open('.user_info') as user_info_dict:
                if user_passwd != user_info_dict['superuser'][0] and COUNT !=3:
                    user_passwd = getpass.getpass('\n\033[31m密码输入错误，您还可以尝试%s次，请重新输入管理员的密码：' % (3 - COUNT))
                    COUNT += 1
                    continue
                elif user_passwd != user_info_dict[user_account][0] and COUNT == 3:
                    print('\n\033[31m密码输入错误次数达到3次，请稍后再试！\n')
                    exit()
                else:
                    print('\n管理员登录成功，请继续进行其它操作！')
                    break
        # 管理员密码输入正确之后的操作
        while True:
            print('\n\033[34m**********\n1.用户解锁\n2.返回主菜单\n3.退出\n**********\033[0m')
            user_choice = input('\n请输入您的选择：')
            user_choice = user_choice_valid(user_choice, '1', '2', '3')
            # 用户选择解锁
            if user_choice == '1':
                user_account = input('\n请输入要解锁的用户名：')
                while True:
                    with shelve.open('.user_info', writeback=True) as user_info_dict:
                        if user_account in user_info_dict and user_info_dict[user_account][1] == 'locked':
                            user_info_dict[user_account][1] = 'normal'
                            print('\n\033[32m用户%s解锁成功，请继续进行其它操作！\033[0m' % user_account)
                            break
                        elif user_account in user_info_dict and user_info_dict[user_account][1] == 'normal':
                            print('\n\033[32m用户%s未被锁定，请继续进行其它操作！\033[0m' % user_account)
                            break
                        else:
                            print('\n\033[31m用户名不存在，请继续进行其它操作！\033[0m')
                            break
            # 用户选择返回主菜单
            elif user_choice == '2':
                break
            # 用户选择退出
            else:
                print('\n\033[32m感谢您的使用，再见！\033[0m\n')
                exit()

    # 用户选择退出
    else:
        print('\n\033[32m感谢您的使用，再见！\033[0m\n')
        exit()
