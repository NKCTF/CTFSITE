#!/bin/sh

cd `cd $(dirname $0); pwd -P`

# TODO: 允许 www-data 用户在当前目录下创建文件
# TODO: www-data 用户需要建立 sock 文件
chmod a+w .

uwsgi --ini uwsgi.ini &