import pandas as pd
import os
import random
import numpy as np
import matplotlib.pyplot as plt

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class DataReader1:
    # 각 단어의 특성은 무시하고 발현 패턴만 봄
    # window_size만큼의 previous data, 단 한 개의 prediction value
    def __init__(self, window_size, file_names):
        self.train_X, self.train_Y, self.test_X, self.test_Y = read_data(window_size, file_names)
        self.predict_X = read_predict_set(window_size, file_names[1])

        # 데이터 읽기가 완료되었습니다.
        # 읽어온 데이터의 정보를 출력합니다.
        print("\n\nData Read Done!")
        print("Training X Size : " + str(self.train_X.shape))
        print("Training Y Size : " + str(self.train_Y.shape))
        print("Test X Size : " + str(self.test_X.shape))
        print("Test Y Size : " + str(self.test_Y.shape) + '\n\n')
        print("Predict X Size : " + str(self.predict_X.shape) + '\n\n')


class DataReader2:
    # 각 단어의 특성은 무시하고 발현 패턴만 봄
    # window_size만큼의 previous data, 단 한 개의 prediction value
    def __init__(self, window_size, file_names):
        self.train_X, self.train_Y, self.test_X, self.test_Y, self.word_list = read_data_binary(window_size, file_names)
        self.predict_X = read_predict_set_binary(window_size, file_names[1])

        # 데이터 읽기가 완료되었습니다.
        # 읽어온 데이터의 정보를 출력합니다.
        print("\n\nData Read Done!")
        print("Training X Size : " + str(self.train_X.shape))
        print("Training Y Size : " + str(self.train_Y.shape))
        print("Test X Size : " + str(self.test_X.shape))
        print("Test Y Size : " + str(self.test_Y.shape) + '\n\n')
        print("Predict X Size : " + str(self.predict_X.shape) + '\n\n')


def read_predict_set(window_size, filename):
    df = pd.read_excel(filename, index_col=0)
    array = df.to_numpy(dtype=float)
    array = np.log2(array)
    array = array / np.max(array)
    array = array[-1 * window_size:, :]
    array = array.transpose()

    return array


def read_predict_set_binary(window_size, filename):
    df = pd.read_excel(filename, index_col=0)
    array = df.to_numpy(dtype=float) > 1
    array = array.astype(float)
    array = array[-1 * window_size:, :]
    array = array.transpose()

    return array


def read_data(window_size, file_names):
    dataset = []
    for el in file_names:
        dataset += read_single_data(el, window_size)

    train_x = []
    train_y = []
    test_x = []
    test_y = []

    random.shuffle(dataset)
    for i in range(len(dataset)):
        x, y = dataset[i]
        if i < 0.85 * len(dataset):
            train_x.append(x)
            train_y.append(y)
        else:
            test_x.append(x)
            test_y.append(y)

    train_x = np.asarray(train_x)
    train_y = np.asarray(train_y)
    test_x = np.asarray(test_x)
    test_y = np.asarray(test_y)

    train_x = train_x.reshape((len(train_x), window_size, 1))
    train_y = train_y.reshape((len(train_y), 1, 1))
    test_x = test_x.reshape((len(test_x), window_size, 1))
    test_y = test_y.reshape((len(test_y), 1, 1))

    return train_x, train_y, test_x, test_y


def read_data_binary(window_size, file_names):
    dataset = []
    for el in file_names:
        set, word_list = read_single_data_binary(el, window_size)
        dataset += set

    train_x = []
    train_y = []
    test_x = []
    test_y = []

    random.shuffle(dataset)
    for i in range(len(dataset)):
        x, y = dataset[i]
        if i < 0.85 * len(dataset):
            train_x.append(x)
            train_y.append(y)
        else:
            test_x.append(x)
            test_y.append(y)

    train_x = np.asarray(train_x)
    train_y = np.asarray(train_y)
    test_x = np.asarray(test_x)
    test_y = np.asarray(test_y)

    train_x = train_x.reshape((len(train_x), window_size, 1))
    train_y = train_y.reshape((len(train_y), 1, 1))
    test_x = test_x.reshape((len(test_x), window_size, 1))
    test_y = test_y.reshape((len(test_y), 1, 1))

    return train_x, train_y, test_x, test_y, word_list


def read_single_data(filename, window_size):
    dataset = []
    df = pd.read_excel(filename, index_col=0)
    array = df.to_numpy(dtype=float) + 0.01
    array = np.log2(array)
    #array -= np.min(array)
    array = array / np.max(array)
    array = array.transpose()

    size, dim = array.shape

    if window_size > dim - 1:
        print("Please provide smaller window size")
        exit(1)

    for el in array:
        for i in range(dim - window_size):
            y = np.asarray(el[i + window_size])
            x = el[i: i + window_size]
            dataset.append([x, y])

    return dataset


def read_single_data_binary(filename, window_size):
    dataset = []
    df = pd.read_excel(filename, index_col=0)
    array = df.to_numpy(dtype=float) > 1
    array = array.astype(float)
    array = array.transpose()

    size, dim = array.shape

    if window_size > dim - 1:
        print("Please provide smaller window size")
        exit(1)

    for el in array:
        for i in range(dim - window_size):
            y = np.asarray(el[i + window_size])
            x = el[i: i + window_size]
            dataset.append([x, y])

    return dataset, list(df.keys())


def draw_graph(prediction, label, history):
    X = prediction / np.max(prediction, axis=0)
    Y = label / np.max(label, axis=0)

    minval = min(np.min(X), np.min(Y))
    maxval = max(np.max(X), np.max(Y))

    fig = plt.figure(figsize=(8, 8))
    plt.title("Regression Result")
    plt.xlabel("Ground Truth")
    plt.ylabel("AI Predict")
    plt.scatter(X, Y)
    plt.plot([minval, maxval], [minval, maxval], "red")
    fig.savefig("result.png")

    train_history = history.history["loss"]
    validation_history = history.history["val_loss"]
    fig = plt.figure(figsize=(8, 8))
    plt.title("Loss History")
    plt.xlabel("EPOCH")
    plt.ylabel("LOSS Function")
    plt.plot(train_history, "red")
    plt.plot(validation_history, 'blue')
    fig.savefig("train_history.png")
