import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# print(pytesseract.get_tesseract_version())

#folder = r'crops_YOLOv5x/crops'
folder = r'crop_yolov7/antiga'


totalPlaca = 0
acertoPlaca = 0
totalCaractere = 0
acertoCaractere = 0
totalMaisQue7Caracteres = 0
totalMenosQue7Caracteres = 0

for filename in os.listdir(folder):
    print(filename)
    caracteresCorretosPlaca = 0
    img = None
    text = None
    print('Filename ', filename)
    img = cv2.imread(os.path.join(folder,filename))
    img = cv2.resize(img.copy(), (240,78), interpolation = cv2.INTER_CUBIC)
    h, w, c = img.shape


    img = img[ h-55:h-5 , w - 220 :w - 15]  # resized to 240x78

    imgGray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
    # plt.imshow(img, cmap='gray'), plt.xticks([]), plt.yticks([])
    # plt.title('Imagem Cinza')
    # plt.show()
    
    blurred = cv2.GaussianBlur(imgGray.copy(), (3,3), cv2.BORDER_DEFAULT)
    # plt.imshow(blurred, cmap='gray'), plt.xticks([]), plt.yticks([])
    # plt.title('Gaussiana')
    # plt.show()
    
    thresh = cv2.adaptiveThreshold(blurred.copy(), 70, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 35, 11)
    # plt.imshow(thresh, cmap='gray'), plt.xticks([]), plt.yticks([])
    # plt.title('Threshold')
    # plt.show()
    
    kernel_rect = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))    
    erode = cv2.erode(thresh.copy(),kernel_rect,iterations=1)
    # plt.imshow(erode,cmap='gray'), plt.xticks([]), plt.yticks([])
    # plt.title('erode')
    # plt.show()    

    dilate = cv2.dilate(erode.copy(),kernel_rect,iterations=1)
    # plt.imshow(dilate,cmap='gray'), plt.xticks([]), plt.yticks([])
    # plt.title('dilate')
    # plt.show()
    

## ----------------------------------------------------------------------------

# 0    Orientation and script detection (OSD) only.
# 1    Automatic page segmentation with OSD.
# 2    Automatic page segmentation, but no OSD, or OCR.
# 3    Fully automatic page segmentation, but no OSD. (Default)
# 4    Assume a single column of text of variable sizes.
# 5    Assume a single uniform block of vertically aligned text.
# 6    Assume a single uniform block of text.
# 7    Treat the image as a single text line.
# 8    Treat the image as a single word.
# 9    Treat the image as a single word in a circle.
# 10    Treat the image as a single character.
# 11    Sparse text. Find as much text as possible in no particular order.
# 12    Sparse text with OSD.
# 13    Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.      
   
    text = pytesseract.image_to_string(dilate, lang='eng', config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
     
    if(text != None):
        totalPlaca = totalPlaca + 1
            
    print('Text: ', text.strip())
    print('Filename: ', filename)
    list_of_letters = list(text.strip())
    print("Recognition:\n", list_of_letters)
    
    # if(filename.split('.')[0] == "GHL1J88"):
    #    list_of_letters.pop(5)    


    heuristc = ''
    if(len(list_of_letters) == 7):
        for i, l in enumerate(list_of_letters):
        
            if(i == 0 or i == 1 or i == 2) :
                if(l == '0'):
                    list_of_letters[i]  = 'O'
                elif(l == '1'):
                    list_of_letters[i]  = 'I'
                elif(l == '2'):
                    list_of_letters[i]  = 'Z'            
                elif(l == '4'):
                    list_of_letters[i]  = 'A'
                elif(l == '5'):
                    list_of_letters[i]  = 'S'
                elif(l == '6'):
                    list_of_letters[i]  = 'G'             
                elif(l == '7'):
                    list_of_letters[i]  = 'T'
                elif(l == '8'):
                    list_of_letters[i]  = 'B'             
            elif(i == 3 or i==4 or i==5 or i==6):
                if(l == 'O'):
                    list_of_letters[i]  = '0'
                if(l == 'Q'):
                    list_of_letters[i]  = '0'            
                elif(l == 'D'):
                    list_of_letters[i]  = '0'         
                elif(l == 'I'):
                    list_of_letters[i]  = '1'
                elif(l == 'Z'):
                    list_of_letters[i]  = '2'           
                elif(l == 'A'):
                    list_of_letters[i]  = '4'
                elif(l == 'S'):
                    list_of_letters[i]  = '5'             
                elif(l == 'G'):
                    list_of_letters[i]  = '6'               
                elif(l == 'T'):
                    list_of_letters[i]  = '7'
                elif(l == 'B'):
                    list_of_letters[i]  = '8'
            heuristc = heuristc + list_of_letters[i]
        
        if(heuristc.strip() == filename.split('.')[0]):
            acertoPlaca = acertoPlaca + 1   
                 
        listCharFilename = list(filename.split('.')[0])
        for i, c in enumerate(listCharFilename):
            totalCaractere = totalCaractere + 1
            if(c == heuristc[i]):
                acertoCaractere = acertoCaractere + 1;    
                caracteresCorretosPlaca = caracteresCorretosPlaca + 1

    elif(len(list_of_letters) > 7):
       totalMaisQue7Caracteres = totalMaisQue7Caracteres + 1
    elif(len(list_of_letters) < 7):
         totalMenosQue7Caracteres = totalMenosQue7Caracteres + 1
                            
    print("Heuristic:\n", list(heuristc)) 
    print("Qtd Caracteres Corretos Placa: ", caracteresCorretosPlaca)
    print("\n")
    
print("Total de Placas = ", totalPlaca)
print("Acerto Total da Placa = ", acertoPlaca)
print("Total de Placas Reconhecidas com MAIS de 7 caracteres = ", totalMaisQue7Caracteres)
print("Total de Placas com MENOS de 7 caracteres = ", totalMenosQue7Caracteres)
print("Total de Placas DESCONSIDERADAS = ", totalMaisQue7Caracteres + totalMenosQue7Caracteres)
print("Total de Caracteres = ", totalCaractere)
print("Acerto Total de Caracteres = ", acertoCaractere)
print("ACC = ", round(acertoCaractere/totalCaractere,4) * 100, "%")

    
