import cv2
import os
import rembg
import sys

class RemoveBackground:
    def __init__(self, images, aspect_ratio, rgb, output_dir, bw=False):
        self.images = images
        self.aspect_ratio = aspect_ratio
        self.rgb = rgb
        self.output_dir = output_dir
        self.bw = bw
        self.model_name = "silueta"
        self.session = rembg.new_session(model_name=self.model_name)
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        if self.face_cascade.empty():
            raise IOError('Unable to load the face cascade classifier xml file')

    def remove(self):
        aspect_ratio = self.aspect_ratio

        for i in self.images:
            print(i)
            imgread = cv2.imread(i[0])

            if self.bw:
                imgread = cv2.cvtColor(imgread, cv2.COLOR_BGR2GRAY)
                rgb = (128,128,128,0)
            else:
                rgb = self.rgb

            img = rembg.remove(imgread, bgcolor=rgb)

            faces = self.face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)

            if len(faces) > 0:
                x, y, w, h = faces[0]
                center_x = x + w // 2
                center_y = y + h // 2

                if w / h > aspect_ratio:
                    crop_width = int(aspect_ratio * h)
                    crop_height = h
                else:
                    crop_width = w
                    crop_height = int(w / aspect_ratio)

                margin_x = crop_width // 2
                margin_y = crop_height // 2
                crop_x = max(0, center_x - crop_width // 2 - margin_x)
                crop_y = max(0, center_y - crop_height // 2 - margin_y)

                crop_img = img[crop_y:crop_y+crop_height+margin_y*2, crop_x:crop_x+crop_width+margin_x*2]

            else:
                print("Face not detected")
                sys.stdout.flush()

            basename = os.path.basename(i[0])
            cv2.imwrite(os.path.join(self.output_dir, basename), crop_img)
            print('o:'+os.path.join(self.output_dir, basename))
            sys.stdout.flush()

