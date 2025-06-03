from datetime import datetime

from simox_yt2mp3_common_functions import CommonFunctions
from simox_yt2mp3_downloader import Downloader
from simox_yt2mp3_extractor import Extractor
from simox_yt2mp3_file_logger import FileLogger
from simox_yt2mp3_language_support_abstract import AbstractLanguageSupport
from simox_yt2mp3_metadata_assigner import MetadataAssigner
from simox_yt2mp3_options import Options
from simox_yt2mp3_searcher import Searcher
from simox_yt2mp3_stdout_colors import StdOutColors
from simox_yt2mp3_stdout_logger import StdOutLogger

class Processor:
  
  def __init__(
      self, 
      options: Options, 
      std_out_colors: StdOutColors, 
      file_logger: FileLogger, 
      std_out_logger: StdOutLogger, 
      metadata_assigner: MetadataAssigner, 
      language_supports: list[AbstractLanguageSupport], 
      downloader: Downloader, 
      searcher: Searcher, 
      extractor: Extractor,
      common_functions: CommonFunctions,
    ):
    self.options = options
    self.std_out_colors = std_out_colors
    self.file_logger = file_logger
    self.std_out_logger = std_out_logger
    self.metadata_assigner = metadata_assigner
    self.language_supports = language_supports
    self.downloader = downloader
    self.searcher = searcher
    self.extractor = extractor
    self.common_functions = common_functions
    
  def __process_playlist__(self, yt_url):
    self.std_out_logger.print_cyan(f"Started execution for playlist URL {yt_url}")
    self.file_logger.log_error_during_playlist = False
    logger_current_playlist_start = datetime.now()
    # info has id of playlist with title, then entries array. Download for each entry!
    info: dict = self.extractor.extract_info(yt_url)
    entries: list[dict] = info.get("entries")
    cnt = 0
    playlist_filename = ""
        
    for entry in entries:
      filename = self.common_functions.get_correct_output_filename(entry, extension=".mp3")
      
      if self.options.getoption("playlists_in_their_own_directory"):
        playlist_filename = self.common_functions.get_playlist_name_for_filename(entry)
        self.common_functions.create_playlist_dir(playlist_filename)
        filename = self.options.getoption("destination_directory") + playlist_filename + "/" + filename.split(self.options.getoption("destination_directory"))[1]
        
      cnt += 1
      single_song_executed_correctly = self.downloader.download_single_song(entry.get("original_url"), entry, filename, True)
      if single_song_executed_correctly:
        self.std_out_logger.print_green(f"Completed execution for track number {cnt} out of {len(entries)} for playlist URL {yt_url}. Saved file: {filename}")
      else:
        self.std_out_logger.print_red(f"Error occurred while executing for track number {cnt} out of {len(entries)} for playlist URL {yt_url}")
        
    now = datetime.now()
    self.file_logger.log_current_iteration = [
      yt_url, 
      "ERROR" if self.file_logger.log_error_during_playlist else "OK", 
      "ERROR" if self.file_logger.log_error_during_playlist else "OK", 
      self.common_functions.elapsed_time_float_seconds(logger_current_playlist_start, now), 
      (self.options.getoption("destination_directory") + playlist_filename) if self.options.getoption("playlists_in_their_own_directory") else ""
    ]
    self.file_logger.print_log_row_runtime()
    self.file_logger.append_log_iteration()
    
    if self.file_logger.log_error_during_playlist:
      self.std_out_logger.print_red(f"Error occurred during execution for playlist URL {yt_url}")
    else:
      self.std_out_logger.print_green(f"Completed execution for playlist URL {yt_url}")

  def __process_single__(self, yt_url):
    self.std_out_logger.print_cyan(f"Started execution for URL {yt_url}")
    info = self.extractor.extract_info(yt_url)
    filename = self.common_functions.get_correct_output_filename(info, extension=".mp3")
    single_song_executed_correctly = self.downloader.download_single_song(yt_url, info, filename, False)
    if single_song_executed_correctly:
      self.std_out_logger.print_green(f"Completed execution for URL {yt_url}. Saved file: {filename}")
    else:
      self.std_out_logger.print_red(f"Error occurred while executing for URL {yt_url}")
      
  def __handle_url_entry__(self, url):
    if url == "" or url.startswith("#"):
      return None
    
    if self.common_functions.check_url_validity(url):
      return url
    else:
      self.std_out_logger.print_yellow(f"The entry '{url}' does not seem to conform to a YouTube URL with a specified video and/or playlist. If you think that's not the case, then contact the developer. Program will now proceed using the entry as a search term")
      self.std_out_logger.print_cyan(f"Proceding with a search on Youtube Music of the given string '{url}'")
      new_url = self.searcher.search(url)
      if new_url == None:
        self.std_out_logger.print_red(f"Unable to complete search with the string '{url}'. Please use an URL for this specific download")
        self.file_logger.log_search_current_iteration = [url, "UNABLE", ""]
        return None
      else:
        self.std_out_logger.print_green(f"Executed search on Youtube Music of the given string '{url}'. Found the best corresponding result with the following URL: {new_url}")
        self.file_logger.log_search_current_iteration = [url, "OK", new_url]
        return new_url
  
  def process(self, yt_url):
    # url = self.__handle_url_entry__(yt_url)

    # if url == None:
      # return

    # self.file_logger.log_url_single(url)
    # if self.file_logger.log_search_current_iteration != []:
      # self.file_logger.print_log_search_runtime()
      # self.file_logger.append_log_search_iteration_and_clear()

    if self.common_functions.is_playlist(yt_url):
      self.__process_playlist__(yt_url)
    else:
      self.__process_single__(yt_url)

