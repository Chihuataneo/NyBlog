from PIL import Image, ImageDraw,ImageFont,ImageFilter
import random

def randcolor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

def create_verifycode():
    firstnum=random.randint(1,20)
    secondnum=random.randint(1,20)
    operator=random.choice('+-*')
    verifystr=str(firstnum)+operator+str(secondnum)
    result=eval(verifystr)
    print(result)
    img=Image.new('RGB', (160,50), (255,255,255))
    draw=ImageDraw.Draw(img)
    font=ImageFont.truetype('Arial.ttf',36)
    verifystr+='=?'
    for index in range(len(verifystr)):
        draw.text((10+20*index,10),text=verifystr[index],font=font,fill=randcolor())
    img=img.filter(ImageFilter.CONTOUR)
    return img,str(result)
