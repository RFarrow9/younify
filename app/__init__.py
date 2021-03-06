from dataclasses import dataclass
import logzero
import typing
import configparser


"""""



"""""

#read the config file first and foremost
config = configparser.ConfigParser()
config.read("resources/config.ini")

# Do this better in future, needs an os agnostic method
log_location = r"C:\Users\robfa\Documents\Git\Younify\temp\log.log"

def setup_logger(__name__: str, file_path: str = log_location, level: int = 10) -> logzero.logger:
    # todo: this should be able to write to lambda/local logs without code change
    logzero.setup_default_logger()
    logzero.logfile(file_path, maxBytes=int(1e6))
    logzero.loglevel(level)
    return logzero.logger


spotify_dir = r"C:\Users\robfa\Documents\Git\Younify" # feck me remove this
youtube_options = {
            'format': 'bestaudio/best',  # choice of quality
            'extractaudio': True,  # only keep the audio
            'noplaylist': True,  # only download single song, not playlist
            'outtmpl': f"{spotify_dir}\%(title)s.%(ext)s",
            'quiet': True
        }


#set up spotify things
# username = config["spotify"]["username"]
# scope = config["spotify"]["scope"]
# client_id = config["spotify"]["client_id"]
# client_secret = config["spotify"]["client_secret"]
# redirect_uri = config["spotify"]["redirect_uri"]

