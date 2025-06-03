from datetime import datetime
from functools import reduce
import music_tag
import yt_dlp

from simox_yt2mp3_common_functions import CommonFunctions
from simox_yt2mp3_file_logger import FileLogger
from simox_yt2mp3_language_support_abstract import AbstractLanguageSupport
from simox_yt2mp3_metadata_assigner import MetadataAssigner
from simox_yt2mp3_options import Options
from simox_yt2mp3_stdout_colors import StdOutColors
from simox_yt2mp3_stdout_logger import StdOutLogger

class Downloader:
  
  def __init__(
    self, 
    options: Options, 
    std_out_colors: StdOutColors, 
    file_logger: FileLogger, 
    std_out_logger: StdOutLogger, 
    metadata_assigner: MetadataAssigner, 
    language_supports: list[AbstractLanguageSupport],
    common_functions: CommonFunctions,
  ):
    self.options = options
    self.std_out_colors = std_out_colors
    self.file_logger = file_logger
    self.std_out_logger = std_out_logger
    self.metadata_assigner = metadata_assigner
    self.language_supports = language_supports
    self.common_functions = common_functions
    
  def download_single_song(self, yt_url, info, filename, is_playlist):
    self.file_logger.log_current_iteration = [yt_url]
    self.file_logger.log_current_song_start = datetime.now()
    try:
      self.__download_audio__(yt_url, info, is_playlist)
      self.file_logger.log_current_iteration.append("OK")
    except Exception as e:
      self.std_out_logger.print_red(e)
      self.std_out_logger.print_red(f"ERROR! Unable to download the song for URL '{yt_url}'. Report the error to the developer")
      self.file_logger.log_current_iteration.extend(["ERROR", "", self.common_functions.elapsed_time_float_seconds(self.file_logger.log_current_song_start, datetime.now()), ""])
      self.file_logger.log_error_during_playlist = True
      self.file_logger.print_log_row_runtime()
      self.file_logger.append_log_iteration()
      return False
    try:
      mp3_file = music_tag.load_file(filename)
      self.metadata_assigner.assign_metadata(mp3_file, info)
      self.file_logger.log_current_iteration.append("OK")
    except Exception as e:
      self.std_out_logger.print_red(e)
      self.std_out_logger.print_red(f"ERROR! Unable to write metadata for file '{filename}'. Most likely the file does not exist since some strange characters are present in the filename")
      self.file_logger.log_current_iteration.extend(["ERROR", self.common_functions.elapsed_time_float_seconds(self.file_logger.log_current_song_start, datetime.now()), ""])
      self.file_logger.log_error_during_playlist = True
      self.file_logger.print_log_row_runtime()
      self.file_logger.append_log_iteration()
      return False
    self.file_logger.log_current_iteration.extend([self.common_functions.elapsed_time_float_seconds(self.file_logger.log_current_song_start, datetime.now()), filename])
    self.file_logger.append_log_iteration()
    self.file_logger.print_log_row_runtime()
    return True
  
  def __download_audio__(self, yt_url, info, is_playlist):
    ytdl_opts = {
      "format": "bestaudio/best",
      "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": self.options.getoption("kbps"),
      }],
      # 'outtmpl': get_correct_output_template(info=info),
      "outtmpl": self.common_functions.get_correct_output_filename(info=info, extension=None, playlist_filename=(self.common_functions.get_playlist_name_for_filename(info) + "/" if self.options.getoption("playlists_in_their_own_directory") and is_playlist else "")),
      "noplaylist": not self.options.getoption("allow_playlist"),
      "quiet": self.options.getoption("quiet_stdout"),
      "no_warnings": self.options.getoption("quiet_stdout"),
      "cookiefile": self.options.getoption("cookiefile"),
    }
    with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
      ytdl.download([yt_url])

  