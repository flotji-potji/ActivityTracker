#!/usr/bin/python
import os
import shutil

def main():
    shutil.move('/home/pi/ActivityTracker/activity_tracker.service', '/etc/systemd/system/activity_tracker.service')
    shutil.move('/home/pi/ActivityTracker/delete_activity_tracker.py', '/home/pi/delete_activity_tracker.py')
    os.system('sudo systemctl enable activity_tracker.service')
    os.system('sudo systemctl start activity_tracker.service')

if __name__ == '__main__':
    main()