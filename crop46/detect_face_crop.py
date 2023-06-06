import cv2
import os

imgread = cv2.imread('photo.jpg')
# Convert the image from BGR color (OpenCV default) to RGB color
rgb_image = cv2.cvtColor(imgread, cv2.COLOR_BGR2RGB)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
faces = face_cascade.detectMultiScale(rgb_image, scaleFactor=1.1, minNeighbors=5)

img_max_width = 3.9 * 300
img_max_height = 5.7 * 300

print(img_max_width,img_max_height)
aspect_ratio = int(img_max_width) / int(img_max_height)

def crop_image_with_faces(image_path):
    imgread = cv2.imread(image_path)
    # Convert the image from BGR color (OpenCV default) to RGB color
    rgb_image = cv2.cvtColor(imgread, cv2.COLOR_BGR2RGB)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(rgb_image, scaleFactor=1.1, minNeighbors=5)

    img_max_width = int(4 * 300)  # Assuming 300 pixels per inch (PPI)
    img_max_height = int(6 * 300)

    print(img_max_width, img_max_height)
    aspect_ratio = img_max_width / img_max_height

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

        # Save the cropped image
        cv2.imwrite("cropped_image_with_face_detect.jpg", crop_img)

        print("Cropped image saved as cropped_image.jpg")

    else:
        print("No faces detected to crop for 4x6 inches")

# Specify the path to your input image
image_path = "photo.jpg"

# Call the function to crop the image
crop_image_with_faces(image_path)


def crop_image_with_aspect_ratio(image_path):
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

    cv2.imwrite("cropped_image_with_aspect_ratio.jpg", img_cropped)
    print("Cropped image saved as cropped_image.jpg")

# Specify the path to your input image
image_path = "photo.jpg"

# Call the function to crop the image
crop_image_with_aspect_ratio(image_path)
