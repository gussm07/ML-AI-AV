import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' """ EJECTUAR PYTESSERACT PARA LEER TEXTO """


def ordenar_puntos(puntos):
    
	n_puntos = np.concatenate([puntos[0], puntos[1], puntos[2], puntos[3]]).tolist()

	y_order = sorted(n_puntos, key=lambda n_puntos: n_puntos[1])

	x1_order = y_order[:2]     
	x1_order = sorted(x1_order, key=lambda x1_order: x1_order[0])

	x2_order = y_order[2:4]
	x2_order = sorted(x2_order, key=lambda x2_order: x2_order[0])
	
	return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]
	
""" LEER LA IMAGEN """    
image = cv2.imread('img_03.jpeg')
""" DETECTAR IMAGEN A ESCALA DE GRISES """
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
""" DETECTAR BORDES DE LA IMAGEN """
canny = cv2.Canny(gray, 10, 150)
""" ENGROSAR LINEAS BLANCAS PARA UNIR AREAS DESPUES DE LA DETECCIÓN DE BORDES """
canny = cv2.dilate(canny, None, iterations=1)
""" ENCUENTRA CONTORNOS EXTERNOS """
cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
""" TOMAR EL CONTORNO MAS GRANDE, QUE CORRESPONDE AL DOCUMENTO """
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]

for c in cnts:
	epsilon = 0.01*cv2.arcLength(c,True)
	approx = cv2.approxPolyDP(c,epsilon,True)
	""" DETECCION DE FIGURAS GEOMETRICAS (RECTANGULO) """

        """ CONDICION QUE TRATA DE UN CUADRADO O RECTANGULO """
	if len(approx)==4:
		cv2.drawContours(image, [approx], 0, (0,255,255),2)
		
		puntos = ordenar_puntos(approx)
        
            
		cv2.circle(image, tuple(puntos[0]), 7, (255,0,0), 2)
		cv2.circle(image, tuple(puntos[1]), 7, (0,255,0), 2)
		cv2.circle(image, tuple(puntos[2]), 7, (0,0,255), 2)
		cv2.circle(image, tuple(puntos[3]), 7, (255,255,0), 2)
		
		pts1 = np.float32(puntos)
		pts2 = np.float32([[0,0],[270,0],[0,310],[270,310]])
		M = cv2.getPerspectiveTransform(pts1,pts2)
		dst = cv2.warpPerspective(gray,M,(270,310))
		cv2.imshow('dst', dst)
		
		texto = pytesseract.image_to_string(dst, lang='spa')
		print('texto: ', texto)

cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()