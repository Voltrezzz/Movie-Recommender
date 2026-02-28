
import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
  print('Failed to open the camera')
  exit()
while True:
  ret , frame = cap.read()
  if not ret:
    print('Error : Couldnt extract the frame')
    break
  
  cv2.imshow('Emotional Detector',frame)

  if cv2.waitKey(1) == ord('q'):
    break

cap.release()
cv2.destroyAllWindows() 