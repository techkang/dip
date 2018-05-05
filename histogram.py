# -*- encoding:utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

for index in range(4):
    img = Image.open('Figure/'+str(index+1)+'.tif')  # 500*500
    arr = np.array(img)
    new_arr = arr.copy()
    counts = np.zeros(256)
    s = np.zeros(256, dtype=np.uint8)
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            counts[arr[i][j]] += 1
    sigma = 0
    for i in range(256):
        sigma += counts[i]
        s[i] = np.uint8(255 * sigma / (len(arr) * len(arr[0])))
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            new_arr[i][j] = s[arr[i][j]]
    new_img = Image.fromarray(new_arr)
    plt.subplot(4, 4, index * 4+1)
    plt.imshow(img)
    plt.axis('off')
    if not index:
        plt.title('origin picture')
    plt.subplot(4, 4, index * 4 + 2)
    plt.imshow(new_img)
    plt.axis('off')
    if not index:
        plt.title('after histogram equalization')
    plt.subplot(4,4,index*4+3)
    for i,count in enumerate(counts):
        plt.plot((i,i),(0,count),'-',lw=0.2,color='black')
    if not index:
        plt.title('histogram of origin picture')
    plt.subplot(4,4,index*4+4)
    plt.plot(range(256),s)
    if not index:
        plt.title('histogram transform equation')
plt.show()