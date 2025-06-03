import yt_dlp

from simox_yt2mp3_common_functions import CommonFunctions
from simox_yt2mp3_file_logger import FileLogger
from simox_yt2mp3_options import Options
from simox_yt2mp3_stdout_colors import StdOutColors
from simox_yt2mp3_stdout_logger import StdOutLogger

class Extractor:
  
  def __init__(
    self, 
    options: Options, 
    std_out_colors: StdOutColors, 
    file_logger: FileLogger, 
    std_out_logger: StdOutLogger,
    common_functions: CommonFunctions,
  ):
    self.options = options
    self.std_out_colors = std_out_colors
    self.file_logger = file_logger
    self.std_out_logger = std_out_logger
  
  def extract_info(self, yt_url):
    ytdl_opts = {
      "format": "bestaudio/best",
      "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": self.options.getoption("kbps"),
      }],
      "skip_download": True,
      "noplaylist": not self.options.getoption("allow_playlist"),
      "quiet": self.options.getoption("quiet_stdout"),
      "no_warnings": self.options.getoption("quiet_stdout"),
      "cookiefile": self.options.getoption("cookiefile"),
    }
    with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
      return ytdl.extract_info(yt_url, download=False)