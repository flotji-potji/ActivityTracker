#!/usr/bin/env python3
import os
import shutil


def main():
    shutil.move('/home/pi/ActivityTracker/at_measure.service', '/etc/systemd/system/at_measure.service')
    shutil.move('/home/pi/ActivityTracker/delete_all.py', '/home/pi/delete_all.py')
    shutil.move('/home/pi/ActivityTracker/gyro.py', '/usr/local/bin/gyro.py')
    os.system('sudo chmod 744 /usr/local/bin/gyro.py')
    os.system('sudo chmod 644 /etc/systemd/system/at_measure.service')
    os.system('sudo systemctl enable at_measure.service')
    os.system('sudo systemctl start at_measure.service')


if __name__ == '__main__':
    main()
