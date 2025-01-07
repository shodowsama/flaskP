import random
import string

from datetime import datetime
from PIL import Image,ImageFont,ImageDraw
from io import BytesIO

class ImageCode():

    def get_text(self):
        list = random.sample(string.ascii_letters + string.digits,4)
        return ''.join(list)

    def rand_color(self):
        red = random.randint(0,255)
        green = random.randint(0,255)
        blue = random.randint(0,255)

        return red,green,blue
    
    def draw_lines(self,draw,num,w,h):
        for i in range(num):
            x1 = random.randint(0,w/2)
            y1 = random.randint(0,h/2)
            x2 = random.randint(0,w/2)
            y2 = random.randint(h/2,h)

            draw.line((x1,y1),(x2,y2),fill='black',width=2)


    def draw_verify_code(self):

        code = self.get_text()

        width,height = 120,50
        im = Image.new('RGB',(width,height),'white')
        font = ImageFont.truetype(font='C:\windows\Font\Arial.ttf',size=40)
        drow = ImageDraw.Draw(im)

        for i in range(4):
            drow.text( (random.randint(3,10)+50*i , random.randint(3,10)) ,
                      text=code[i],fill=self.rand_color(),font=font)

        self.draw_lines(drow,3,width,height)

        return im,code
    
    def get_code(self):
        image,code = self.draw_verify_code()
        buf = BytesIO()
        image.save(buf,'jpeg')
        image_b_string = buf.getvalue()
        return code,image_b_string



Image_Code = ImageCode()
Image_Code.draw_verify_code()

def model_to_json(result):
    dict = {}
    for k,v in result.__dict__.items():
        if not k.startswith('_sa_'):
            if isinstance(v,datetime):
                v = v.strftime('%Y-%m-%d %H:%M:%S')
            dict[k] = v
    return dict