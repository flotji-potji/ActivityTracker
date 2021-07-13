#!/usr/bin/python
import os
import shutil

def main():
    os.system('sudo systemctl stop activity_tracker.service')
    os.system('sudo systemctl disable activity_tracker.service')
    os.remove('/etc/systemd/system/activity_tracker.*')
    os.remove('/usr/lib/systemd/system/activity_tracker.*')
    os.system('sudo systemctl daemon-reload')
    os.system('sudo systemctl reset-failed')
    shutil.rmtree('ActivityTracker')

if __name__ == '__main__':
    main()