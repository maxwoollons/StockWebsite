from PIL import ImageDraw, Image, ImageFont

class Watermark(object):
    def process(self, img):
        fnt = ImageFont.truetype("static/font/font.ttf", 300)
        d = ImageDraw.Draw(img)

        d.text((200,500), "ultimateimagination.com.au", font=fnt, fill=(255,255,255,128))
        d.text((200,200), "ultimateimagination.com.au", font=fnt, fill=(255,255,255,255))
        d.text((200,800), "ultimateimagination.com.au", font=fnt, fill=(255,255,255,128))
        return img