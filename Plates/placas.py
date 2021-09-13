import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

placa = []
image = cv2.imread('auto001.jpg')
""" TRANSFORMA IMAGEN A ESCALA DE GRISES Y QUITAR EL RUIDO """
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.blur(gray,(3,3))
""" ENGROSAR AREA BLANCAS SI LA PLACA NO ES TAN GRUESA """
canny = cv2.Canny(gray,150,200)
canny = cv2.dilate(canny,None,iterations=1)
#_,cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(image,cnts,-1,(0,255,0),2)

""" RECORRE CADA CONTORNO EN CNTS """
for c in cnts:
  area = cv2.contourArea(c)
  #DETECTA RECTANGULO O CUADRADO DENTRO DE LA IMAGEN
  x,y,w,h = cv2.boundingRect(c)
  #DETERMINA VERTICES DEL CONTORNO (PREDETERMINADO)
  epsilon = 0.09*cv2.arcLength(c,True)
  approx = cv2.approxPolyDP(c,epsilon,True)
  
  #EL IF BUSCA CONFIABILIDAD DE CONTORNOS, MIENTRAS MAS MEJOR EL RESULTADO
  if len(approx)==4 and area>9000:
    print('area=',area)
    #cv2.drawContours(image,[approx],0,(0,255,0),3)

    #CALCULAR EL AREA DE LA PLACA DEPENDIENDO DE LA PLACA DEL LUGAR
    aspect_ratio = float(w)/h
    if aspect_ratio>2.4:
      #ALMACENA EL AREA DONDE ESTA LA MATRICULA EN ESCALA DE GRISES
      placa = gray[y:y+h,x:x+w]
      #MODO DE SEGMENTACION  DE PAGINA 
      text = pytesseract.image_to_string(placa,config='--psm 11')
      print('PLACA: ',text)
      cv2.imshow('PLACA',placa)
      #IMPRIME SOLO LA PLACA
      cv2.moveWindow('PLACA',780,10)
      cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)
      #VISUALIZA RESULTADOS DE LA PLACA EN IMAGEN
      cv2.putText(image,text,(x-20,y-10),1,2.2,(0,255,0),3)
      
cv2.imshow('Image',image)
cv2.moveWindow('Image',45,10)
cv2.waitKey(0)