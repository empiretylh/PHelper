from PIL import Image
import math
import os
from datetime import datetime

class GeneratePhoto:
    def __init__(self, paper_size, gap, images, img_max_width, img_max_height, raw_export, paper_output_di):
        self.paper_size = paper_size
        self.gap = gap
        self.images = images
        self.img_max_width = img_max_width
        self.img_max_height = img_max_height
        self.raw_export = raw_export
        self.paper_output_di = paper_output_di
        print(images)
	
	
    def deleteimage(self, file_path):
        # Check if the file exists before deleting
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
            print("File deleted successfully.")
        else:
            print("File does not exist.")

    def export(self):
        paper_size = self.paper_size
        gap = self.gap
        images = self.images	
        img_max_width = self.img_max_width
        img_max_height = self.img_max_height

        # Calculate the images that fit inside the paper
        limited_img_xaxis = int(paper_size[0] / (img_max_width + gap))
        limited_img_yaxis = int(paper_size[1] / (img_max_height + gap))
        limited_paper_images = limited_img_xaxis * limited_img_yaxis

        img_qty = sum(int(count) for _, count in images)
        paper_qty = math.ceil(img_qty / limited_paper_images)

        sets = []  # Initialize an empty list of sets
        current_set = []  # Initialize an empty list to hold the images for the current set

        # Iterate over the images
        for name, count in images:
            # Add the current image to the current set count times
            for _ in range(int(count)):
                # If adding the current image would exceed the limit, add the current set to the list of sets and start a new set
                if len(current_set) == limited_paper_images:
                    sets.append(current_set)
                    current_set = []
                current_set.append(name)

        # Add the last set to the list of sets
        if current_set:
            sets.append(current_set)

        count_set = []

        for set in sets:
            name_counts = {}
            for name in set:
                if name in name_counts:
                    name_counts[name] += 1
                else:
                    name_counts[name] = 1
            count_set.append(name_counts)

        print(count_set)

        pname = 0

        for p in count_set:
            a4_image = Image.new('RGB', paper_size, color='white')

            # Get the current date and time
            date_time_string = datetime.now().strftime("%Y%m%d_%H%M%S")

            values_list = list(p.values())
            key_list = list(p.keys())

            imgs_sum = sum(values_list)
            index = 0

            print('Img:', os.path.join(self.raw_export, os.path.basename(key_list[index])))

            img = Image.open(os.path.join(self.raw_export, os.path.basename(key_list[index])))
            # img.thumbnail((img_max_width, img_max_height), resample=Image.BICUBIC)
            img = img.resize((int(img_max_width),int(img_max_height)),resample=Image.BICUBIC) 

            positions = []
            for a in range(imgs_sum):
                x_pos = a % limited_img_xaxis
                y_pos = a // limited_img_xaxis
                print(f"({x_pos}, {y_pos})")

                position = (
                    int(x_pos * img_max_width) + (gap * x_pos) + gap,
                    int(y_pos * img_max_height) + (gap * y_pos) + gap
                )
                a4_image.paste(img,position)

                if a == sum(values_list[:index + 1]) - 1:
                    index += 1
                    try:
                        img = Image.open(os.path.join(self.raw_export, os.path.basename(key_list[index])))
                        img = img.resize((int(img_max_width),int(img_max_height)),resample=Image.BICUBIC) 
                        # img.thumbnail((img_max_width, img_max_height), resample=Image.BICUBIC)
                    except IndexError:
                        print(IndexError)

            pn = str(pname)

            pname += 1
            pathname = os.path.join(self.paper_output_di, "p_"+pn+"_" + date_time_string + '.jpg')
            a4_image.save(pathname)

            print(pathname)
