#!/usr/bin/env python
# coding:utf-8

from fabric.api import *
import random
import string

#脚本说明：添加删除svn和dev账号

#添加新用户前修改如下用户信息
uname="litingting"
ip="192.168.1.97"

#group="ios_admin"
group="php_admin"

##
upasswd="".join(random.sample('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#%',8))

ip1=ip.split('.')[3]

network1="""ONBOOT=yes
DEVICE=eth1:%s
TYPE=Ethernet
BOOTPROTO=static
IPADDR=%s
NETMASK=255.255.255.0
""" % (ip1, ip)

devIfg='ifcfg-eth1:%s' % ip1

devUpstream="""
upstream php_%s {
    server %s:9000;
}
""" % (uname,ip)

devPhpfpm="""
[%s]
user = %s
group = %s
listen = %s:9000
pm = static
pm.max_children = 2
pm.start_servers = 10
pm.min_spare_servers = 10
pm.max_spare_servers = 20
pm.max_requests = 0
request_slowlog_timeout = 5s
slowlog = logs/$pool.log
""" % (uname,uname,uname,ip)


env.roledefs= {'svn': ['192.168.1.15'], 'dev': ['192.168.1.8'], 'svnWaice': [''], 'svnXiaomi': ['']}
env.passwords = {'root@192.168.1.15:22': 'password', 'root@192.168.1.8:22': 'password', 'root@11.11.11.11:22': 'password', 'root@22.22.22.22:22': 'password'}

#添加用户svn账号
#@roles('svn')
def svnadd():
    with cd("/opt/svnroot/youjk/conf"):
        run('htpasswd -b web.conf "%s" "%s"' % (uname,upasswd))
        run("sed -i '/^%s/ s/$/,%s/' authz" % (group, uname))
        run('/etc/init.d/httpd restart')
		
	print "用户名: %s" % uname
	print "密码: %s" % upasswd

#外测添加svn
@roles('svnWaice')
def svn_waiceadd():
    with cd("/data/app/subversion/youjuke/conf"):
        run('htpasswd -b web.conf "%s" "%s"' % (uname,upasswd))
        run("sed -i '/^%s/ s/$/,%s/' authz" % (group, uname))
        run('/etc/init.d/httpd restart')
	
	print "用户名: %s" % uname
	print "密码: %s" % upasswd

#小米装添加svn
@roles('svnXiaomi')
def svn_xiaomiadd():
    with cd("/opt/svn/xiaomi/conf"):
        run('htpasswd -b web.conf "%s" "%s"' % (uname,upasswd))
        run("echo '%s=rw' >> authz" % (uname))
        run('/etc/init.d/httpd restart')
	
	print "用户名: %s" % uname
	print "密码: %s" % upasswd


#删除用户svn账号
@roles('svn')
def svndel():
    with cd("/opt/svnroot/youjk/conf"):
        run("sed -i '/^%s*/d' web.conf" % (uname))
        run("sed -i 's/,%s//' authz" % (uname))
        run('/etc/init.d/httpd restart')
		
	print "svn删除成功"

#删除外侧svn账号
@roles('svnWaice')
def svn_waicedel():
    with cd("/data/app/subversion/youjuke/conf"):
        run("sed -i '/^%s*/d' web.conf" % (uname))
        run("sed -i 's/,%s//' authz" % (uname))
        run('/etc/init.d/httpd restart')

	print "外侧svn账号删除成功" 

#删除小米装svn
@roles('svnXiaomi')
def svn_xiaomidel():
    with cd("/opt/svn/xiaomi/conf"):
        run("sed -i '/^%s*/d' web.conf" % (uname))
        run("sed -i '/^%s*/d' authz" % (uname))
        run('/etc/init.d/httpd restart')

	print "小米装svn账号删除成功" 


#添加smb用户，配置开发环境
@roles('dev')
def devadd():
    with cd("/etc/sysconfig/network-scripts"):
        run("echo '%s' > '%s'" % (network1, devIfg))
    run('useradd %s' % uname)
    run("echo -e '%s\n%s' | smbpasswd -a %s -s" % (upasswd,upasswd,uname))
    with cd("/usr/local/nginx/conf"):
        run("echo '%s' >> 'upstream.conf'" % devUpstream)
    with cd('/usr/local/nginx/conf/http-vhost'):
        run("cp yangkexuan.conf %s.conf" % uname)
        run("sed -i 's/yangkexuan/%s/g' %s.conf" % (uname,uname))
        run("sed -i 's/192.168.1.59/%s/g' %s.conf" % (ip,uname))
    with cd('/usr/local/nginx/conf/https-vhost'):
        run("cp yangkexuan.conf %s.conf" % uname)
        run("sed -i 's/yangkexuan/%s/g' %s.conf" % (uname,uname))
        run("sed -i 's/192.168.1.59/%s/g' %s.conf" % (ip,uname))
    with cd('/usr/local/php/etc'):
        run("echo '%s' >> 'php-fpm.conf'" % devPhpfpm)
    run('chmod +x /home/%s' % uname)
    run('mkdir /home/%s/logs' % uname)
    run('/etc/init.d/network restart')
    run('/etc/init.d/smb restart')
    run('/etc/init.d/php-fpm restart')
    run('/etc/init.d/nginx restart')

    print "开发环境账号"
    print "账号： %s" % uname
    print "密码： %s" % upasswd
    print "服务器地址： %s" % ip


#删除开发环境账号
@roles('dev')
def devdel():
	with cd("/etc/sysconfig/network-scripts"):
		run("rm -f '%s'" % (devIfg))
	with cd("/usr/local/nginx/conf"):
		run("sed -i '/^upstream php_%s/,/^}$/d' upstream.conf" % (uname))
	with cd('/usr/local/nginx/conf/http-vhost'):
		run("mv %s.conf old/%s.conf.del" % (uname, uname))
	with cd('/usr/local/nginx/conf/https-vhost'):
		run("mv %s.conf old/%s.conf.del" % (uname, uname))
	with cd('/usr/local/php/etc'):
		n1=run("sed -n -e '/\[%s\]/=' php-fpm.conf" % (uname))
		n2=int(n1) + 11
		run("sed -i '%s,%sd' php-fpm.conf" % (n1,n2))
	run("smbpasswd -x %s" % uname)
	run('/etc/init.d/smb restart')
	run('/etc/init.d/network restart')
	run('/etc/init.d/php-fpm restart')
	run('/etc/init.d/nginx restart')
	run("userdel %s" % uname)
	
	print "%s删除成功" % uname

@task
def addall():
#    execute(svnadd)
    execute(svn_waiceadd)
#    execute(svn_xiaomiadd)
#    execute(svndel)
#    execute(svn_waicedel)
#    execute(svn_xiaomidel)
#    execute(devadd)
#    execute(devdel)
