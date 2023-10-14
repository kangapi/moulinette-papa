import os
import time
from shutil import move
import mimetypes
import typer
from rich.progress import track
from rich.console import Console
console = Console()

def main(from_folder: str = typer.Argument(help="The folder where your files are"),
         to_folder: str = typer.Argument(help="Where you want to move your files"),
         device_name: str = typer.Argument(help="The name of the device")):

    console.print("[blue]Looks like a link")

    total = 0
    good_total = 0
    bad_total = 0

    for value in track(range(100), description="Processing..."):

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

                good_total += 1

            else:
                # Move the file to a folder called "bad"
                bad_folder = os.path.join(to_folder, "bad")
                if not os.path.exists(bad_folder):
                    os.makedirs(bad_folder)
                new_file_path = os.path.join(bad_folder, file)
                move(from_folder + "/" + file, new_file_path)
                # Log into a file
                with open(to_folder + "/-log.txt", "a") as log_file:
                    log_file.write(file + "\n")

                bad_total += 1

            total += 1
    print(f"Processed {total} files.")
    console.print(f"[green]{good_total}[/green] videos or photos have correctly been moved.")
    console.print(f"[red]{bad_total}[/red] files unsupported (see log file (-log.txt) and \"bad\" folder in the destination directory).")

if __name__ == "__main__":
    typer.run(main)
