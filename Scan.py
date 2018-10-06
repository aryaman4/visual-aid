from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
import cv2
import imutils
from PIL import Image
import pytesser3
import os
original_open = open
def bin_open(filename, mode='rb'):       # note, the default mode now opens in binary
    return original_open(filename, mode)

def scan ():
    image = cv2.imread("paper6.jpg")
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height=500)

    kernel = cv2.getStructuringElement(cv2.MORPH_ERODE, (5, 5))
    image = cv2.erode(image, kernel, iterations=1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    edged = cv2.Canny(gray, 30, 175)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    for c in cnts:

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)

    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset=10, method="gaussian")
    warped = (warped > T).astype("uint8") * 255

    warped = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, warped)
    import builtins


    img = Image.open(filename)

    try:
        builtins.open = bin_open
        bts = pytesser3.image_to_string(img)
    finally:
        builtins.open = original_open

    os.remove(filename)
    file = open("text.txt", "x")
    file = open("text.txt", "r+")
    file.write(str(bts, 'cp1252', 'ignore'))
    file.close()
    file = open("text.txt", "r+")
    f = open("temp.txt", "x")
    f = open("temp.txt", "r+")
    while True:
        c = file.read(1)
        if not c:
            break
        if ord(c) < 126:
            f.write(c)
    f.close()
    file.close()
    os.remove("text.txt")
    os.renames("temp.txt", "text.txt")