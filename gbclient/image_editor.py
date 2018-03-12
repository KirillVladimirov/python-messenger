#!/usr/bin/python3
# -*- coding: utf-8 -*-


from PyQt5.QtGui import QPixmap

from PIL import Image as PILImage
from PIL import ImageDraw as PILImageDraw
from PIL.ImageQt import ImageQt


class ImageEditor(object):

    def __init__(self, image):
        self.image = image
        self.image_draw = PILImageDraw.Draw(image)

    def filter(self, filter_name):
        if self.image_draw:
            method = getattr(self.image_draw, filter_name)
            return self.method()

        return None

    def filter_gray(self):
        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()

        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = (a + b + c) // 3
                self.image_draw.point((i, j), (S, S, S))

        img_tmp = ImageQt(self.image.convert('RGBA'))
        return img_tmp

    def filter_noise(self):
        pass

    def filter_negative(self):
        pass

    def cut_image(self):
        pass

    def scaling(self):
        pass
