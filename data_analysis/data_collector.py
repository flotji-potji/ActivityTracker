#!/bin/var/env python3
import csv
import pandas as pd
import numpy as np


def data_collector(path='sensor_data.csv', category='all', csv_type='eng'):
    data = []
    labels = []
    splitted_row = []
    with open(path, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
        for row in csv_reader:
            if len(row) > 0:
                if 'Jän' not in row[0]:
                    if csv_type is 'eng':
                        splitted_row = row[0].split(',')
                    elif csv_type is 'ger':
                        splitted_row = row[0].split(';')
                    if category is 'all':
                        data.append([float(cell) for cell in splitted_row[:len(splitted_row) - 1]])
                    elif category is 'gyro':
                        data.append([float(cell) for cell in splitted_row[:3]])
                    elif category is 'acc':
                        data.append([float(cell) for cell in splitted_row[3:6]])
                    elif category is 'gyroacc':
                        data.append([float(cell) for cell in splitted_row[:6]])
                    labels.append(float(splitted_row[len(splitted_row) - 1]))
    return {
        'data': np.array(data),
        'target': np.array(labels),
        'frame': None,
        'target_names': np.array(['idle', 'walking', 'running'], dtype='<U10'),
        'DESCR': 'activity tracker recorded dataset',
        'feature_names': [
            'gyro_scaled_x',
            'gyro_scaled_y',
            'gyro_scaled_z',
            'acc_scaled_x',
            'acc_scaled_y',
            'acc_scaled_z',
            'rot_x',
            'rot_y'],
        'filename': path
    }


def main():
    print(data_collector('new_sensor_data.csv')['data'][:2])
    print(data_collector('new_sensor_data.csv')['target'][:2])


if __name__ == '__main__':
    main()
