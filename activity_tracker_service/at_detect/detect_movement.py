#!/usr/bin/env python3
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from joblib import load
from gyro import collect_data
import numpy as np
import time

knn = load('/home/pi/ActivityTracker/knn_model.joblib')
mlp = load('/home/pi/ActivityTracker/mlp_model.joblib')


def detect_movement():
    X = np.array(collect_data())
    target_names = ['idle', 'walking', 'running']

    print("starting predicting knn model...")
    tic = time.perf_counter()
    y_knn = knn.predict(X)
    toc = time.perf_counter()
    print(f'finished in {toc - tic:0.4f} seconds')

    print("starting predicting mlp model...")
    tic = time.perf_counter()
    y_mlp = mlp.predict(X)
    toc = time.perf_counter()
    print(f'finished in {toc - tic:0.4f} seconds')

    print("Sample counts per class KNN:\n",
          {n: v for n, v in zip(target_names, np.bincount(y_knn))})

    print("Sample counts per class MLP:\n",
          {n: v for n, v in zip(target_names, np.bincount(y_mlp))})


def main():
    detect_movement()


if __name__ == '__main__':
    main()
