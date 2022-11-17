import time
from Camera import Camera 

def main():
    cam = Camera()

    end = time.perf_counter() + 10

    compteur_frame = 0
    frame_precendente = None
    while end > time.perf_counter():
        compteur_frame +=1

        img_gris = cam.convert_to_grayscale(cam.obtenir_image())

        #cheque si le compyeur est pair
        if((compteur_frame % 2) == 0):