#!/usr/bin/env python3

import yaml
import subprocess
import argparse
import pycurl
from io import BytesIO
import xml.etree.ElementTree as ET
import os
import base64



config_path = "/home/a.zhideev/rclone/rclone.conf"

with open("conf.yaml") as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)



#
#print(command)


#for child in o.response('d:href'):
#    print (child.tag, child.attrib)
#print(out)
s = 'nxs'
def get_user(s):
    for i in config['server'][s]['connect']:
        if i[:4] == 'pass':
            q=i.split()[2]
            continue
        if i[:4] == 'user':
            r=i.split()[2]
            continue
    return(r,q)
t = get_user(s)
command = "curl --silent -u " + t[0] +':'+ t[1]+"  -X PROPFIND  \'https://storage.nixys.ru/remote.php/webdav/\' | xmllint --format --xpath getlastmodified -"

print(command)
p = subprocess.Popen(command, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
o = ET.fromstring(out)
print (out)
"""
def get_pass (s):
    command = 'rclone obscure '+ str(s)
    p = subprocess.run(command, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.decode('utf-8')
    print ('pass hashed')
    return (out)

def create_conf(s):
    f = open('rclone-new.conf', 'w')
    f.write('['+s+']'+'\n' )
    for i in config['server'][s]['connect']:
        if i[:4] == 'pass':
            q=i.split()[2]
            f.write('pass = '+ get_pass(q) +'\n')
            continue
        f.write(i +'\n')
    f.close()
    print ('config file created')
    return ()

def sync_start(s):
    excludes = " --exclude ".join(config['server'][s]['excludes'])
    keys = " ".join(config['server'][s]['keys'])
    cmd = 'rclone --config rclone-new.conf --log-file='+ config['server'][s]['logfile_path']+ s+'-storage-sync.log --log-level ' + config['server'][s]['loglevel'] + ' sync '+ config['server'][s]['source']+ ' '+ s +':'+ config['server'][s]['destination']+' --exclude '+ excludes + ' --exclude-from '+ config['server'][s]['excludes_file']+' --bwlimit='+config['server'][s]['bandwidth'] + ' '+keys
    return cmd

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd', help='List of commands')

    list_parser = subparsers.add_parser('ls', help='ls command')
    list_parser.add_argument('servername', type=str, help='Remote server name')
    list_parser.add_argument('dirname', type=str, help='Directory to list, / for root')

    copy_parser = subparsers.add_parser('copy', help='Copy [From] [To]')
    copy_parser.add_argument('source', help='From')
    copy_parser.add_argument('destination', help='To:')

    start_parser = subparsers.add_parser('start', help='start')
    start_parser.add_argument('servername', type=str, help='Remote server name')

    return parser.parse_args()

with open("conf.yaml") as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

for l in config['server']:
    #print (l)
    size = check_size(l)
    #print (size)
    q=round(int(size)/1073741824, 2)
    r = round(q/int(config['server'][l]['storage_size'])*100, 2)
    #print(r)
    if r > int(config['server'][l]['quota']):
        print ('Quota used percents more then '+ config['server'][l]['quota']+'% (current used space: '+str(q)+'/'+config['server'][l]['storage_size']+' Gb ('+str(r)+'%)). ')

args = parse_args()
if args.cmd == 'ls':
    if args.dirname[:1] == '/':
        print ('cut')
        args.dirname = args.dirname[1:]
        print (args.dirname)
    command = 'rclone --config '+config_path+' --dry-run ls ' + args.servername+ ':'+args.dirname
    subprocess.Popen(command, shell=True)
elif args.cmd == 'copy':
    command = 'rclone --config '+config_path+' --dry-run copy ' + args.source + ' ' + args.destination
elif args.cmd == '' or 'start':
    for i in config['server']:
        total_size = get_size(i)
        #print (total_size)
        subprocess.Popen(total_size, shell=True)
        command = sync_start(i)
        #print(command)
        subprocess.Popen(command, shell=True)



#print(command)
#subprocess.Popen(command, shell=True)
"""