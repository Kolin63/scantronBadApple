from moviepy import VideoFileClip, ImageSequenceClip, AudioFileClip, CompositeAudioClip
from PIL import Image, ImageDraw
import numpy as np
import math
import shutil
import os

fps = 30
stopframe = -1
resolution = (32, 24) 
circleRadius = 16
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
    ratio = [shape[0] / resolution[1], shape[1] / resolution[0]]  
    
    for y in range(0, resolution[1]):  
        for x in range(0, resolution[0]):  

            average = 0
            averageLength = 0
            for a in range(math.floor(y * ratio[0]), math.floor(y * ratio[0] + ratio[0])):  
                for b in range(math.floor(x * ratio[1]), math.floor(x * ratio[1] + ratio[1])):  
                    pixel = frame[a, b, 0]
                    if (pixel > 128): pixel = 1
                    else: pixel = 0
                    average += pixel
                    averageLength += 1
            
            average = average / averageLength
            if (average > 0.5):
                lowResFrames[i, x, y] = 1  
            else:
                lowResFrames[i, x, y] = 0
    
    if (i == stopframe):
        break


lowResFrames = np.rot90(lowResFrames, axes=(2, 1))


print("\n\n\n\n\n\n")
if (os.path.isdir(imageFolder)): 
    shutil.rmtree(imageFolder)
os.mkdir(imageFolder)


for i in range(0, lowResFrames.shape[0]):
    indexStr = str(i)
    indexStr = indexStr.zfill(8)
    print("Drawing on Image " + indexStr)
    imagePath = imageFolder + "/" + indexStr + ".png"
    shutil.copyfile(os.getcwd() + "/scantron.png", imagePath)
    
    image = Image.open(imagePath)
    draw = ImageDraw.Draw(image)

    offsetX = 220
    multX = 52
    for y in range(0, lowResFrames.shape[2]):  
        if (y == 10):
            offsetX -= 20
            continue
        if (y >= 21):
            offsetX = 286
            multX = 48
        if (y == 21):
            continue

        offsetY = 415
        multY = 46
        for x in range(0, lowResFrames.shape[1]):  
            if (x == 11 and y > 21):
                multX = 52
                offsetX -= 105
                multY = 46
            if (x == 5 and y < 21 or x == 11 or x == 23):
                offsetY += 10.5
                continue
            if (x == 17):
                offsetY += 8
                continue
            if (y > 21 and x < 11):
                multY = 42.5
                if (x == 9):
                    offsetY += 10
                    continue
                if (x == 10 and y < 27):
                    continue

            if (lowResFrames[i, x, y] == 1):  
                continue
                # pass

            # Center Coordinates
            posX = math.floor(y * multX + circleRadius + offsetX)  
            posY = math.floor(x * multY + circleRadius + offsetY) 

            # gradient = (math.floor(totalFrames / 255 * i), x * 7, y * 7)
            draw.ellipse((posX - circleRadius, posY - circleRadius, posX + circleRadius, posY + circleRadius), fill=black)

            # print("\tDrawing on Image " + str(i) + " (" + str(x) + ", " + str(y) + ")")

    image.save(imagePath)
    if (i == stopframe):
        break


finishedVideo = ImageSequenceClip(imageFolder, fps=fps)

audio = AudioFileClip("video.webm")
newAudio = CompositeAudioClip([audio])
finishedVideo.audio = newAudio

finishedVideo.write_videofile(finishedVideoLocation)
