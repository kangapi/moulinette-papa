import os
import time
from shutil import move
import mimetypes
import typer
from rich.progress import Progress
from rich.console import Console
from simple_term_menu import TerminalMenu


console = Console()


def main(from_folder: str = typer.Argument(help="The folder where your files are"),
         to_folder: str = typer.Argument(help="Where you want to move your files")):

    options = ["iPhone5SAnge", "G10", "G10-AmDa", "GoProHero3+", "D500", "iPhone6SAnge", "iPhone7Amelie", "GoProHero9", "Phone11ProMaxJM",
               "iPhoneXRDamien", "DJI-Mini-2", "DJI-Mini-2-Pano", "iPhone11Amelie", "iPhone11Ange", "Canon2000D"]

    terminal_menu = TerminalMenu(options, title="Select your device :", menu_cursor_style=("fg_cyan", "bold"), menu_highlight_style=("bg_cyan", "fg_black"))
    menu_entry_index = terminal_menu.show()

    device_name = options[menu_entry_index]
    print(f"You have selected {device_name}!")

    goodMimeTypes = ["image/jpeg", "image/png", "image/heic", "video/mp4", "video/quicktime", "image/x-adobe-dng",
                     "image/gif", "video/m4v", "video/x-m4v"]

    file_list = os.listdir(from_folder)
    total = len(file_list)

    with Progress() as progress:
        task = progress.add_task("[cyan]Processing files...", total=total)

        good_total = 0
        bad_total = 0

        for file in file_list:
            if mimetypes.guess_type(file)[0] in goodMimeTypes:
                file_path = os.path.join(from_folder, file)
                fileDate = os.path.getmtime(file_path)
                folderDateStr = time.strftime("%Y%m%d", time.localtime(fileDate))
                fileDateStr = time.strftime("%Y%m%d-%H%M%S", time.localtime(fileDate))

                day_folder = os.path.join(to_folder, folderDateStr)
                if not os.path.exists(day_folder):
                    os.makedirs(day_folder)

                new_file_path = os.path.join(day_folder, fileDateStr + "_" + device_name + "_" + file)
                move(file_path, new_file_path)

                good_total += 1
            else:
                bad_folder = os.path.join(to_folder, "- Bad")
                if not os.path.exists(bad_folder):
                    os.makedirs(bad_folder)
                new_file_path = os.path.join(bad_folder, file)
                move(os.path.join(from_folder, file), new_file_path)

                with open(os.path.join(to_folder, "- log.txt"), "a") as log_file:
                    log_file.write(file + "\n")
                bad_total += 1

            progress.update(task, completed=good_total + bad_total)

    print(f"Processed {total} files.")
    console.print(f"[green]{good_total}[/green] videos or photos have correctly been moved.")
    console.print(
        f"[red]{bad_total}[/red] files unsupported, see log file [red]\"- log.txt\"[/red] and [red]\"- Bad\"[/red] folder in the destination directory.")


if __name__ == "__main__":
    typer.run(main)
