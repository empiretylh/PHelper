import cv2
from PIL import Image
import rembg
import os
import tempfile

def wmsg(msg):
    temp_file_path = os.path.join(tempfile.gettempdir(), 'pascaltemp.txt')

    # Write data to the temporary file
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write(msg)

class RemoveBackground():

   #images will be array
    def __init__(self,images,aspect_ratio,rgb,output_di,bw=False):
        self.images = images
        self.aspect_ratio = aspect_ratio
        self.rgb = rgb
        self.output_di = output_di
        self.bw = bw
        self.model_name = "silueta"
        self.session = rembg.new_session(model_name=self.model_name)

  

      
    def remove(self):       
        aspect_ratio = self.aspect_ratio
        
        for i in self.images:
            print(i)
           
            imgread = cv2.imread(i[0])
           
            if self.bw:
                rgb = (128,128,128,0)
            else:
                rgb = self.rgb
            
            img = rembg.remove(imgread,bgcolor=rgb)
           
            # Convert the image to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Load the face detector
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

            if face_cascade.empty():
                raise IOError('Unable to load the face cascade classifier xml file')


            # Detect faces in the grayscale image
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            if len(faces) > 0:
                # Calculate the center of the bounding box
                x, y, w, h = faces[0]
                center_x = x + w // 2
                center_y = y + h // 2
                
                # Calculate the width and height of the cropped image
                aspect_ratio = self.aspect_ratio
                if w / h > aspect_ratio:
                    crop_width = int(aspect_ratio * h)
                    crop_height = h
                else:
                    crop_width = w
                    crop_height = int(w / aspect_ratio)
                    
                # Calculate the coordinates of the top-left corner of the cropped image
                margin_x = crop_width // 2
                margin_y = crop_height // 2
                crop_x = max(0, center_x - crop_width // 2 - margin_x)
                crop_y = max(0, center_y - crop_height // 2 - margin_y)

                # Crop the image
                if self.bw:
                    crop_img = gray[crop_y:crop_y+crop_height+margin_y*2, crop_x:crop_x+crop_width+margin_x*2]
                else:
                    crop_img = img[crop_y:crop_y+crop_height+margin_y*2, crop_x:crop_x+crop_width+margin_x*2]
                                
            else:
                print("Face not detect")  
               
            basename = os.path.basename(i[0])
           
            cv2.imwrite(self.output_di+basename,crop_img)
           
# images = {('img.jpg',5)}
# paper_size = (1200,1800)
# gap = 40; # gap between images;

# img_max_width = 1.1 * 300
# img_max_height = 1.3 * 300


# aspect_ratio = img_max_width / img_max_height
# bg_rgb = (255,0,0)
# output_di = 'img/'
# a = RemoveBackground(images,aspect_ratio,bg_rgb,output_di,True)
# a.remove()
