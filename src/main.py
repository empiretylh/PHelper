from PaperLayout import GeneratePhoto
from Rbg import RemoveBackground
import sys
import os

# images = {('img2.jpg',12)}
# aspect_ratio = 1.1 / 1.3
# bg_rgb = (0,0,255,0)
# output_di = 'img/'
# bw = False

# a = RemoveBackground(images,aspect_ratio,bg_rgb,output_di,bw)
# a.remove()

# print('Finished........................... Removing')

# paper_size = (2480,3508)
# gap = 50; # gap between images;

# img_max_width = 1.1 * 300
# img_max_height = 1.3 * 300
# a = GeneratePhoto(paper_size,gap,images,img_max_width,img_max_height,raw_export=output_di)

# a.export()

# image, quantity, img_size, paper_size, bw, bg_color


def createDirectory():
	# Get the user's home directory
	home_dir = os.path.expanduser("~")

	# Specify the Documents folder path for different operating systems
	documents_folder = ""
	if os.name == "posix":  # Linux or macOS
	    documents_folder = os.path.join(home_dir, "Documents")
	elif os.name == "nt":  # Windows
	    documents_folder = os.path.join(home_dir, "Documents")
	
	# Create the directory if it doesn't exist
	directory1 = os.path.join(documents_folder, "Pascal/img")
	directory2 = os.path.join(documents_folder, "Pascal/paper")
	
	os.makedirs(directory1, exist_ok=True)
	os.makedirs(directory2, exist_ok=True)
	print('Created Directory')
	
	return os.path.join(documents_folder,"Pascal")


if __name__ == '__main__':
    args = sys.argv[1:]

    images = args[0]  # IMAGES
    qty = args[1]     # QUANTITY

  
    image = images.split(",")
    qty = qty.split(",")


    combined_IMAGES = [(filename, quantity) for filename, quantity in zip(image, qty)] ## convert to (img.jpg,qty)

    img_arg_size = args[2] if len(args) > 2 else "1.1,1.3" # Get Image Size arg[2]
    img_size = tuple(float(x) for x in img_arg_size.split(","))

    #Paper --------------------------------------- arg[3]
    paper_arg_size = args[3] if len(args) > 3 else "2480,3508"

    paper_size = tuple(int(x) for x in paper_arg_size.split(","))

    # Black and White ----------------------- arg[4]
    bw = args[4] if len (args) > 4 else True

    if bw == "True":
        bw = True
    else:
        bw = False

    # Background Color --------------------- arg[5]
    bg_arg_color = args[5] if len(args) > 5 else "255,0,0,0" # BGR
    bg_color = tuple(int(x) for x in bg_arg_color.split(","))
    
    mainpath = createDirectory()
    
    img_output_di = mainpath+'/img/'
    paper_output_di = mainpath+'/paper/'


    img_max_width = img_size[0] * 300
    img_max_height = img_size[1] * 300

    print(img_max_width,img_max_height)
    aspect_ratio = int(img_max_width) / int(img_max_height)

    gap = 50; # gap between images;

    bg_rgb = bg_color
    
    
    
   
        

    a = RemoveBackground( combined_IMAGES,aspect_ratio,bg_rgb,img_output_di,bw)
    a.remove()


    GeneratePhoto(paper_size,gap, combined_IMAGES,img_max_width,img_max_height,raw_export=img_output_di,paper_output_di=paper_output_di).export()


    print("Generate Finished")



