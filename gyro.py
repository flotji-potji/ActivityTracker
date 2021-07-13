#!/usr/bin/python
import smbus2 as smbus
import math
from gpiozero import Button, LED
from time import sleep
import os

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
i2c_address = 0x68
bus = smbus.SMBus(1)

# Buttons and LEDs
idle_button = Button(14)
walking_button = Button(15)
running_button = Button(18)
idle_led = LED(22)
walking_led = LED(27)
running_led = LED(17)

# target vector labels
IDLE_STATE_LABEL = '0'
WALKING_STATE_LABEL = '1'
RUNNING_STATE_LABEL = '2'


def read_byte(reg):
    return bus.read_byte_data(i2c_address, reg)


def read_word(reg):
    h = bus.read_byte_data(i2c_address, reg)
    l = bus.read_byte_data(i2c_address, reg + 1)
    value = (h << 8) + l
    return value


def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


def get_sensor_data():
    gyro_x = read_word_2c(0x43)
    gyro_y = read_word_2c(0x45)
    gyro_z = read_word_2c(0x47)
    gyro_x_scaled = gyro_x / 131
    gyro_y_scaled = gyro_y / 131
    gyro_z_scaled = gyro_z / 131

    acc_x = read_word_2c(0x3b)  # acc = acceleration
    acc_y = read_word_2c(0x3d)
    acc_z = read_word_2c(0x3f)
    acc_x_scaled = acc_x / 16384.0
    acc_y_scaled = acc_y / 16384.0
    acc_z_scaled = acc_z / 16384.0

    rot_x = get_x_rotation(acc_x_scaled, acc_y_scaled, acc_z_scaled)
    rot_y = get_y_rotation(acc_x_scaled, acc_y_scaled, acc_z_scaled)

    return (gyro_x_scaled, gyro_y_scaled, gyro_z_scaled, acc_x_scaled, acc_y_scaled, acc_z_scaled, rot_x, rot_y)


def store_sensor_data(data, label):
    with open('data/sensor_data.csv', 'w') as outfile:
        for row in data:
            for column in row:
                print(f'{column},', file=outfile, end='')
            print(label, file=outfile)


def collect_data(time=10,frequency=100):
    res = []
    for _ in range(frequency * time):
        res.append(get_sensor_data())
        sleep(1/frequency)
    return res


def idle_pressed():
    store_sensor_data(collect_data(), IDLE_STATE_LABEL)


def walking_pressed():
    store_sensor_data(collect_data(), WALKING_STATE_LABEL)


def running_pressed():
    store_sensor_data(collect_data(), RUNNING_STATE_LABEL)


def main():
    # activate module to communicate with it
    bus.write_byte_data(i2c_address, power_mgmt_1, 0)

    new_path = r'data'
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    while True:
        if idle_button.is_pressed:
            idle_pressed()
            break
        elif walking_button.is_pressed:
            walking_pressed()
            break
        elif running_button.is_pressed:
            running_pressed()
            break


if __name__ == '__main__':
    main()
