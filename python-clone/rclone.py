#!/usr/bin/env python3

import yaml
import subprocess
import argparse

config_path = "/home/a.zhideev/rclone/rclone.conf"
logfile_path = "/home/a.zhideev/rclone/log"
with open("conf.yaml") as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

excludes = " --exclude ".join(config['options']['excludes'])
keys = " ".join(config['options']['keys'])

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd', help='list of commands')

    list_parser = subparsers.add_parser('ls', help='ls command')
    list_parser.add_argument('dirname', type=str, help='Directory to list')

    size_parser = subparsers.add_parser('size', help='directory size')
    size_parser.add_argument('dirname', type=str, help='Directory to list')

    restore_parser = subparsers.add_parser('restore', help='restore')
    restore_parser.add_argument('source', help='from')
    restore_parser.add_argument('destination', help='to:')

    start_parser = subparsers.add_parser('start', help='start')

    return parser.parse_args()

args = parse_args()

if args.cmd == 'ls':
    command = 'rclone --config '+config_path+' --log-file='+logfile_path+' --log-level DEBUG --dry-run ls '+ 'nxs:'+ args.dirname
elif args.cmd == 'size':
    command = 'rclone --config '+config_path+' --log-file='+logfile_path+' --log-level DEBUG --dry-run size '+ 'nxs:'+ args.dirname
elif args.cmd == 'restore':
    command = 'rclone --config '+config_path+' --log-file='+logfile_path+' --log-level DEBUG --dry-run copy ' + 'nxs:'+ args.source + ' ' + args.destination
elif args.cmd == 'start':
    command = 'rclone --config '+config_path+' --log-file='+logfile_path+' --log-level DEBUG '+ config['options']['type']+ ' '+ config['options']['source']+' nxs:'+ config['options']['destination']+' --exclude '+ excludes + ' --exclude-from '+ config['options']['excludes_file']+' --bwlimit='+config['options']['bandwidth'] + ' '+keys
else:
    command = 'rclone --config '+config_path+' --log-file='+logfile_path+' --log-level DEBUG --dry-run '+ config['options']['type']+ ' '+ config['options']['source']+' --exclude '+ excludes + ' --exclude-from '+ config['options']['excludes_file']+' --bwlimit='+config['options']['bandwidth'] + ' '+keys+ ' nxs:'+ config['options']['destination']


print(command)
subprocess.Popen(command, shell=True)