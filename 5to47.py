import os
from shutil import copyfile, rmtree
from PIL import Image
import image_slicer

#creating a temp folder for the quadrants ones to go
try:
    os.mkdir("temp")
except Exception as e:
    print(e)
    
for i in range(5):
    copyfile(f"{i}.png", f"temp/{i}.png")
os.chdir("temp")

#import the compact ctm images, divide them into quadrants and load them
im = []
for i in range(5):
    image_slicer.slice(f'{i}.png', 4)
    os.remove(f'{i}.png')
    im.append([Image.open(f"{i}_01_01.png"), Image.open(f"{i}_01_02.png"), Image.open(f"{i}_02_01.png"), Image.open(f"{i}_02_02.png")])

#making another folder for the textures
try:
    os.mkdir("../textures")
except Exception as e:
    print(e)
os.chdir("../textures")

#stitch the images together to achieve 47 ctm textures
def compactTo47(a, b, c, d):
    (w, h)=im[0][0].size
    width=w*2
    height=h*2
    result = Image.new('RGBA', (width, height))
    result.paste(im=im[a][0], box=(0, 0))
    result.paste(im=im[b][1], box=(w, 0))
    result.paste(im=im[c][2], box=(0, h))
    result.paste(im=im[d][3], box=(w, h))
    return result

tiles=[[0,0,0,0],[0,3,0,3],[3,3,3,3],[3,0,3,0],[0,3,2,4],[3,0,4,2],[2,4,2,4],[3,3,4,4],[4,1,4,4],[4,4,4,1],[1,4,1,4],[1,1,4,4],
       [0,0,2,2],[0,3,2,1],[3,3,1,1],[3,0,1,2],[2,4,0,3],[4,2,3,0],[4,4,3,3],[4,2,4,2],[1,4,4,4],[4,4,1,4],[4,4,1,1],[4,1,4,1],
       [2,2,2,2],[2,1,2,1],[1,1,1,1],[1,2,1,2],[2,4,2,1],[3,3,1,4],[2,1,2,4],[3,3,4,1],[1,1,1,4],[1,1,4,1],[4,1,1,4],[1,4,4,1],
       [2,2,0,0],[2,1,0,3],[1,1,3,3],[1,2,3,0],[4,1,3,3],[1,2,4,2],[1,4,3,3],[4,2,1,2],[1,4,1,1],[4,1,1,1],[4,4,4,4]]

for i in range(47):
    r=compactTo47(tiles[i][0],tiles[i][1],tiles[i][2],tiles[i][3])
    r.save(f'{i}.png')

#delete temp folder
for x in im:
    for el in x:
        el.close()
try:
    rmtree("../temp/")
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))
    
print("Finished to convert the ctm_compact textures to ctm! They are saved in the 'textures' folder.\r\n\r\n - Made by Kynatosh")
