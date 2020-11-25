import cv2
img = cv2.imread('mark.png',cv2.IMREAD_COLOR)
new_img = img[:6,:6,:]
for i in range(3):
	for x in range(6):
		for y in range(6):

			new_img[x,y,i] = 1
cv2.imwrite('mmy_marker.png',new_img)