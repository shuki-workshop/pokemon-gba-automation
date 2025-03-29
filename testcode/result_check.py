import cv2
import numpy as np
import shutil

path =      "C:\PokeCon\Poke-Controller-Modified\SerialController\Captures\\"
path_072 =  "C:\PokeCon\Poke-Controller-Modified\SerialController\Captures\d072\\"
path_129 =  "C:\PokeCon\Poke-Controller-Modified\SerialController\Captures\d129\\"
path_349 =  "C:\PokeCon\Poke-Controller-Modified\SerialController\Captures\d349\\"

x = 204
y = 778

start = 0
end = 99999

for i in range(start, end):
    file = path + str(i) + '.png'
    bgr_array = cv2.imread(file)

    
    if bgr_array is not None:
        if bgr_array[x, y, 2] >= 190 and bgr_array[x, y, 1] <= 90 and bgr_array[x, y, 0] <= 40:
            shutil.move(file, path_129)
        elif bgr_array[x, y, 2] <= 60 and bgr_array[x, y, 1] >= 120 and bgr_array[x, y, 0] >= 170:
            shutil.move(file, path_072)
        elif bgr_array[x, y, 2] >= 130 and bgr_array[x, y, 1] >= 130 and bgr_array[x, y, 0] <= 130:
            shutil.move(file, path_349)