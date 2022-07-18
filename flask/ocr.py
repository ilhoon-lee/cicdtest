import json
import base64
import requests
import text_filter as tf

with open("D:/recipe_crol/test9.jpg", "rb") as f:
    img = base64.b64encode(f.read())

text_reconize(img)
def text_reconize(img):
 
    URL = "https://up8wh3ooec.apigw.ntruss.com/custom/v1/13236/52b0ee39e1a14ae9e57428f32e0a1d6cc2c15b6d81c060cb7b20a1b8ee67b9bc/general"
    KEY = "d1FYa0dldWV0VlpvRVV2clZ0bUhubUFSVFltem16em8="
    headers = {
        "Content-Type": "application/json",
        "X-OCR-SECRET": KEY
    }    
    data = {
        "version": "V1",
        "requestId": "sample_id", 
        "timestamp": 0, 
        "images": [
            {
                "name": "sample_image",
                "format": "png",
                "data": img.decode('utf-8')
            }]}
    
    data = json.dumps(data)
    response = requests.post(URL, data=data, headers=headers)
    res = json.loads(response.text)
    fields=res['images'][0]['fields']

    name=[]           
    for i in range(len(fields)):
        name.append(fields[i]['inferText'])
    text = []
    for i in range(len(name)):
        if tf.text_filter(name[i]) is not None:
            text.append(tf.text_filter(name[i]))
        textkind=list(set(text))
    return textkind


