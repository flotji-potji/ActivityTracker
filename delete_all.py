#!/usr/bin/env python3
import os
import shutil


def main():
    os.system('sudo systemctl stop at_measure.service')
    os.system('sudo systemctl disable at_measure.service')
    if os.path.exists('/etc/systemd/system/at_measure.service'):
        os.remove('/etc/systemd/system/at_measure.service')
    if os.path.exists('/usr/lib/systemd/system/at_measure.service'):
        os.remove('/usr/lib/systemd/system/at_measure.service')
    os.system('sudo systemctl daemon-reload')
    os.system('sudo systemctl reset-failed')
    shutil.rmtree('ActivityTracker')


if __name__ == '__main__':
    main()
