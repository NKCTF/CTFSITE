# ctfsite
为南开 CTF 开发的 Web 项目。

## 生产环境配置说明

以下均针对 Ubuntu 生产环境配置。

### 下载

从 github 上下载本仓库到本地：

```bash
$ git clone https://github.com/NKCTF/ctfsite.git && cd ctfsite
```

### 隐私设置

本项目利用 `python` 的环境变量设置来保存 `mysql` 用户名密码和 `github OAuth2.0`  的 `secret key` ，需要通过以下的方式创建两个文件：

```bash
$ cat << _EOF_ > ctfsite/config.py
import os
os.environ["ctfsite-mysql-dbname"] = <你的数据库名称>
os.environ["ctfsite-mysql-username"] = <用于登陆 mysql 的用户名>
os.environ["ctfsite-mysql-password"] = <该用户名的密码>
_EOF_

$ cat << _EOF_ > backend/user/config.py
import os
os.environ["github_client_secret"] = <github 第三方登陆的密钥>
_EOF_
```

*PostScript*：

- 若没有配置 `github` 第三方登陆接口，可以不配置第二个文件内容，但是一定要创建这个文件。

- 若设置了域名或使用 ip 访问需要在 `ctfsite/settings.py` 中的 `ALLOWED_HOST` 中进行设置。

### 前端配置运行

需要配置安装 `node.js` 与管理它的 `npm`：

```bash
$ apt-get install nodejs npm
```

升级 `node.js` 与 `npm` 到最新版本：

```bash
$ npm install -g n && n stable
# 升级 node.js

$ npm -g install npm@next
# 升级 npm
```

安装 `node.js` 包并且生成静态文件：

```bash
$ cd frontend
$ npm install && npm run build
$ cd ..
```

### 后端配置运行

需要安装 `python3.6` 或以上版本，需要配置 `mysql` 并且将 `utf-8` 设置为默认字符集。

安装依赖文件：

```bash
$ pip install -r requirement.txt
```

迁移数据库：

```bash
$ python manage.py migrate
# 如果发生了错误，可以尝试以下的命令序列：
# python manage.py makemigrations user
# python manage.py makemigrations question
# python manage.py makemigrations message
# python manage.py migrate
```

收集静态文件：

```bash
$ python manage.py collectstatic
```

*PostScript*：此时通过一个的命令就可以直接运行服务了，但是这个服务不适合生产级的应用（亲测两个人同时访问就有崩溃的可能）：

```bash
$ python manage.py runserver 0:80
```

其中，`0 ` 表示可以通过任意 `ip` 访问该服务器，`80` 表示开放在服务器的 `80` 端口。

### 生产级配置说明

`Django` 采用 `wsgi` 协议与 `nginx` 进行通信，官网的配置教程在下：

> https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html

介于官网有详细的 `Debug` 教程，在此就不重复了。

## 开发环境配置说明

对于开发框架，前端使用 `Vue.js`，后端使用 `Django`

### 下载

从 github 上下载本仓库到本地：

```bash
$ git clone https://github.com/NKCTF/ctfsite.git && cd ctfsite
```

### 隐私设置

本项目利用 `python` 的环境变量设置来保存 `mysql` 用户名密码和 `github OAuth2.0`  的 `secret key` ，需要通过以下的方式创建两个文件：

```bash
$ cat << _EOF_ > ctfsite/config.py
import os
os.environ["ctfsite-mysql-dbname"] = <你的数据库名称>
os.environ["ctfsite-mysql-username"] = <用于登陆 mysql 的用户名>
os.environ["ctfsite-mysql-password"] = <该用户名的密码>
_EOF_

$ cat << _EOF_ > backend/user/config.py
import os
os.environ["github_client_secret"] = <github 第三方登陆的密钥>
_EOF_
```

*PostScript*：

- 在本地部署开发环境，无法使用 `github` 的第三方登陆，进行调试时应直接注册账号。
- 一定要创建 `backend/user/config.py` 和 `ctfsite/config.py` 这两个文件。

### 前端配置运行

需要配置安装 `node.js` 与管理它的 `npm`：

```bash
$ apt-get install nodejs npm
```

升级 `node.js` 与 `npm` 到最新版本：

```bash
$ npm install -g n && n stable
# 升级 node.js

$ npm -g install npm@next
# 升级 npm
```

安装 `node.js` 包并且生成静态文件：

```bash
$ cd frontend
$ npm install && npm run dev
```

这时使用 `chrome` 访问 `localhost:8080` 即可实时进行开发。（好像需要禁用什么安全策略来者，有空再写）

### 后端配置运行

需要安装 `python3.6` 或以上版本，需要配置 `mysql` 并且将 `utf-8` 设置为默认字符集。

安装依赖文件：

```bash
$ pip install -r requirement.txt
```

迁移数据库：

```bash
$ python manage.py migrate
# 如果发生了错误，可以尝试以下的命令序列：
# python manage.py makemigrations user
# python manage.py makemigrations question
# python manage.py makemigrations message
# python manage.py migrate
```

收集静态文件：

```bash
$ python manage.py collectstatic
```

*PostScript*：此时通过一个的命令就可以直接运行服务了，但是这个服务不适合生产级的应用（亲测两个人同时访问就有崩溃的可能）：

```bash
$ python manage.py runserver 0:80
```

其中，`0 ` 表示可以通过任意 `ip` 访问该服务器，`80` 表示开放在服务器的 `80` 端口。

## Django

简单介绍关于 Django。

- 使用命令 `django-admin startproject mysite` 可以初始化一个 Django 项目。

- Django 提供了一个集成了许多管理功能的 Python 脚本 &rarr; **manage.py**

- 一个 Django 项目由许多应用组成，这些应用为 Python 的模块的文件夹，与 manage.py 一起置于根文件夹下，使用 `python manage.py startapp polls` 命令可以初始化创建一个 Django 应用。
- 在应用的文件夹内，一般有以下文件：
  - `models.py`：这个文件表明的数据库的设计方式，内部的一个 Python 类对应着一个数据库中的表单。
  - `admin.py`：这个文件中表明了以管理员方式登录网站时，可以操作的内容。

## ctfsite

Django 项目全部在该文件夹内，以下是关于该项目内容的一些解释：

### `User`

有关用户信息的数据。登录界面、用户信息界面的视图。

下表为 User 这个应用的数据库设计：

| 表名 | 属性                                                         |
| ---- | ------------------------------------------------------------ |
| User | id &rarr; int, not null, primary key, autoincrement<br />name &rarr; char(32), not null, unique<br />qq &rarr; char(16), null<br />description &rarr; char(128), not null<br />Email &rarr; char(32), null<br />belongTo_id &rarr; int, null, references "user_team" ("id") deferrable initially deferred; |
| Team | id &rarr; int, not null, primary key, autoincrement<br />name &rarr; char(32), not null, unique<br />description &rarr; char(128), not null |

### `question`

与题目相关的数据。题目相关界面的视图。

### `Post`

与公告相关的数据。公告展示、编辑公告的视图。