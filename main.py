from moviepy import VideoFileClip
from PIL import Image, ImageDraw
import numpy as np
import math
import shutil
import os

fps = 24
resolution = (32, 24) 
circleRadius = 16
circleSize = (52, 45)
black = (0, 0, 0)

video = VideoFileClip("video.webm")
imageFolder = os.getcwd() + "/imgDirectory"

duration = video.duration
totalFrames = math.floor(duration * fps)
lowResFrames = np.zeros(shape=(totalFrames, resolution[0], resolution[1]))

print("\n\n\n\nTotal Frames: ", totalFrames)
print(os.getcwd() + "\n\n\n")

for i in range(0, totalFrames):
    frame = video.get_frame(fps / 6)
    shape = frame.shape
    ratio = [shape[0] / resolution[0], shape[1] / resolution[1]]
    
    for x in range(0, resolution[0]):
        for y in range(0, resolution[1]):
            pixel = frame[math.floor(x * ratio[0]), math.floor(y * ratio[1]), 0]
            if (pixel > 128): lowResFrames[i,x,y] = 1


print("\n\n\n\n\n\n")
if (os.path.isdir(imageFolder)): 
    shutil.rmtree(imageFolder)
os.mkdir(imageFolder)
for i in range(0, lowResFrames.shape[0]):
    print("Drawing on Image " + str(i))
    imagePath = imageFolder + "/" + str(i) + ".png"
    shutil.copyfile(os.getcwd() + "/scantron.png", imagePath)
    
    image = Image.open(imagePath)
    draw = ImageDraw.Draw(image)

    offsetX = 0
    for x in range(0, resolution[0]):
        if (x == 10 or x == 21):
            offsetX -= 20
            continue

        offsetY = 0
        for y in range(0, resolution[1]):
            if (y == 5 or y == 11 or y == 17 or y == 23):
                offsetY += 10.5
                continue

            # if (lowResFrames[i,x,y] == 1): continue

            # Center Coordinates
            posX = math.floor(220 + x * 52 + circleRadius + offsetX)
            posY = math.floor(415 + y * 46 + circleRadius + offsetY)

            gradient = (math.floor(totalFrames / 255 * i), x * 7, y * 7)
            draw.ellipse((posX - circleRadius, posY - circleRadius, posX + circleRadius, posY + circleRadius), fill=gradient)

            print("\tDrawing on Image " + str(i) + " (" + str(x) + ", " + str(y) + ")")

    image.save(imagePath)
    print("Done Drawing on Image " + str(i) + "\n")
    break
