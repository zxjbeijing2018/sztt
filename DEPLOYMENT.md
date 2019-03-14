# 部署方案

### 安装 supervisor

 ```
 sudo apt install -y supervisor
 ```
 or
 ```
 pip install supervisor
 ```
 因为 supervisor 不支持 Python3 因此，确保 pip 版本是 Python2
 
### 配置 supervisor

安装完成后不要启动，首先创建配置文件

```
sudo vim /etc/supervisor/supervisord.conf
```
目录结构可以更改，配置文件一定要以 .conf 结尾
写入下面内容
```
; supervisor config file

[unix_http_server]
file=/var/run/supervisor.sock   ; (the path to the socket file)
chmod=0700                       ; sockef file mode (default 0700)

[supervisord]
logfile=/var/log/supervisor/supervisord.log ; (main log file;default $CWD/supervisord.log)
pidfile=/var/run/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
childlogdir=/var/log/supervisor            ; ('AUTO' child log dir, default $TEMP)

[inet_http_server]
port=0.0.0.0:9000
username=super
password=1030475


; the below section must remain in the config file for RPC
; (supervisorctl/web interface) to work, additional interfaces may be
; added by defining them in separate rpcinterface: sections
[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///var/run/supervisor.sock ; use a unix:// URL  for a unix socket

; The [include] section can just contain the "files" setting.  This
; setting can list multiple files (separated by whitespace or
; newlines).  It can also contain wildcards.  The filenames are
; interpreted as relative to this file.  Included files *cannot*
; include files themselves.

[include]
files = /etc/supervisor/conf.d/*.conf
```
其中

```[inet_http_server]```的内容是用来从 web 端管理 supervisor 如果不需要可以直接删除

```[include]``` 为管理配置文件目录

### 启动 supervisor
```
sudo supervisord -c /etc/supervisor/supervisord.conf
```
```/etc/supervisor/supervisord.conf```是配置文件所在目录

### celery 配置文件

```
sudo vim /etc/supervisor/conf.d/szttcelery.conf
```
```szttcelery.conf```文件名可以修改，但是应保存在 supervisor 配置 ```[include]``` 字段定义的路径下，并以 ```.conf```结尾

并写入下面内容
```
[program:szttcelery]
directory = /root/sztt/sztt
command = celery -A sztt worker -l info
autostart = true
startsecs = 5
autorestart = true
startretries = 3
user = root
redirect_stderr = true
stdout_logfile_maxbytes = 20MB
stdout_logfile_backups = 20
stdout_logfile = /root/logs/celery.log
```
其中

 - ```[program:szttcelery]``` szttcelery 可修改，要求唯一，supervisor以该名字作为唯一标识
 - ```directory``` 为项目路径
 - ```stdout_logfile``` 为 log file,可自行修改

### django 配置文件

```
sudo vim /etc/supervisor/conf.d/szttserver.conf
```
写入以下内容
```
[program:szttserver]
directory = /root/sztt/sztt
command = gunicorn -w 4 -b 0.0.0.0:8090 sztt.wsgi:application
autostart = true
startsecs = 5
autorestart = true
startretries = 3
user = root
redirect_stderr = true
stdout_logfile_maxbytes = 20MB
stdout_logfile_backups = 20
stdout_logfile = /root/logs/server.log
```

具体的修改和 celery 同理

### 安装 gunicorn

```
pip3 install gunicorn
```

### 启动 supervisor

```
supervisorctl
```
进入supervisor 交互shell

```
reload
```
重新载入管理配置

此时应该可以看到
```
szttcelery                       RUNNING   pid 16013, uptime 2 days, 1:52:57
szttserver                       RUNNING   pid 16086, uptime 2 days, 1:51:09
```
表示服务启动

如果在supervisor配置中启用了 ```[inet_http_server]``` 可以在 通过 ip:port 从页面端管理 supervisor