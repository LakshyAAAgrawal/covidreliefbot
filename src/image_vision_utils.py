import pytesseract
import cv2
import numpy as np
from PIL import Image


def preprocess_img(filename):
    img_1 = cv2.imread(filename)
    dpi = None

    # ToDo use DPI for adaptive blurring
    # try:
    #     with Image.open(filename) as im:
    #         dpi = im.info['dpi']
    # except Exception as ex:
    #     pass

    img2gray = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 180, 255, cv2.THRESH_BINARY)
    image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
    ret, img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY)

    # Open Noise and close holes
    # kernel = np.ones((1, 1), np.uint8)
    # img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=1)
    # img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=1)

    # if( dpi is not None) and (dpi[0] > 90) and (dpi[1] > 90):
    #     print('Dilating!!', dpi)
    #     ### Required in low density image, but harmful in high density image
    #     kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    #     img = cv2.dilate(img, kernel, iterations=1) # Cross Dilate

    #### ToDo: Work on fine-graining of contouring and focus
    # contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # for contour in contours:
    #     print(contour.shape)
    #     # get rectangle bounding contour
    #     [x, y, w, h] = cv2.boundingRect(contour)

    #     # Don't plot small false positives that aren't text
    #     if w < 35 and h < 35:
    #         continue

    #     # draw rectangle around contour on original image
    #     # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
    return img


if __name__=='__main__':
    # filename = '/home/viresh/Documents/CovidReliefBot/UselessSample2.jpg'
    # filename = '/home/viresh/Documents/CovidReliefBot/UselessSample1.jpg'
    # filename = '/home/viresh/Documents/CovidReliefBot/useful2.jpg'
    filename = '/home/viresh/Documents/CovidReliefBot/useful.jpg'

    img = preprocess_img(filename)
    print(pytesseract.image_to_string(img))

    cv2.namedWindow("Real", cv2.WINDOW_NORMAL)
    cv2.imshow('Real', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

