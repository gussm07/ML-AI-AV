import cv2
import mediapipe as mp 

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

with mp_face_mesh.FaceMesh(
	static_image_mode=True,
	max_num_faces=1,
	min_detection_confidence=0.5) as face_mesh:

	image = cv2.imread("img_01.jpg")
	cv2.imshow("Image",image)
	cv2.waitKey(0)
cv2.destroyAllWindows() 