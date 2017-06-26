### login程序简介

- 作者：何应钦
- QQ：381904496
- Python版本：3.5.2
- 程序版本：v1
- 功能：简单实现了用户注册、登录、查询、修改密码、注销、解锁等功能，并使用本地文件存储用户信息

### login程序功能

- 用户注册（用户名和密码只能是字母和数字的组合，没有限定长度）
- 用户登录（连续3次输错密码，账户将被锁定）
    - 修改密码
    - 注销
- 查看用户信息（用户名，状态，注册时间）
- 用户解锁（需要管理员账户）
- 退出

### 使用说明

- 第一次执行程序时，会自动创建管理员账户，用户名和密码都是superuser，用于普通用户账号解锁
- 除管理员账户外，程序没有内置任何用户信息，需要先进行注册
- 对注册时使用的用户名和密码做了一定的限制
  - 必须是数字或字母
  - 长度必须是5~10个字符
- 程序使用了getpass模块来隐藏用户输入的密码，pycharm不支持getpass模块，所以请务必在命令行中使用pychon解释器来执行程序

### 备注

程序使用shelve模块来进行用户信息对象的本地存储，程序第一次运行时，会在程序所在目录生成一个.user_info.db的隐藏文件来保存用户信息