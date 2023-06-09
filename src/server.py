from PaperLayout import GeneratePhoto
from Rbg import RemoveBackground
import sys
import os

from websocket_server import WebsocketServer
import logging
server = WebsocketServer(host='127.0.0.1', port=13254, loglevel=logging.INFO)


def create_directory():
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
    
    return os.path.join(documents_folder, "Pascal")


def message_received(client,server, message):
    global images, qtys, img_size, paper_size, bw, bg_color
    print(message)
    if message.startswith("Images:"):
        images = message[7:]
    elif message.startswith("Qty:"):
        qtys = message[4:]
    elif message.startswith("ImgSize:"):
        img_arg_size = message[8:]
        img_size = tuple(float(x) for x in img_arg_size.split(","))
    elif message.startswith("PaperSize:"):
        paper_arg_size = message[10:]
        paper_size = tuple(int(x) for x in paper_arg_size.split(","))
    elif message.startswith("Bw:"):
        bw = message[3:] == "true"
    elif message.startswith("BgColor:"):
        bg_arg_color = message[8:]
        bg_color = tuple(int(x) for x in bg_arg_color.split(","))
    elif message == "start_processing":
        # Process the data when the "StartProcessing" message is received
        print("Starting Processing")
        main_path = create_directory()
        img_output_di = os.path.join(main_path, 'img/')
        paper_output_di = os.path.join(main_path, 'paper/')
        img_max_width = img_size[0] * 300
        img_max_height = img_size[1] * 300
        aspect_ratio = img_max_width / img_max_height
        gap = 50
        bg_rgb = bg_color

        combined_IMAGES = [(filename, quantity) for filename, quantity in zip(images.split(","), qtys.split(","))]

        # Call your functions to process the data
        a = RemoveBackground(combined_IMAGES, aspect_ratio, bg_rgb, img_output_di, bw)
        a.remove()
        GeneratePhoto(paper_size, gap, combined_IMAGES, img_max_width, img_max_height, raw_export=img_output_di, paper_output_di=paper_output_di).export()
        server.send_message(client,"Finished Generation")
        print("FInished Server Generation")

def new_client(client,server):
    print("New Client Connected")
    server.send_message_to_all("New Client Connected")

if __name__ == "__main__":
    images = ""
    qtys = ""
    img_size = (1.1, 1.3)
    paper_size = (2480, 3508)
    bw = False
    bg_color = (255, 0, 0, 0)
    print("Server is Starting")
    

    server.set_fn_new_client(new_client)
    server.set_fn_message_received(message_received)
    server.run_forever()
    
    print("server started")