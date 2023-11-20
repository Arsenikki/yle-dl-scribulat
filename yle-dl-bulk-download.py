import subprocess
import os
import time

inputUrlFile = "urls.txt"
outputPath = "./downloads"

def download_videos():
    print("Starting YLE Areena bulk downloader")

    # Open the file containing URLs
    with open(inputUrlFile, 'r') as file:
        for url in file:
            url = url.strip()
            print("-------------------")
            print(f"Downloading: '{url}'")
            print("with container id:")
            
            # Download the video using subprocess
            subprocess.run(["docker", "run", "--rm", "-d", f"-u={os.getuid()}:{os.getgid()}", f"-v{os.getcwd()}/{outputPath}:/out", "taskinen/yle-dl", url])
            time.sleep(10)  # To avoid overwhelming the system
    
    print("Download complete!")

download_videos()