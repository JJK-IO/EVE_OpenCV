import subprocess
import time

import cv2
import numpy
import pyscreenshot
from pygame import mixer  # Load the required library


def is_windows():
    import platform
    if "windows" in platform.platform().lower():
        return True
    return False


def get_screen_resolution():
    if is_windows():
        import ctypes
        user32 = ctypes.windll.user32
        width = user32.GetSystemMetrics(0)
        height = user32.GetSystemMetrics(1)
        return {'width': width, 'height': height}
    else:
        output = \
        subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4', shell=True, stdout=subprocess.PIPE).communicate()[0]
        resolution = output.split()[0].split(b'x')
        return {'width': resolution[0], 'height': resolution[1]}


def intel_grab():
    width = int(get_screen_resolution()['width'])
    height = int(get_screen_resolution()['height'])
    x1 = width - 18  # width - (width/9)
    x2 = width  # width
    y1 = 0  # 0 + (height/2)
    y2 = height  # height
    im = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
    im.save('test.png')


def find_hostiles(screen):
    img_rgb = cv2.imread(screen)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    neut_img = cv2.imread('neut.png', 0)
    red_img = cv2.imread('red.png', 0)
    neut2_img = cv2.imread('neut2.png', 0)

    w, h = red_img.shape[::-1]

    neut_match = cv2.matchTemplate(img_gray, neut_img, cv2.TM_CCOEFF_NORMED)
    neut2_match = cv2.matchTemplate(img_gray, neut2_img, cv2.TM_CCOEFF_NORMED)
    neut2_match = cv2.matchTemplate(img_gray, neut2_img, cv2.TM_CCOEFF_NORMED)
    red_match = cv2.matchTemplate(img_gray, red_img, cv2.TM_CCOEFF_NORMED)

    threshold = 0.99

    loc_neut = numpy.where(neut_match >= threshold)
    loc_neut2 = numpy.where(red_match >= threshold)
    loc_red = numpy.where(red_match >= threshold)

    total_match = len(loc_neut[0]) + len(loc_red[0]) + len(loc_neut2[0])

    if total_match > 0:
        for pt in zip(*loc_red[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        for pt in zip(*loc_neut[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        for pt in zip(*loc_neut2[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        cv2.imwrite('res.png', img_rgb)

    return total_match


if __name__ == "__main__":
    mixer.init()
    mixer.music.load('reee.ogg')
    while True:
        time.sleep(1)
        intel_grab()
        if find_hostiles('test.png') > 0:
            print("HOSTILES FOUND!!!")
            mixer.music.play()
        else:
            mixer.music.stop()
