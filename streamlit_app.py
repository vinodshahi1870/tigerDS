import streamlit as st
from skimage.metrics import structural_similarity 
import imutils 
import cv2
from PIL import Image 
import requests

st.title('📺 Pan Card Checker')

st.write('Here you can check Pan Card is tampered or not')
original = Image.open(requests.get( 'https://www.thestatesman.com/wp-content/uploads/2019/07/pan-card.jpg', stream=True) .raw)
tampered = Image.open(requests.get('https://assets1.cleartax-cdn.com/s/img/20170526124335/Pan4.png', stream=True) .raw)
print("Original Image",original.format,"Size" ,original.size,"  ","Tempered Image",tampered.format,"Size",  tampered.size)
original = original.resize((250,160))
original.save("original.png")
tampered = tampered.resize((250,160))
tampered.save("tampered.png")
print("Original image size:",original.size,"  ","Tampered image size:", tampered.size)
original
tampered
original = cv2.imread("original.png")
tampered = cv2.imread("tampered.png")
original_gray = cv2.cvtColor(original , cv2.COLOR_BGR2GRAY)
tampered_gray = cv2.cvtColor(tampered, cv2.COLOR_BGR2GRAY)
(score,diff) = structural_similarity(original_gray,tampered_gray,full=True)
diff = (diff*255).astype("uint8")
print('SSIM:  {}'.format(score))
thres = cv2.threshold(diff,0,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[1]
cunt = cv2.findContours(thres.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cunts = imutils.grab_contours(cunt)
for c in cunts:
    # applying contours on image
    (x,y,w,h) =cv2.boundingRect(c)
    cv2.rectangle(original,(x,y),(x+w,y+h),(0,0,255),2)
    cv2.rectangle(tampered,(x,y),(x+w,y+h),(0,0,255),2)
print("original format of Image")
Image.fromarray(original)
print("Tampered format of Image")
Image.fromarray(tampered)
print("Threshold Image")
Image.fromarray(thres)

