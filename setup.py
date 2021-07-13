#!/usr/bin/python
import os
import shutil

def main():
    shutil.move('activity_tracker.service', '/etc/systemd/system/activity_tracker.service')
    os.system('sudo systemctl enable activity_tracker.service')
    os.system('sudo systemctl start activity_tracker.service')

if __name__ == '__main__':
    main()