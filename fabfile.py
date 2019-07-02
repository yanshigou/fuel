# -*- coding: utf-8 -*-

from datetime import datetime
from fabric.api import *
from fabvenv import virtualenv

# 登录用户和主机名：
env.user = 'root'
env.password = 'Dzt1234567'
env.hosts = ['47.106.174.128']
pack_name = 'deploypack_fuel.tar.gz'


def pack():
    ' 定义一个pack任务 '
    # 打一个tar包：
    local('del  %s' % pack_name)
    local('md  ..\pack_tmp')
    local('xcopy /e /s .\* ..\pack_tmp')
    # --exclude *.tar.gz
    with lcd('..\pack_tmp'):
        local('tar -czvf ../fuel/%s --exclude *.pyc --exclude fabfile.py --exclude 00* --exclude *.tar.gz ./*'
              % pack_name)
    local('rd /s /q  ..\pack_tmp')


def deploy():
    ' 定义一个部署任务 '
    # 远程服务器的临时文件：
    tag = datetime.now().strftime('%y.%m.%d_%H.%M.%S')
    print(env.host)
    hosttag = ''
    remote_work_dir = ''
    if env.host == '47.106.174.128':
        remote_work_dir = '/root/www/fuel/'
        hosttag = 'mx'
    else:
        exit(1)

    remote_tmp_tar = '/tmp/%s' % pack_name
    run('rm -f %s' % remote_tmp_tar)
    # 上传tar文件至远程服务器：
    put(pack_name, remote_tmp_tar)
    # 备份远程服务器工程
    # back_tar_name = '/home/ubuntu/www/backup/Lock%s.tar.gz' % tag
    # run('tar -czvf %s /home/ubuntu/www/Lock/*' % back_tar_name)
    # 删除原有工程
    # run('rm -rf /home/ubuntu/www/Lock/*')
    # 解压：
    run('tar -xzvf %s -C %s' % (remote_tmp_tar, remote_work_dir))
    run('mv %sother/settings_%s.py %sfuel/settings.py' % (remote_work_dir, hosttag, remote_work_dir))
    run('mv %sother/fuel_nginx_%s.conf %sfuel_nginx.conf' % (remote_work_dir, hosttag, remote_work_dir))
    run('mv %sother/fuel_uwsgi_%s.ini %sfuel_uwsgi.ini' % (remote_work_dir, hosttag, remote_work_dir))
    run('mv %sother/uwsgi_params_%s %suwsgi_params' % (remote_work_dir, hosttag, remote_work_dir))
    run('rm -rf %sother' % remote_work_dir)
    with cd(remote_work_dir):
        if env.host == '47.106.174.128':
            with virtualenv('/root/www/fuel/kkwork'):
                run('python manage.py makemigrations')
                run('python manage.py migrate')
                run('chmod a+x ./restart.sh')
                run('sh ./restart.sh', pty=False)
                run('sudo service nginx restart')
                run('sleep 5')
        else:
            run('python manage.py makemigrations')
            run('python manage.py migrate')
            run('chmod a+x ./restart.sh')
            run('sh ./restart.sh', pty=False)
            run('sudo service nginx restart')
            run('sleep 5')


