import cv2
import numpy as np
import shutil

path =      "C:\PokeCon\Poke-Controller-Modified\SerialController\Captures\\"
path_072 =  "C:\PokeCon\Poke-Controller-Modified\SerialController\Captures\d072\\"
path_129 =  "C:\PokeCon\Poke-Controller-Modified\SerialController\Captures\d129\\"
path_349 =  "C:\PokeCon\Poke-Controller-Modified\SerialController\Captures\d349\\"

x = 204
y = 778

for i in range(0, 2):
    file = path + str(i) + '.png'
    bgr_array = cv2.imread(file)

    if bgr_array is not None:
        print(i)
        print(bgr_array[x, y,:])
