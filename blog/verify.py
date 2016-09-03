from PIL import Image, ImageDraw,ImageFont,ImageFilter
import random

def randcolor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

def randcolor_2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def create_lines(draw,size):
    line_num=random.randint(5,8)
    for num in range(line_num):
        begin=(random.randint(0,size[0]),random.randint(0,size[1]))
        end=(random.randint(0,size[0]),random.randint(0,size[1]))
        draw.line([begin,end],fill=randcolor_2())
    return draw

def create_points(draw,size):
    point_num=random.randint(200,400)
    while point_num:
        w=random.randint(0,size[0])
        h=random.randint(0,size[1])
        draw.point((w,h),fill=randcolor())
        point_num-=1
    return draw

def create_verifycode():
    size=(160,50)
    firstnum=random.randint(1,20)
    secondnum=random.randint(1,20)
    operator=random.choice('+-*')
    verifystr=str(firstnum)+operator+str(secondnum)
    result=eval(verifystr)
    img=Image.new('RGB',size, (255,255,255))
    draw=ImageDraw.Draw(img)
    font=ImageFont.truetype('Arial.ttf',36)
    verifystr+='=?'
    for index in range(len(verifystr)):
        draw.text((10+20*index,10),text=verifystr[index],font=font,fill=randcolor())
    draw=create_lines(draw,size)
    draw=create_points(draw,size)
    img=img.filter(ImageFilter.CONTOUR)
    return img,str(result)
