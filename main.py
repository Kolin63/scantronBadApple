from moviepy import VideoFileClip, ImageSequenceClip
from PIL import Image, ImageDraw
import numpy as np
import math
import shutil
import os

fps = 0.5
resolution = (32, 24) 
circleRadius = 16
circleSize = (52, 45)
black = (0, 0, 0)

video = VideoFileClip("video.webm")
finishedVideoLocation = os.getcwd() + "/finishedVideo.mp4"
imageFolder = os.getcwd() + "/imgDirectory"

duration = video.duration
originalFPS = video.fps
totalFrames = math.floor(duration * fps)
lowResFrames = np.zeros(shape=(totalFrames, resolution[0], resolution[1]))

print("\n\n\n\nTotal Frames:", totalFrames)
print("Original Total Frames:", duration * originalFPS)
print("Original FPS:", originalFPS)
print(os.getcwd() + "\n\n\n")

for i in range(0, totalFrames):
    print("Getting Colors of Frame " + str(i))
    frame = video.get_frame(i / fps)
    shape = frame.shape
    ratio = [shape[0] / resolution[0], shape[1] / resolution[1]]
    
    for x in range(0, resolution[0]):
        for y in range(0, resolution[1]):

            average = 0
            averageLength = 0
            for a in range(math.floor(x * ratio[0]), math.floor(x * ratio[0] + ratio[0])):
                for b in range(math.floor(y * ratio[1]), math.floor(y * ratio[1] + ratio[1])):
                    pixel = frame[a, b, 0]
                    if (pixel > 128): pixel = 1
                    else: pixel = 0
                    average += pixel
                    averageLength += 1
            
            average = average / averageLength
            if (average > 0.5):
                lowResFrames[i, x, y] = 1



input("STOP ITTT")

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

    offsetX = 220
    multX = 52
    for x in range(0, resolution[0]):
        if (x == 10):
            offsetX -= 20
            continue
        if (x >= 21):
            offsetX = 286
            multX = 48
        if (x == 21):
            continue

        offsetY = 415
        multY = 46
        for y in range(0, resolution[1]):
            if (y == 11 and x > 21):
                multX = 52
                offsetX -= 105
                multY = 46
            if (y == 5 and x < 21 or y == 11 or y == 23):
                offsetY += 10.5
                continue
            if (y == 17):
                offsetY += 8
                continue
            if (x > 21 and y < 11):
                multY = 42.5
                if (y == 9):
                    offsetY += 10
                    continue
                if (y == 10 and x < 27):
                    continue

            if (lowResFrames[i,x,y] == 1): 
                continue

            # Center Coordinates
            posX = math.floor(x * multX + circleRadius + offsetX)
            posY = math.floor(y * multY + circleRadius + offsetY)

            # gradient = (math.floor(totalFrames / 255 * i), x * 7, y * 7)
            draw.ellipse((posX - circleRadius, posY - circleRadius, posX + circleRadius, posY + circleRadius), fill=black)

            # print("\tDrawing on Image " + str(i) + " (" + str(x) + ", " + str(y) + ")")

    image.save(imagePath)

    if (i == 1000): break

finishedVideo = ImageSequenceClip(imageFolder, fps=fps)
finishedVideo.write_videofile(finishedVideoLocation)
