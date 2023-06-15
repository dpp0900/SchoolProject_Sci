import base64
import requests
import json
import time
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

import static.lib.logger as logger


def OCR(data):
    with open(data, "rb") as f:
        img = base64.b64encode(f.read())
    URL = open("OCR_url","r").read()
    KEY = open("OCR_token","r").read()
    headers = {
        "Content-Type": "application/json",
        "X-OCR-SECRET": KEY
    }
    data = {
        "version": "V1",
        "requestId": "ScProject" + str(time.time()),
        "timestamp": 0,
        "images": [
            {
                "name": "ScProject" + str(time.time()),
                "format": "png",
                "data": img.decode('utf-8')
            }
        ]
    }
    data = json.dumps(data)
    response = requests.post(URL, data=data, headers=headers)
    res = json.loads(response.text)
    return res

def removeSign(text):
    return text.replace(",","").replace("!","").replace(".","").replace("?","").replace(" ","")

def checkPreviousCats(cat):
    model = json.load(open("model.json", "r"))
    prevwords = []
    for prevcat in model["wordlist"]:
        if cat == prevcat:
            break
        prevwords.append(json.load(open("model.json", "r"))[prevcat].keys())
        
    print(prevwords)

def putTextPIL(img, text, pos, color, fontPath, fontSize):
    font = ImageFont.truetype(fontPath, fontSize)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text(pos, text, font=font, fill=color)
    img = np.array(img_pil)
    return img

def getVertices(boundingPoly):
    verticesTOP = (int(boundingPoly[0]['x']), int(boundingPoly[0]['y']))
    verticesLOW = (int(boundingPoly[2]['x']), int(boundingPoly[2]['y']))
    verticesMID = ((int(boundingPoly[0]['x'])),abs(int(boundingPoly[0]['y'])-10))
    return verticesTOP, verticesLOW, verticesMID

def resizeImg(imgPath, standardSize):
    img = cv2.imread(imgPath)
    height, width, _ = img.shape
    if height > standardSize or width > standardSize:
        if height > width:
            ratio = standardSize / height
        else:
            ratio = standardSize / width
        img = cv2.resize(img, dsize=(0,0), fx=ratio, fy=ratio, interpolation=cv2.INTER_AREA)
    cv2.imwrite(imgPath, img)

def label(imgPath, imgName):
    resizeImg(imgPath, 1000)
    imgData = OCR(imgPath)
    json.dump(imgData, open("response.json", "w"), indent=4, ensure_ascii=False)
    wordsData = json.load(open("model.json", "r"))

    img = cv2.imread(imgPath)
    idx = 0
    for field in imgData['images'][0]['fields']:
        idx += 1
        if field == None:
            continue
        boundingPoly = field['boundingPoly']['vertices']
        inferText = removeSign(field['inferText'])
        for cat in wordsData["wordlist"]:
            for word in wordsData["wordlist"][cat].items():
                if word[0] in inferText:
                    if not inferText in wordsData["blacklist"]:
                        verticesTOP, verticesLOW, verticesMID = getVertices(boundingPoly)
                        cv2.rectangle(img, verticesTOP,verticesLOW,(255,0,0))
                        img = putTextPIL(img, field['inferText'].replace(word[0], word[1]), verticesMID, (0,0,0), "AppleGothic.ttf", 10)
                        logger.write_log("label.py", f"trans {word[0]} as {word[1]}", time.time(), "debug")
                        #imgData['images'][0]['fields'][idx] = None
                        break
                    else:
                        continue
                elif word[1].lower() == inferText.lower() and word[1] != 0:
                    verticesTOP, verticesLOW, verticesMID = getVertices(boundingPoly)
                    cv2.rectangle(img, verticesTOP,verticesLOW,(255,0,0))
                    img = putTextPIL(img, word[0], verticesMID, (0,0,0), "AppleGothic.ttf", 10)
                    logger.write_log("label.py", f"trans {word[1]} as {word[0]}", time.time(), "debug")
                    #imgData['images'][0]['fields'][idx] = None
                    break
    cv2.imwrite("static/img/output/" + imgName, img)

if __name__ == "__main__":
    label("static/img/input/science.8511582.fp.png", "out.png")
    #checkPreviousCats("elements")
