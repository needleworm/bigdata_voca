import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d
import os
import numpy as np
from PIL import Image

score_xlsx = 'ai_score.xlsx'
fig_dir = 'ai_scores'

sunung_xlsx = "sunung.xlsx"
pgw_xlsx = "pgw.xlsx"
fig_dir_2 = "sunung_figures"
fig_dir_3 = "pgw_figures"

if fig_dir not in os.listdir():
    os.mkdir(fig_dir)

if fig_dir_2 not in os.listdir():
    os.mkdir(fig_dir_2)

if fig_dir_3 not in os.listdir():
    os.mkdir(fig_dir_3)

data_score = pd.read_excel(score_xlsx, index_col=0).T
data_sn = pd.read_excel(sunung_xlsx, index_col=0)
data_pgw = pd.read_excel(pgw_xlsx, index_col=0)

word_list = data_score.keys()


def chart(df, word, dir):
    fig, ax = plt.subplots(figsize=(3, 3))
    score = int(df[word])
    ax.pie([100 - score, score], wedgeprops={'width': 0.4}, startangle=90, colors=['#D3D3D3', '#80FFFF'])
    if score > 0:
        plt.text(0, -0.06, str(score), ha='center', va='center', fontsize=45, color="#00FFFF")
    else:
        plt.text(0, -0.06, "?", ha='center', va='center', fontsize=45)

    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    plt.axis('off'), plt.xticks([]), plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)

    fig.canvas.draw()
    cnv = np.array(fig.canvas.renderer._renderer)
    cnv = cnv[60:540, 60:540]

    img = Image.fromarray(cnv, "RGBA").convert('CMYK')
    img.save(dir + "/" + word + ".jpg")
    img.close()

    plt.close()


def draw_estimate(df1,word, dir):
    fig, ax = plt.subplots(figsize=(3, 2))

    alpha = 0.1

    y = df1[word].copy()
    x = [i + 1 for i in range(len(y))]
    err = 1 - ((max(y) - y) / max(y)) ** 2

    ax.plot(x, y, color="black", alpha=0.25, linewidth="0.5")

    sigma = 0.8
    upper = gaussian_filter1d(y + err, sigma=sigma)
    ax.fill_between(x, upper, upper * 0, facecolor="cyan", alpha=alpha)

    sigma = 1
    upper = gaussian_filter1d(y + err, sigma=sigma)
    ax.fill_between(x, upper, upper * 0, facecolor="cyan", alpha=alpha * 2)

    sigma = 1.5
    upper = gaussian_filter1d(y + err, sigma=sigma)
    ax.fill_between(x, upper, upper * 0, facecolor="cyan", alpha=alpha)

    sigma = 2
    upper = gaussian_filter1d(y + err, sigma=sigma)
    ax.fill_between(x, upper, upper * 0, facecolor="cyan", alpha=alpha)

    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)

    fig.canvas.draw()
    cnv = np.array(fig.canvas.renderer._renderer)
    cnv = cnv[50:400-50, 76:600 - 76]

    img = Image.fromarray(cnv, "RGBA").convert('CMYK')
    img.save(dir + "/" + word + ".jpg")
    img.close()

    plt.close()


for word in word_list:
    chart(data_score, word, fig_dir)
    #draw_estimate(data_sn, word, fig_dir_2)
    #draw_estimate(data_pgw, word, fig_dir_3)

