#!/usr/bin/env python3

import yaml
import subprocess
import argparse
import time
import pycurl
from io import BytesIO

config_path = "/home/a.zhideev/rclone/rclone.conf"

with open("conf.yaml") as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

#i = 'nxs'
#f = open('rclone-new.conf', 'w')
#f.write('['+'nxs'+']'+'\n' )
#for i in config['server']['nxs']['connect']:
    #print (config['server']['nxs']['connect'][1])
#    f.write(i +'\n')
#buffer = BytesIO()
#c = pycurl.Curl()
#c.setopt(c.URL, 'https://storage.nixys.ru/remote.php/webdav/')
#c.setopt(c.WRITEDATA, buffer)
#c.perform()
#c.close()

command = 'curl --silent -u a.zhideev-tmp:Z8tfgmCjNW7ut6Y  -X PROPFIND  \'https://storage.nixys.ru/remote.php/webdav/\' | xmllint --format -'
#print(command)
subprocess.Popen(command, shell=True)
"""

def get_size(g):
    cmd = 'rclone --config '+config_path+' --dry-run size '+ g + ': > /tmp/storage-'+g+'.txt'
    return cmd

def check_size(c):
    with open('/tmp/storage-'+c+'.txt', 'r') as f:
        for line in f.readlines():
            for i, word in enumerate(line.split()):
                if i == 4:
                    used_size = (word[1:])
                    break
    f.close()
    return used_size

def sync_start(s):
    excludes = " --exclude ".join(config['server'][s]['excludes'])
    keys = " ".join(config['server'][s]['keys'])
    cmnd = 'rclone --config '+config_path+' --log-file='+ config['server'][s]['logfile_path']+ s+'-storage-sync.log --log-level ' + config['server'][s]['loglevel'] + ' sync '+ config['server'][i]['source']+ ' '+ s +':'+ config['server'][s]['destination']+' --exclude '+ excludes + ' --exclude-from '+ config['server'][s]['excludes_file']+' --bwlimit='+config['server'][s]['bandwidth'] + ' '+keys
    return cmnd

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd', help='List of commands')

    list_parser = subparsers.add_parser('ls', help='ls command')
    list_parser.add_argument('dirname', type=str, help='[Remote server name]:[Directory to list]')

    copy_parser = subparsers.add_parser('copy', help='Copy [From] [To]')
    copy_parser.add_argument('source', help='From')
    copy_parser.add_argument('destination', help='To:')

    start_parser = subparsers.add_parser('start', help='start')

    return parser.parse_args()



args = parse_args()
if args.cmd == 'ls':
    command = 'rclone --config '+config_path+' --dry-run ls ' + args.dirname
    #print(command)
    subprocess.Popen(command, shell=True)
elif args.cmd == 'copy':
    command = 'rclone --config '+config_path+' --dry-run copy ' + args.source + ' ' + args.destination
elif args.cmd == '' or 'start':
    for i in config['server']:
        total_size = get_size(i)
        time.sleep(1)
        #print (total_size)
        size = check_size(i)
        q=round(int(size)/1073741824, 2)
        r = round(q/int(config['server'][i]['storage_size'])*100, 2)
        #print(r)
        if r > int(config['server'][i]['quota']):
            print ('Quota used percents more then '+ config['server'][i]['quota']+'% (current used space: '+str(q)+'/'+config['server'][i]['storage_size']+' Gb ('+str(r)+'%)). ')
        subprocess.Popen(total_size, shell=True)
        command = sync_start(i)
        #print(command)
        subprocess.Popen(command, shell=True)
"""



#print(command)
#subprocess.Popen(command, shell=True)
