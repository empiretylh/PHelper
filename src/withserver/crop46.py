import cv2
import os

img_max_width = 3.9 * 300
img_max_height = 5.7 * 300

print(img_max_width,img_max_height)
aspect_ratio = int(img_max_width) / int(img_max_height)


def crop_image_with_faces(image_path,aspect_ratio,output_dir,server,client):
    imgread = cv2.imread(image_path)
    # Convert the image from BGR color (OpenCV default) to RGB color
    rgb_image = cv2.cvtColor(imgread, cv2.COLOR_BGR2RGB)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(rgb_image, scaleFactor=1.1, minNeighbors=5)

    aspect_ratio = aspect_ratio

    if len(faces) > 0:
        print('Faces Detected and Crop:', len(faces))

        # Calculate the bounding box that contains all the detected faces
        min_x = min(faces[:, 0])
        min_y = min(faces[:, 1])
        max_x = max(faces[:, 0] + faces[:, 2])
        max_y = max(faces[:, 1] + faces[:, 3])

        # Calculate the current aspect ratio of the bounding box
        width = max_x - min_x
        height = max_y - min_y
        current_ratio = width / height

        if current_ratio > aspect_ratio:
            # Reduce height to match the desired aspect ratio
            new_height = int(width / aspect_ratio) + 5
            margin = (height - new_height) // 3
            min_y += margin
            max_y = min_y + new_height
        else:
            # Reduce width to match the desired aspect ratio
            new_width = int(height * aspect_ratio) + 5
            margin = (width - new_width) // 3
            min_x += margin
            max_x = min_x + new_width

        # Perform cropping
        crop_img = imgread[min_y:max_y, min_x:max_x]
        
        basename = os.path.basename(i[0])
        path = os.path.join(output_dir,basename)
        # Save the cropped image
        cv2.imwrite(path, crop_img)
        server.send_message(client,"BUTY:",path)
        
    else:
        print("No faces detected to crop")
        crop_image_with_aspect_ratio(image_path=image_path,aspect_ratio=aspect_ratio,output_dir=output_dir,server=server,client=client)


def crop_image_with_aspect_ratio(image_path,aspect_ratio,output_dir,server,client):
    img = cv2.imread(image_path)

    target_ratio = aspect_ratio

    image_height, image_width, _ = img.shape
    current_ratio = image_width / image_height

    if current_ratio > target_ratio:
        new_width = int(image_height * target_ratio)
        margin = int((image_width - new_width) / 2)
        img_cropped = img[:, margin:margin + new_width]
    else:
        new_height = int(image_width / target_ratio)
        margin = int((image_height - new_height) / 2)
        img_cropped = img[margin:margin + new_height, :]

    basename = os.path.basename(image_path)
    path = os.path.join(output_dir,basename)
    cv2.imwrite(path, img_cropped)
    server.send_message(client,"BUTY:",path)
    print("Cropped image saved as cropped_image.jpg")



class CropBeauty:
    def __init__(self,images,aspect_ratio,output_dir,facemode=False,server='',client=''):
        self.images = images 
        self.aspect_ratio = aspect_ratio 
        self.output_di = output_dir 
        self.server = server 
        self.client = client 
        self.facemode = facemode

    def crop(self):
        aspect_ratio = self.aspect_ratio 

        for i in self.images:
            if self.facemode:
                crop_image_with_faces(image_path=i,aspect_ratio=aspect_ratio,output_dir=self.output_di,server=self.server,client=self.client)
            else:
                crop_image_with_aspect_ratio(image_path=i,aspect_ratio=aspect_ratio,output_dir=self.output_di,server=self.server,client=self.client)
    
        print("Crop Image Finished")