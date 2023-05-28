import cv2
from PIL import Image
import pypdfium2 as pdfium
from os import walk
import uuid
import json
################  EXTRACT IMAGES FROM PDF ################################
PDF_NAME = "Sanskrit_Text"
pdf = pdfium.PdfDocument("Sanskrit_Text.pdf")
version = pdf.get_version()  # get the PDF standard version
n_pages = len(pdf)
page_indices = [i for i in range(n_pages)]  # all pages
renderer = pdf.render(
    pdfium.PdfBitmap.to_pil,
    page_indices = page_indices,
    scale = 300/72,  # 300dpi resolution
)
for i, image in zip(page_indices, renderer):
    image.save("./pdf-images/%s_%0*d.jpg" % (PDF_NAME, n_pages, i))


################  PERDORM OCR ###########################################

# make an array of images extracted from pdf
filenames = next(walk("./pdf-images"), (None, None, []))[2] 
kernels = [(50,10, 110, 550), (50,10, 110, 550), (50,10, 110, 550), (50,10, 110, 550), (35, 17, 70, 650)]
bounding_boxes = {}
for index, img in enumerate(filenames):
    image = cv2.imread("./pdf-images/" + img)
    base_image = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernels[index][0], kernels[index][1]))
    dilate = cv2.dilate(thresh, kernel, iterations = 1)
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key = lambda x: cv2.boundingRect(x)[0])

    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if h > kernels[index][2] and w > kernels[index][3]:
            roi = image[y:y+h, x:x+w]
            uid = str(uuid.uuid1())
            cv2.imwrite("./pdf-images/cropped-images/%s.png" %(uid), roi)
            cv2.rectangle(image, (x,y), (x+w, y+h), (36, 255, 12), 2)
            bounding_boxes[uid] = {
                'top_left': [x, y],
                'top_right': [x+w, y],
                'bottom_left': [x, y+h],
                'bottom_right': [x+w, y+h]
            }
    with open('bounding_boxes.json', 'w') as file:
        json.dump(bounding_boxes, file, indent=4)
    cv2.imwrite("./pdf-images/bounding-box/%s.png" %(img[:-4]), image)