#!/usr/bin/env python3
import os
import shutil

def main():
    shutil.move('/home/pi/ActivityTracker/activity_tracker.service', '/etc/systemd/system/activity_tracker.service')
    shutil.move('/home/pi/ActivityTracker/delete_activity_tracker.py', '/home/pi/delete_activity_tracker.py')
    shutil.move('/home/pi/ActivityTracker/gyro.py', '/usr/local/bin/gyro.py')
    os.system('sudo chmod 744 /usr/local/bin/gyro.py')
    os.system('sudo chmod 644 /etc/systemd/system/activity_tracker.service')
    os.system('sudo systemctl enable activity_tracker.service')
    os.system('sudo systemctl start activity_tracker.service')

if __name__ == '__main__':
    main()