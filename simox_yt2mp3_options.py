import sys
import os
import re

from simox_yt2mp3_stdout_colors import StdOutColors

std_out_colors = StdOutColors()

class Options:
  
  def __init__(
    self,
    std_out_colors: StdOutColors
  ):
    self.std_out_colors = std_out_colors
  
  options = {
    "no_main_artist": False,
    "no_other_artists": False,
    "no_album": False,
    "allow_playlist": False,
    "no_track_number": False,
    "playlists_in_their_own_directory": False,
    "no_log_files": False,
    "quiet_stdout": False,
    "no_stdout": False,
    "allow_non_squared_covers": False,
    "overwrite_files": False,
    "search_force_candidate_selection": False,
    "enable_free_search": False,
    "disable_search_explicit_first": False,
    "kbps": "320",
    "possible_kbps": [str(v) for v in list(range(96, 320 + 32, 32))], # not settable
    "destination_directory": "downloads/",
    "cookiefile": None,
    "search_limit": 10,
    "search_explicit_limit": 5, # not settable
    "search_csv_delimiter": "|",
    "search_acceptance_ratio": 0.9,
    "general_acceptance_ratio": 0.9,
    "max_res": 720, # not settable
  }

  def __check_cookies_are_conform_to_netscape__(self, cookiefile):
    pattern = re.compile(
      r'^(?P<domain>[^\t]+)\t'
      r'(?P<flag>[^\t]+)\t'
      r'(?P<path>[^\t]+)\t'
      r'(?P<secure>[^\t]+)\t'
      r'(?P<expires>\d+)\t'
      r'(?P<name>[^\t]+)\t'
      r'(?P<value>[^\t]*)$'
    )
    with open(cookiefile, "r") as cookies:
      for cookie in cookies:
        if cookie.strip() == "" or cookie.strip().startswith("#"):
          continue
        if not pattern.match(cookie.strip()):
          return False
      return True

  def getoptions(self):
    return self.options

  def getoption(self, option):
    return self.options[option]
  
  def setoption(self, option_key, option_value):
    self.options[option_key] = option_value

  def __print_red__(self, string_to_print):
    if not self.getoption("no_stdout"):
      print(self.std_out_colors.get_colored_string(string_to_print, StdOutColors.RED))

  def __print_yellow__(self, string_to_print):
    if not self.getoption("no_stdout"):
      print(self.std_out_colors.get_colored_string(string_to_print, StdOutColors.YELLOW))

  def __print_green__(self, string_to_print):
    if not self.getoption("no_stdout"):
      print(self.std_out_colors.get_colored_string(string_to_print, StdOutColors.GREEN))

  def __print_cyan__(self, string_to_print):
    if not self.getoption("no_stdout"):
      print(self.std_out_colors.get_colored_string(string_to_print, StdOutColors.CYAN))

  def __print__(self, string_to_print):
    if not self.getoption("no_stdout"):
      print(string_to_print)
  
  def parse_options(self):
    if "--no-stdout" in sys.argv[1:]:
      self.setoption("no_stdout", True)
      self.setoption("quiet_stdout", True)

    for arg in sys.argv[1:]:
      print_set_option = True
      match arg:
        case "--no-album":
          self.setoption("no_album", True)
          
        case "--allow-playlist":
          self.setoption("allow_playlist", True)
          
        case "--no-track-number":
          self.setoption("no_track_number", True)
          
        case "--playlists-in-their-own-directory":
          self.setoption("playlists_in_their_own_directory", True)
          
        case "--no-log-files":
          self.setoption("no_log_files", True)
          
        case "--quiet-stdout":
          self.setoption("quiet_stdout", True)
          
        case "--allow-non-squared-covers":
          self.setoption("allow_non_squared_covers", True)
          
        case "--allow-non-squared-covers":
          self.setoption("allow_non_squared_covers", True)
          
        # case "--force-accept-search-candidate":
        #   self.setoption("force_accept_search_candidate", True)
        
        case "--overwrite-files":
          self.setoption("overwrite_files", True)
          
        case "--search-force-candidate-selection":
          self.setoption("search_force_candidate_selection", True)
          
        case "--disable-search-explicit-first":
          self.setoption("disable_search_explicit_first", True)
          
        case "--enable-free-search":
          self.setoption("enable_free_search", True)

        case "--no-stdout":
          self.setoption("no_stdout", True)
          
        case arg if arg.startswith("--kbps="):
          kbps_value = arg.split("kbps=")[1]
          if kbps_value in self.getoption("possible_kbps"):
            self.setoption("kbps", kbps_value)
            self.__print_cyan__(f"Set desired kbps to {self.getoption('kbps')} kbps")
          else:
            self.__print_yellow__(f"WARNING: Invalid kbps value. Defaulting to {self.getoption('kbps')} kbps")
          print_set_option = False
          
        case arg if arg.startswith("--cookies="):
          cookiefile = arg.split("cookies=")[1]
          if (os.path.isfile(cookiefile)):
            cookies_conform_to_netscape = self.__check_cookies_are_conform_to_netscape__(cookiefile)
            if cookies_conform_to_netscape:
              self.setoption("cookiefile", cookiefile)
              self.__print_cyan__(f"Set desired cookiefile to '{self.getoption('cookiefile')}'")
            else:
              self.__print_yellow__(f"WARNING: The given cookiefile '{cookiefile}' does not seem to be conform to the NetScape standard; execution will proceed with NO cookies. Please check how the cookies were exported or if you believe there's a code error contact the developer.")
          else:
            self.__print_yellow__(f"WARNING: Invalid cookiefile passed. '{cookiefile}' does not seem to resolve to a file")
          print_set_option = False
          
        case arg if arg.startswith("--search-limit="):
          limit = arg.split("search-limit=")[1]
          print_set_option = False
          try:
            limit = int(limit)
            if limit <= 0:
              raise Exception
            self.setoption("search_limit", limit)
            self.__print_cyan__(f"Set search limit to '{self.getoption('search_limit')}'", StdOutColors.CYAN)
          except Exception as e:
            self.__print_yellow__(f"WARNING: Invalid search limit passed (must be positive integer). Reverting to the standard ({self.getoption('search_limit')})")
            
        case arg if arg.startswith("--search-explicit-limit="):
          limit = arg.split("search-explicit-limit=")[1]
          print_set_option = False
          try:
            limit = int(limit)
            if limit <= 0:
              raise Exception
            self.setoption("search_explicit_limit", limit)
            self.__print_cyan__(f"Set search explicit limit to '{self.getoption('search_explicit_limit')}'")
          except Exception as e:
            self.__print_yellow__(f"WARNING: Invalid search explicit limit passed (must be positive integer). Reverting to the standard ({self.getoption('search_explicit_limit')})")
            
        case arg if arg.startswith("--search-csv-delimiter="):
          delimiter = arg.split("search-csv-delimiter=")[1]
          print_set_option = False
          if len(delimiter) == 1:
            self.setoption("search_csv_delimiter", delimiter)
            self.__print_cyan__(f"Set search CSV delimiter to '{self.getoption('search_csv_delimiter')}'")
          else:
            self.__print_yellow__(f"WARNING: Invalid search CSV delimiter passed. The delimiter has to be a single character; the following was passed: '{self.getoption('search_csv_delimiter')}'")
            
        case arg if arg.startswith("--search-acceptance-ratio="):
          limit = arg.split("search-acceptance-ratio=")[1]
          print_set_option = False
          try:
            limit = float(limit)
            if limit <= 0 or limit > 1:
              raise Exception
            self.setoption("search_acceptance_ratio", limit)
            self.__print_cyan__(f"Set search acceptance ratio to '{self.getoption('search_acceptance_ratio')}'")
          except Exception as e:
            self.__print_yellow__(f"WARNING: Invalid search acceptance ratio passed, it must be between (0, 1]. Reverting to the standard ({self.getoption('search_acceptance_ratio')})")
            
        case arg if arg.startswith("--general-acceptance-ratio="):
          limit = arg.split("general-acceptance-ratio=")[1]
          print_set_option = False
          try:
            limit = float(limit)
            if limit <= 0 or limit > 1:
              raise Exception
            self.setoption("general_acceptance_ratio", limit)
            self.__print_cyan__(f"Set general acceptance ratio to '{self.getoption('general_acceptance_ratio')}'")
          except Exception as e:
            self.__print_yellow__(f"WARNING: Invalid general acceptance ratio passed, it must be between (0, 1]. Reverting to the standard ({self.getoption('general_acceptance_ratio')})")

        case arg if arg.startswith("--destination-directory="):
          desination_directory = arg.split("destination-directory=")[1]
          if not desination_directory.endswith("/"):
            desination_directory += "/"
          self.setoption("destination_directory", desination_directory)
          self.__print_cyan__(f"Set desired destination directory to '{self.getoption('destination_directory')}'")
          print_set_option = False
            
        case _:
          print_set_option = False
          self.__print_red__(f"Unrecognized option '{arg}'. Be sure to check the manual for the available options and thei spelling")
          
      if print_set_option:
        self.__print_cyan__(f"Set option '{arg.split('--')[1]}' to True")

# elif arg == "--no-main-artist":
#   global no_main_artist
#   no_main_artist = True
# elif arg == "--no-other-artists":
#   global no_other_artists
#   no_other_artists = True