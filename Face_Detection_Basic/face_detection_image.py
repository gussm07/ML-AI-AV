import cv2
import mediapipe as mp 

mp_face_detection = mp.solutions.face_detection 
mp_drawing = mp.solutions.drawing_utils

with mp_face_detection.FaceDetection(
	min_detection_confidence=0.5) as face_detection: #valor minimo de confianza para detectar rostro
	image = cv2.imread("img_01.jpg") #leer imagen de entrada

	height, width, _ = image.shape 
	image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)#TRANSFORMAR POR DEFECTO LA IMAGEN A RGB
	results = face_detection.process(image_rgb)

	#print("Detections", results.detections)


	if results.detections is not None:
		for detection in results.detections:
			#BoundingBox
			print(int(detection.location_data.relative_bounding_box.xmin*widht))
			xmin = int(detection.location_data.relative_bounding_box.xmin*widht)
			ymin = int(detection.location_data.relative_bounding_box.ymin*height)
			w = int(detection.location_data.relative_bounding_box.widht*widht)
			h = int(detection.location_data.relative_bounding_box.height*height)
			cv2.rectangle(image,(xmin,ymin), (xmin+w,ymin+h), (0,255,0),2)

			# Ojo derecho
			x_RE = int(detection.location_data.relative_keypoints[0].x * widht)
			y_RE = int(detection.location_data.relative_keypoints[0].y * height)
			cv2.circle(image, (x_RE, y_RE), 3,(0,0,255),2)

			# Ojo izquierdo
			x_LE = int(detection.location_data.relative_keypoints[1].x * widht)
			y_LE = int(detection.location_data.relative_keypoints[1].y * height)
			cv2.circle(image, (x_LE, y_LE), 3,(255,0,255),2)

			# punta de la nariz
			x_NT = int(detection.location_data.relative_keypoints[2].x * widht)
			y_NT = int(detection.location_data.relative_keypoints[2].y * height)
			cv2.circle(image, (x_NT, y_NT), 3,(0,0,255),2)
			
			#CENTRO DE LA BOCA

			x_MC =int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER).x * widht)
			y_MC =int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER).y * height)
			cv2.circle(image, (x_MC, y_MC),3,(0,255,0),2)

			#TRAGO DE LA OREJA DERECHA
			x_RET =int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.RIGHT_EAR_TRAGION).x * widht)
			y_RET =int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.RIGHT_EAR_TRAGION).y * height)
			cv2.circle(image, (x_RET, y_RET),3,(0,255,255),2)

			x_RET =int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.LEFT_EAR_TRAGION).x * widht)
			y_RET =int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.LEFT_EAR_TRAGION).y * height)
			cv2.circle(image, (x_RET, y_RET),3,(255,255,0),2)


	if results.detections is not None:
		for detection in results.detections:
			mp_drawing.draw_detection(image, detection,
			mp_drawing.DrawingSpec(color=(255,0,255), thickness=3, circle_radius=3),
			mp_drawing.DrawingSpec(color=(0,255,255), thickness=3))


	cv2.imshow("Image", image)
	cv2.waitKey(0)
cv2.destroyAllWindows()