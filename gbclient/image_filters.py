
import random
from PIL import ImageDraw as PILImageDraw
from PIL.ImageQt import ImageQt


def negative_filter(editor):
    image = editor.image
    if image is None:
        return
    draw = PILImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()

    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            draw.point((i, j), (255 - a, 255 - b, 255 - c))

    return ImageQt(image.convert('RGBA'))


def noise_filter(editor):
    image = editor.image
    if image is None:
        return
    draw = PILImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()

    max_noise = 100
    min_noise = -100
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0] + random.randint(min_noise, max_noise)
            b = pix[i, j][1] + random.randint(min_noise, max_noise)
            c = pix[i, j][2] + random.randint(min_noise, max_noise)

            if a > 255:
                a = 255
            if b > 255:
                b = 255
            if c > 255:
                c = 255

            if a < 0:
                a = 0
            if b < 0:
                b = 0
            if c < 0:
                c = 0

            draw.point((i, j), (a, b, c))

    return ImageQt(image.convert('RGBA'))


def gray_filter(editor):
    image = editor.image
    if image is None:
        return
    draw = PILImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()

    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = (a + b + c) // 3
            draw.point((i, j), (S, S, S))

    return ImageQt(image.convert('RGBA'))
