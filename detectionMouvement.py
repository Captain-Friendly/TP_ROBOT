import time
from Camera import Camera 
import cv2
import numpy as np

def main():
    cam = Camera()

    end = time.perf_counter() + 10

    compteur_frame = 0
    frame_precendente = None
    while True:
        compteur_frame +=1
        img = cam.obtenir_image()
        frame_actuelle = cam.convert_to_grayscale(img)
        #cheque si le compyeur est pair
        if((compteur_frame % 2) == 0):
            frame_actuelle = cv2.GaussianBlur(src=frame_actuelle, ksize=(5,5), sigmaX=0)
            
            
            if(frame_precendente is None):
                #si on a pas de frame precendete, on skip le reste du while
                frame_precendente = frame_actuelle
                continue
            
            differences = cv2.absdiff(src1=frame_precendente, src2=frame_actuelle)
            frame_precendente = frame_actuelle

            # I dont even know what this does
            kernel = np.ones((5, 5))
            differences = cv2.dilate(differences, kernel, 1)

            # prend les differences d'une taille minimum
            differences_min =  cv2.threshold(src=differences, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]


            contours, _ = cv2.findContours(image=differences_min, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(image=img, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

            for contour in contours:
                if cv2.contourArea(contour) < 50:
                    # too small: skip!
                    continue
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=2)

            cv2.imshow('Motion detector', img)

            if cv2.waitKey(1) == ord('x'):
                break