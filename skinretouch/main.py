import cv2
import numpy as np

def skin_retouching(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to the LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # Split the LAB image into channels
    l, a, b = cv2.split(lab)

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to the L channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_eq = clahe.apply(l)

    # Merge the equalized L channel with the original a and b channels
    lab_eq = cv2.merge((l_eq, a, b))

    # Convert the LAB image back to the BGR color space
    result = cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)

    # Apply bilateral filtering to smooth the skin texture while preserving the edges
    smoothed = cv2.bilateralFilter(result, d=9, sigmaColor=75, sigmaSpace=75)

    # Combine the original image and the smoothed image using a mask
    mask = cv2.absdiff(result, smoothed)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)
    result = cv2.bitwise_and(image, image, mask=mask)
    result = cv2.add(result, smoothed)

    return result

# Example usage
input_image_path = 'photo_2023-06-10_09-52-10.jpg'
output_image = skin_retouching(input_image_path)
cv2.imshow('Original', cv2.imread(input_image_path))
cv2.imshow('Retouched', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
