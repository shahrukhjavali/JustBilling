import cv2
from pyzbar.pyzbar import decode
import imutils
import numpy as np


def barcodeScanner():
    video = cv2.VideoCapture(0)
    video.set(3, 640)
    video.set(4, 480)
    a = 0
    value = 0
    while True:
        a = a + 1
        check, frame = video.read()
        frame = imutils.resize(frame, width=400)
        for barcode in decode(frame):
            value = barcode.data.decode('utf-8')
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (255, 0, 255), 5)
            # cv2.imshow("Image", gray)
            break
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()
    print("scanned" +" "+ str(value))
    return value
