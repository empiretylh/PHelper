from PaperLayout import GeneratePhoto
from Rbg import RemoveBackground
import sys
import os

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


def getData():
	line  = sys.stdin.readline()
	return line.strip()


while True:
	print("Import Images")
	images = getData()

	if not images:
		break
	else:
		images = images.replace('"','')

	print("Import Qty")
	qtys = getData()

	if not qtys:
		break

	image = images.split(",")
	qty = qtys.split(",")

	combined_IMAGES = [(filename, quantity) for filename, quantity in zip(image, qty)] ## convert to (img.jpg,qty)

	print("Image Size")
	img_arg_size =  getData()
	if not img_arg_size:
		img_arg_size = "1.1,1.3"

	img_size = tuple(float(x) for x in img_arg_size.split(","))

	print("Paper Size")
	paper_arg_size = getData()

	if not paper_arg_size:
		paper_arg_size = "2480,3508"

	paper_size = tuple(int(x) for x in paper_arg_size.split(","))


	print("B or W")

	bw = getData()

	if not bw:
		bw = False

	if bw == "true":
		bw = True
	else:
		bw = False
	
	print("BG Color")

	bg_arg_color = getData()
	
	if not bg_arg_color:
		bg_arg_color = "255,0,0,0"

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

	print('msg:' + 'Finished Remove Background and Crop')

	GeneratePhoto(paper_size,gap, combined_IMAGES,img_max_width,img_max_height,raw_export=img_output_di,paper_output_di=paper_output_di).export()

	print('msg:' + "Finished Paper Layout")


	print("o:Completed")
	sys.stdout.flush()
