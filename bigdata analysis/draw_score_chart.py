import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d
import os

score_xlsx = 'ai_score.xlsx'
fig_dir = 'ai_scores'

if fig_dir not in os.listdir():
    os.mkdir(fig_dir)

df = pd.read_excel(score_xlsx, index_col=0).T

word_list = df.keys()


def chart(df, word, dir):
    fig, ax = plt.subplots(figsize=(3, 3))
    score = int(df[word])
    ax.pie([100 - score, score], wedgeprops={'width': 0.4}, startangle=90, colors=['#D3D3D3', '#7af6fd'])
    if score > 0:
        plt.text(0, -0.06, str(score), ha='center', va='center', fontsize=45)
    else:
        plt.text(0, -0.06, "?", ha='center', va='center', fontsize=45)

    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)

    plt.savefig("test.png", bbox_inches='tight')
    plt.savefig(dir + "/" + word + ".png", bbox_inches='tight')
    plt.close()


def draw_estimate(df1, df2, word, dir):
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    alpha = 0.1

    y = df1[word].copy()
    x = [i + 1 for i in range(len(y))]
    err = 1 - ((max(y) - y) / max(y)) ** 2

    y2 = df2[word].copy()
    x2 = [i + 1 for i in range(len(y2))]
    err2 = 1 - ((max(y2) - y2) / max(y2)) ** 2

    ax[0].plot(x, y, color="black", alpha=0.25)
    ax[1].plot(x2, y2, color="black", alpha=0.25)

    sigma = 0.8
    upper = gaussian_filter1d(y + err, sigma=sigma)
    ax[0].fill_between(x, upper, upper * 0, facecolor="red", alpha=alpha)

    upper2 = gaussian_filter1d(y2 + err2, sigma=sigma)
    ax[1].fill_between(x2, upper2, upper2 * 0, facecolor="green", alpha=alpha)

    sigma = 1
    upper = gaussian_filter1d(y + err, sigma=sigma)
    ax[0].fill_between(x, upper, upper * 0, facecolor="red", alpha=alpha * 2)

    upper2 = gaussian_filter1d(y2 + err2, sigma=sigma)
    ax[1].fill_between(x2, upper2, upper2 * 0, facecolor="green", alpha=alpha)

    sigma = 1.5
    upper = gaussian_filter1d(y + err, sigma=sigma)
    ax[0].fill_between(x, upper, upper * 0, facecolor="red", alpha=alpha)

    upper2 = gaussian_filter1d(y2 + err2, sigma=sigma)
    ax[1].fill_between(x2, upper2, upper2 * 0, facecolor="green", alpha=alpha)

    sigma = 2
    upper = gaussian_filter1d(y + err, sigma=sigma)
    ax[0].fill_between(x, upper, upper * 0, facecolor="red", alpha=alpha)

    upper2 = gaussian_filter1d(y2 + err2, sigma=sigma)
    ax[1].fill_between(x2, upper2, upper2 * 0, facecolor="green", alpha=alpha)

    ax[0].axes.xaxis.set_visible(False)
    ax[0].axes.yaxis.set_visible(False)
    ax[1].axes.xaxis.set_visible(False)
    ax[1].axes.yaxis.set_visible(False)

    plt.savefig(dir + "/" + word + ".png", bbox_inches='tight')
    plt.close()


for word in word_list:
    chart(df, word, fig_dir)
