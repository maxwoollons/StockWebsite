from PIL import ImageDraw, Image, ImageFont

class Watermark(object):
    def process(self, img):
        img = img.convert('RGBA')
        fnt = ImageFont.truetype("static/font/font.ttf", 300)
        
        txt = Image.new('RGBA', img.size, (255,255,255,0))
        d = ImageDraw.Draw(txt)   



        
        
        
        d.text((200,200), "ultimateimagination.com.au", font=fnt, fill=(255,255,255,80))
        
        d.text((200,800), "ultimateimagination.com.au", font=fnt, fill=(255,255,255,80))
        
        d.text((200,1400), "ultimateimagination.com.au", font=fnt, fill=(255,255,255,80))
        
        d.text((200,2000), "ultimateimagination.com.au", font=fnt, fill=(255,255,255,80))
        d.text((200,2600), "ultimateimagination.com.au", font=fnt, fill=(255,255,255,80))
        img = Image.alpha_composite(img, txt) 
        
        return img