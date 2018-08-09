#coding=utf-8
from random import randint, choice
from PIL import Image, ImageDraw, ImageFont #导入三个文件，画板，画笔，文字
from cStringIO import StringIO # 导入内存文件接口
from string import printable # 可打印字符

def create_captcha():
    '''图形验证码方法1：'''
    # # 字体
    # font_path = "utils/captcha/font/Arial.ttf"
    # # 打开一个背景图片
    # img = Image.open('utils/captcha/image2.jpg')
    #
    # font = ImageFont.truetype(font_path, 100)
    # # 画笔
    # draw = ImageDraw.Draw(img)
    # # 文字
    # text = '12345'
    # # 写的文字位置
    # draw.text((100, 10), text, font=font, fill=(100,100,100))
    # # 写的线文字位置
    # draw.line(((100,10), (300, 10)), fill=(100,100,100), width=2)
    #
    #
    # out = StringIO()
    # img.save(out, format='jpeg')
    # content = out.getvalue()
    # out.close()
    # return 'aaa', content


    #'''图形验证码方法2：'''
    # 字体位置及字体颜色
    font_path = "utils/captcha/font/Arial.ttf"
    font_color = (randint(150,200), randint(0,150), randint(0,150)) # rgb 红绿蓝
    # 线条的颜色
    line_color = (randint(0,150), randint(0,150), randint(150,200))
    # 点的颜色
    point_color = (randint(0, 150), randint(50, 150), randint(150, 200))
    width, height = 100, 40
    # 图片颜色
    image = Image.new('RGB', (width, height), (200, 200, 200))
    font = ImageFont.truetype(font_path, height-10)
    # 将画笔画的任何笔记放在画板上
    draw = ImageDraw.Draw(image)

    #生成验证码
    # printable是一串字符串：打印出来如下：
    # "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    # print printable,type(printable) # 打印测试
    # 通过join将空字符传和printable这个字符串的前62个元素进行切割出阿来，
    # 通过choice随机选择4次，得到4个从"0123....WXYZ"中随机获取的字符串
    text =''.join([choice(printable[:62]) for i in xrange(4)])
    #把验证码写到画布上
    draw.text((10,10), text, font=font, fill=font_color)
    #在画板上绘制线条，循环次数代表线的条数
    for i in xrange(0, 5):
        draw.line(((randint(0, width), randint(0, height)),
                   (randint(0, width), randint(0, height))),
                  fill=line_color, width=2)
    #在画板上绘制点
    for i in xrange(randint(100, 1000)):
        draw.point((randint(0, width), randint(0, height)), fill=point_color)
    #输出
    out = StringIO() # 将图片保存实例化对象，放在内存文件上
    image.save(out, format='jpeg') # 让文件以'jpeg'的方式保存到内存文件上
    content = out.getvalue()
    out.close() # 文件用完就关闭
    print '图型验证码',text
    return text, content # 将验证码和内容（即由各类点和线形成的图片）都返回










