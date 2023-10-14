import os
import time
from shutil import move
import mimetypes
import typer

def main(from_folder: str = typer.Argument(help="The folder where your files are"),
         to_folder: str = typer.Argument(help="Where you want to move your files"),
         device_name: str = typer.Argument(help="The name of the device")):

    typer.echo(f"Moving files from {from_folder} to {to_folder} with device name {device_name}")

    goodMimeTypes = ["image/jpeg", "image/png", "image/heic", "video/mp4", "video/quicktime", "image/x-adobe-dng",
                     "image/gif", "video/m4v", "video/x-m4v"]

    for file in os.listdir(from_folder):

        if mimetypes.guess_type(file)[0] in goodMimeTypes:

            file_path = os.path.join(from_folder, file)
            fileDate = os.path.getmtime(file_path)
            folderDateStr = time.strftime("%Y%m%d", time.localtime(fileDate))
            fileDateStr = time.strftime("%Y%m%d%H%M%S", time.localtime(fileDate))

            # Crée un répertoire pour la date correspondante s'il n'existe pas
            day_folder = os.path.join(to_folder, folderDateStr)
            if not os.path.exists(day_folder):
                os.makedirs(day_folder)

            # Déplace le fichier dans le répertoire correspondant en le renommant
            new_file_path = os.path.join(day_folder, fileDateStr + "_" + device_name + "_" + file)
            move(file_path, new_file_path)
            print(f"Moved {file} to {new_file_path}")

        else:
            print(f"Skipping {file} because it is not in the list of good mime types")

if __name__ == "__main__":
    typer.run(main)
