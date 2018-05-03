from PIL import Image
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

DEBUG = False


def filter_func():
    def arith_mean(origin, i, j, kernel_size=3):
        temp = 0
        for x in range(i - int(kernel_size / 2), i + int(kernel_size / 2) + 1):
            for y in range(j - int(kernel_size / 2), j + int(kernel_size / 2) + 1):
                temp += origin[x, y]
        return int(temp / (kernel_size * kernel_size))

    def mean_filter(x, kernel_size=3):
        result = x.copy()
        for i in range(int(kernel_size), len(x) - int(kernel_size)):
            for j in range(int(kernel_size), len(x[0]) - int(kernel_size)):
                result[i][j] = arith_mean(x, i, j, kernel_size)
        return result

    def geo_filter(x, kernel_size=3):
        result = x.copy()
        for i in range(int(kernel_size), len(x) - int(kernel_size)):
            for j in range(int(kernel_size), len(x[0]) - int(kernel_size)):
                temp = float(x[i][j])
                for xx in range(i - int(kernel_size / 2), i + int(kernel_size / 2) + 1):
                    for y in range(j - int(kernel_size / 2), j + int(kernel_size / 2) + 1):
                        if xx != i or y != j:
                            temp *= x[xx, y]
                result[i][j] = int(temp ** (1 / kernel_size ** 2))
        return result

    def harmonic_filter(x, kernel_size=3):
        result = x.copy()
        for i in range(int(kernel_size), len(x) - int(kernel_size)):
            for j in range(int(kernel_size), len(x[0]) - int(kernel_size)):
                temp = 0
                flag = False
                for xx in range(i - int(kernel_size / 2), i + int(kernel_size / 2) + 1):
                    for y in range(j - int(kernel_size / 2), j + int(kernel_size / 2) + 1):
                        if x[xx, y]:
                            temp += 1 / x[xx, y]
                        else:
                            temp = 0
                            flag = True
                            break
                    if flag:
                        break
                result[i][j] = 0 if temp == 0 else kernel_size * kernel_size / temp
        return result

    def inverse_harmonic_filter_4(x, kernel_size=3):
        Q = 1.5
        result = x.copy()
        for i in range(int(kernel_size), len(x) - int(kernel_size)):
            for j in range(int(kernel_size), len(x[0]) - int(kernel_size)):
                numerator = 0
                denominator = 0
                for xx in range(i - int(kernel_size / 2), i + int(kernel_size / 2) + 1):
                    for y in range(j - int(kernel_size / 2), j + int(kernel_size / 2) + 1):
                        numerator += x[xx, y] ** (Q + 1)
                        denominator += x[xx, y] ** Q
                result[i][j] = 0 if denominator == 0 else numerator / denominator
        return result

    def inverse_harmonic_filter_5(x, kernel_size=3):
        Q = -1.5
        result = x.copy()
        for i in range(int(kernel_size), len(x) - int(kernel_size)):
            for j in range(int(kernel_size), len(x[0]) - int(kernel_size)):
                numerator = 0
                denominator = 0
                for xx in range(i - int(kernel_size / 2), i + int(kernel_size / 2) + 1):
                    for y in range(j - int(kernel_size / 2), j + int(kernel_size / 2) + 1):
                        if x[xx, y]:
                            numerator += x[xx, y] ** (Q + 1)
                            denominator += x[xx, y] ** Q
                if (denominator) > 10 ** (-9):
                    result[i][j] = int(numerator / denominator)
                else:
                    result[i][j] = 0
        return result

    def max_filter(x, kernel_size=3):
        result = x.copy()
        for i in range(int(kernel_size), len(x) - int(kernel_size)):
            for j in range(int(kernel_size), len(x[0]) - int(kernel_size)):
                temp = x[i, j]
                for xx in range(i - int(kernel_size / 2), i + int(kernel_size / 2) + 1):
                    for y in range(j - int(kernel_size / 2), j + int(kernel_size / 2) + 1):
                        if x[xx, y] > temp:
                            temp = x[xx, y]
                result[i][j] = temp
        return result

    def min_filter(x, kernel_size=3):
        result = x.copy()
        for i in range(int(kernel_size), len(x) - int(kernel_size)):
            for j in range(int(kernel_size), len(x[0]) - int(kernel_size)):
                temp = x[i, j]
                for xx in range(i - int(kernel_size / 2), i + int(kernel_size / 2) + 1):
                    for y in range(j - int(kernel_size / 2), j + int(kernel_size / 2) + 1):
                        if x[xx,y]==255:
                            pass
                        if x[xx, y] < temp:
                            temp = x[xx, y]
                result[i][j] = temp
        return result

    def mid_filter(x, kernel_size=3):
        result = x.copy()
        for i in range(int(kernel_size), len(x) - int(kernel_size)):
            for j in range(int(kernel_size), len(x[0]) - int(kernel_size)):
                maxnow = int(x[i, j])
                minnow = int(x[i, j])
                for xx in range(i - int(kernel_size / 2), i + int(kernel_size / 2) + 1):
                    for y in range(j - int(kernel_size / 2), j + int(kernel_size / 2) + 1):
                        if x[xx, y] < minnow:
                            minnow = x[xx, y]
                        if x[xx, y] > maxnow:
                            maxnow = x[xx, y]
                result[i][j] = int((maxnow + minnow) / 2)
        return result
    if DEBUG:
        return [min_filter]
    else:
        return [mean_filter, geo_filter, harmonic_filter, inverse_harmonic_filter_4, inverse_harmonic_filter_5,
                signal.medfilt2d, max_filter, min_filter, mid_filter]

arr = np.ones((250, 250), dtype=np.uint8) * 0
for i in range(1, 10):
    arr[20:230, 25 * i:25 * i + 7] = np.uint8(255)

img_filters = filter_func()

if DEBUG:
    img_filters = img_filters[-1:]

result = []
kernel_sizes = [3, 5, 9]
count=1

for i, img_filter in enumerate(img_filters):
    result.append([])
    for kernel_size in kernel_sizes:
        img = Image.fromarray(img_filter(arr, kernel_size))
        plt.subplot(int((len(img_filters)+1)/2), len(kernel_sizes*2), count)
        plt.title((img_filter.__name__[:-7], kernel_size))
        plt.xticks([])
        plt.yticks([])
        plt.imshow(img)
        count+=1
plt.show()
