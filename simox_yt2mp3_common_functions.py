import difflib
from functools import reduce
import os
import re

from simox_yt2mp3_language_support_abstract import AbstractLanguageSupport
from simox_yt2mp3_options import Options
from simox_yt2mp3_stdout_colors import StdOutColors

class CommonFunctions:
  
  def __init__(
      self, 
      options: Options, 
      std_out_colors: StdOutColors,
      language_supports: list[AbstractLanguageSupport],  
    ):
    self.options = options
    self.std_out_colors = std_out_colors
    self.language_supports = language_supports
    
  def apply_language_supports(self, filename):
    return reduce(lambda s, f: f(s), [language_support.translate_regex for language_support in self.language_supports], filename)
    # for language_support in language_supports:
      # filename = language_support.translate_regex(filename)
    # return filename  

  def is_music(self, info: dict):
    return info.get("artists") != None and info.get("track") != None

  def is_similar_string(self, a, b, acceptable_ratio):
    if a == None or b == None:
      return False
    return difflib.SequenceMatcher(None, a, b).ratio() >= acceptable_ratio
  
  def is_similar_string_case_insensitive(self, a, b, acceptable_ratio):
    if a == None or b == None:
      return False
    a = a.lower()
    b = b.lower()
    return difflib.SequenceMatcher(None, a, b).ratio() >= acceptable_ratio
    
  def elapsed_time_float_seconds(self, start, end):
    return (end - start).total_seconds()

  def get_default_extension(self, extension):
    if extension == None:
      return ".%(ext)s"
    else:
      return extension

  def normalize_filename(self, filename):
    # windows illegals:
    # < (less than)
    # > (greater than)
    # : (colon - sometimes works, but is actually NTFS Alternate Data Streams)
    # " (double quote)
    # / (forward slash)
    # \ (backslash)
    # | (vertical bar or pipe)
    # ? (question mark)
    # * (asterisk)
    # 0-31 (ASCII control characters)
    # CON, PRN, AUX, NUL, COM1, COM2, COM3, COM4, COM5, COM6, COM7, COM8, COM9, LPT1, LPT2, LPT3, LPT4, LPT5, LPT6, LPT7, LPT8, LPT9
    # Filenames cannot end in a space or dot.

    # linux illegals:
    # / (forward slash)
    # 0 (NULL byte)
    # .  (special name referring to current directory)
    # .. (special name referring to parent directory)

    filename = re.sub(r"[^\x20-\x7F]+", "", filename, 0) # replace all non-ASCII between 32 and 255
    filename = re.sub(r"[<>:\?\*\"]", "", filename, 0) # replace deletable illegal tokens
    filename = re.sub(r"[/\\|⧸]", " ", filename, 0) #replace all characters we want to be spaced instead of eliminated
    return filename

  def get_option_no_album_filename(self, album: str):
    if self.options.getoption("no_album"):
      return ""
    else:
      return album.strip() + " - "
    
  def get_option_no_track_number_filename(self, info: dict):
    if self.options.getoption("no_track_number"):
      return ""
    album = info.get("album")
    playlist = info.get("playlist")
    prefixed_album = "Album - " + str(album)
    if album != None and (album == playlist or prefixed_album == playlist or self.is_similar_string(album, playlist, self.options.getoption("general_acceptance_ratio")) or self.is_similar_string(prefixed_album, playlist, self.options.getoption("general_acceptance_ratio"))):
      playlist_index = info.get("playlist_index")
      playlist_count = info.get("playlist_count")
      if playlist_index == None or playlist_count == None:
        return ""
      playlist_len_zeroes = max(len(str(playlist_count)), 2)
      return str(playlist_index).rjust(playlist_len_zeroes, "0") + " "
    return ""

  def get_output_filename_for_music(self, info: dict, extension, playlist_filename):
    artists = info.get("artists")
    main_artist = artists[0]
    album = info.get("album")
    track = info.get("track")
    other_artists = artists[1:]
    other_artists_string = ""
    if len(other_artists) > 0 and not "(feat." in track:
      other_artists_string = " (feat. " + ", ".join(other_artists) + ")"
    extension = self.get_default_extension(extension)
    return self.options.getoption("destination_directory") + playlist_filename + self.normalize_filename(self.apply_language_supports(self.get_option_no_album_filename(album) + main_artist.strip() + " - " + self.get_option_no_track_number_filename(info) + track.strip() + other_artists_string)) + extension

  def get_output_filename_for_not_music(self, info: dict, extension, playlist_filename):
    title = info.get("title")
    extension = self.get_default_extension(extension)
    if " - " in title:
      return self.options.getoption("destination_directory") + playlist_filename + self.normalize_filename(self.apply_language_supports(title.strip())) + extension
    else:
      channel = info.get("channel")
      return self.options.getoption("destination_directory") + playlist_filename + self.normalize_filename(self.apply_language_supports(channel.strip() + " - " + title.strip())) + extension
    
  def filename_already_exists(self, filename):
    return os.path.exists(f"{filename}")
    
  def get_new_filename_if_already_exists(self, filename, extension):
    if self.options.getoption("overwrite_files"):
      return filename
    
    expected_extension = ".%(ext)s" if extension == None else ".mp3"
    if ".%(ext)s" in filename:
      filename = filename.replace(".%(ext)s", ".mp3")

    original_filename_no_extension = filename.split(".mp3")[0]
    cnt = 0
    while (self.filename_already_exists(filename)):
      cnt += 1
      # print(f"The filename '{filename}' already exists. Trying with a copy (copy count is {cnt})")
      filename = original_filename_no_extension + " (" + str(cnt) + ").mp3"
      # print(f"Tryng with the following filename '{filename}'")
    new_filename = ".".join(filename.split(".")[:-1]) + expected_extension
    # print(f"The filename for the copy is '{new_filename}'")
    return new_filename
    
  def get_correct_output_filename(self, info, extension=None, playlist_filename=""):
    filename = ""
    if self.is_music(info):
      filename = self.get_output_filename_for_music(info, extension, playlist_filename)
    else:
      filename = self.get_output_filename_for_not_music(info, extension, playlist_filename)
    return self.get_new_filename_if_already_exists(filename, extension)

  def get_playlist_name_for_filename(self, info: dict): #pass the first song's info (?)
    album = info.get("album")
    playlist = info.get("playlist")
    prefixed_album = "Album - " + str(album)
    artists = info.get("artists")
    if album != None and artists != None and (album == playlist or prefixed_album == playlist or self.is_similar_string(album, playlist, self.options.getoption("general_acceptance_ratio")) or self.is_similar_string(prefixed_album, playlist, self.options.getoption("general_acceptance_ratio"))):
      return self.normalize_filename(self.apply_language_supports(artists[0] + " - " + album))
    else:
      return self.normalize_filename(self.apply_language_supports(playlist))
    
  def is_playlist(self, url):
    return "playlist?" in url
  
  def create_playlist_dir(self, playlist_filename):
    if not os.path.exists(f"{self.options.getoption('destination_directory')}{playlist_filename}"):
      os.mkdir(f"{self.options.getoption('destination_directory')}{playlist_filename}")

  def create_destination_dir(self):
    if not os.path.exists(f"{self.options.getoption('destination_directory')}"):
      os.mkdir(f"{self.options.getoption('destination_directory')}")

  def create_main_log_dir(self):
    if not os.path.exists(f"logs"):
      os.mkdir(f"logs")

  def create_log_dir(self, log_program_start_string):
    if not os.path.exists(f"logs/logs {log_program_start_string}"):
      os.mkdir(f"logs/logs {log_program_start_string}")

  def check_url_validity(self, url):
    regex_match = re.match(r"^http(s)?:\/\/(((www\.)?youtube|music\.youtube)\.com\/((watch\?v=[a-zA-Z0-9\-_]{11})(&list=[a-zA-Z0-9\-_]+)?|playlist\?list=[a-zA-Z0-9\-_]+)|youtu\.be\/[a-zA-Z0-9\-_]{11}(&si=[a-zA-Z0-9\-_]+)?)$", url)
    return regex_match != None