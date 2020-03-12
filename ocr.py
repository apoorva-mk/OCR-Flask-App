import pytesseract
import base64
import cv2 
import numpy as np
from PIL import Image

print("Hi")
filename = "/home/apoorva/Pictures/testocr.png"
file_to_store = "imageToSave.jpg"

#remove noise
def remove_noise(image):
    return cv2.medianBlur(image,3)

# convert to grayscale image
def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#remove skew
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def preprocess(img):
    temp = remove_noise(img)
    temp = convert_to_grayscale(temp)
    temp = thresholding(temp)
    temp = deskew(temp)
    return temp



def obtain_text_from_image(encoded_string):
    with open(file_to_store, "wb") as fh:
        fh.write(base64.decodebytes(encoded_string))

    img = cv2.imread(file_to_store)
    processed_img = preprocess(img)
    cv2.imwrite("Preprocessed.jpg",processed_img)
    text = pytesseract.image_to_string(Image.open('Preprocessed.jpg'))
    return text




def convert():
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string


#obtain_text_from_image(convert())
