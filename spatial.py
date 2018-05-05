import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def mean_filter(x, kernel_size=3):
    result = x.copy()
    for i in range(int(kernel_size), len(x) - int(kernel_size)):
        for j in range(int(kernel_size), len(x[0]) - int(kernel_size)):
            temp = 0
            for xx in range(i - int(kernel_size / 2), i + int(kernel_size / 2) + 1):
                for y in range(j - int(kernel_size / 2), j + int(kernel_size / 2) + 1):
                    temp += x[xx][y]
            result[i][j] = temp//(kernel_size*kernel_size)
    return result

def med_filter(x, kernel_size=3):
    result = x.copy()
    for i in range(int(kernel_size), len(x) - int(kernel_size)):
        for j in range(int(kernel_size), len(x[0]) - int(kernel_size)):
            temp=[]
            for xx in range(i - int(kernel_size / 2), i + int(kernel_size / 2) + 1):
                for y in range(j - int(kernel_size / 2), j + int(kernel_size / 2) + 1):
                    temp.append(x[xx][y])
            temp.sort()
            result[i][j] = temp[kernel_size*kernel_size//2]
    return result

def modified_alpha_filter(x, d, kernel_size=3):
    result = x.copy()
    for i in range(int(kernel_size), len(x) - int(kernel_size)):
        for j in range(int(kernel_size), len(x[0]) - int(kernel_size)):
            temp=[]
            for xx in range(i - int(kernel_size / 2), i + int(kernel_size / 2) + 1):
                for y in range(j - int(kernel_size / 2), j + int(kernel_size / 2) + 1):
                    temp.append(x[xx][y])
            temp.sort()
            result[i][j] = sum(temp[d//2:kernel_size*kernel_size-d//2])//(kernel_size*kernel_size-d)
    return result

if __name__ == '__main__':
    index=0
    img = Image.open('Figure/' + str(index + 5) + '.tif')  # 500*500
    arr = np.array(img)
    new_arr = mean_filter(arr)
    new_img = Image.fromarray(new_arr)

    plt.subplot(2, 3, index * 3 + 1)
    plt.imshow(img)
    plt.title('origin figure')

    plt.subplot(2,3,index*3+2)
    plt.imshow(new_img)
    plt.title('mean filtering')

    plt.subplot(2, 3, index * 3 + 3)
    new_arr = med_filter(arr)
    new_img = Image.fromarray(new_arr)
    plt.imshow(new_img)
    plt.title('mid filtering')

    img = Image.open('Figure/' + str(6) + '.tif')  # 500*500
    arr = np.array(img)
    new_arr = modified_alpha_filter(arr,5,5)
    new_img = Image.fromarray(new_arr)
    # print(new_arr[0])

    plt.subplot(2, 3, 4)
    plt.imshow(img)
    plt.title('origin figure')

    plt.subplot(2, 3, 5)
    plt.imshow(new_img)
    plt.title('modified alpha filtering')

    plt.subplot(2, 3, 6)
    new_arr_2 = med_filter(arr)
    new_img_2 = Image.fromarray(new_arr_2)
    plt.imshow(new_img_2)
    plt.title('mid filtering')

    plt.show()