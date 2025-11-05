import csv
from ytmusicapi import YTMusic
from simox_yt2mp3_common_functions import CommonFunctions
from simox_yt2mp3_file_logger import FileLogger
from simox_yt2mp3_options import Options
from simox_yt2mp3_stdout_colors import StdOutColors
from simox_yt2mp3_stdout_logger import StdOutLogger

class Searcher:
  
  __yt_music__ = YTMusic()
  __youtube_base_href_video__ = "https://music.youtube.com/watch?v="
  __youtube_base_href_playlist__ = "https://music.youtube.com/playlist?list="
  
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
    self.common_functions = common_functions
    
  def __is_acceptable_candidate_song__(self, candidate_info: dict, artist, song, acceptable_ratio):
    info_artist = candidate_info.get("artists")[0].get("name") # TOFIX maybe this can be done better or with variants
    info_song = candidate_info.get("title")
    return self.common_functions.is_similar_string_case_insensitive(artist, info_artist, acceptable_ratio) and self.common_functions.is_similar_string_case_insensitive(song, info_song, acceptable_ratio)

  def __is_acceptable_candidate_album__(self, candidate_info: dict, artist, album, acceptable_ratio):
    info_artist = candidate_info.get("artists")[0].get("name") # TOFIX maybe this can be done better or with variants
    info_album = candidate_info.get("title")
    return self.common_functions.is_similar_string_case_insensitive(artist, info_artist, acceptable_ratio) and self.common_functions.is_similar_string_case_insensitive(album, info_album, acceptable_ratio)

  def __is_acceptable_candidate_playlist__(self, candidate_info: dict, author, playlist, acceptable_ratio):
    info_author = candidate_info.get("author") # TOFIX maybe this can be done better or with variants
    info_playlist = candidate_info.get("title")
    return self.common_functions.is_similar_string_case_insensitive(author, info_author, acceptable_ratio) and self.common_functions.is_similar_string_case_insensitive(playlist, info_playlist, acceptable_ratio)
  
  def __get_correct_href_from_result_type__(self, candidate_info: dict):
    result_type = candidate_info.get("resultType")
    match result_type:
      case result_type if result_type in ["album", "playlist"]:
        return self.__youtube_base_href_playlist__ + candidate_info.get("playlistId")
      case result_type if result_type in ["song", "video"]:
        return self.__youtube_base_href_video__ + candidate_info.get("videoId")
      case result_type if result_type in ["artist", "podcast"]:
        self.std_out_logger.print_yellow(f"Found '{result_type}' as result type. I don't really know what to do with this result type, so I will skip this iteration")
      case _:
        self.std_out_logger.print_yellow(f"Found '{result_type}' as result type. This is an unexpected value, please report it to the developer")
    return None

  def __get_correct_id_from_result_type__(self, candidate_info: dict):
    result_type = candidate_info.get("resultType")
    match result_type:
      case result_type if result_type in ["album", "playlist"]:
        return candidate_info.get("playlistId")
      case result_type if result_type in ["song", "video"]:
        return candidate_info.get("videoId")
    return None
  
  def __get_search_values_from_csvlike__(self, search_string: str):
    reader = csv.reader(search_string.lower().strip().splitlines(), delimiter=self.options.getoption("search_csv_delimiter"))
    values = next(reader)
    if len(values) == 2:
      artist, song_or_album = values[0], values[1]
      return artist, song_or_album, "songs"
    elif len(values) == 3:
      artist, song_or_album, search_type = values[0], values[1], values[2]
      if search_type == "P" or search_type == "p":
        search_type = "playlists"
      elif search_type == "A" or search_type == "a":
        search_type = "albums"
      elif search_type == "S" or search_type == "s" or search_type == "":
        search_type = "songs"
      else:
        self.std_out_logger.print_yellow(f"Unrecognized character expressing search type. Expecting either ['S', 's', ''] for a song search, ['A', 'a'] for album search and ['P', 'p'] for playlist search. Proceding with song search (default)")
        search_type = "songs"
      return artist, song_or_album, search_type
    else:
      self.std_out_logger.print_red(f"Invalid search string. Search format is: ARTIST{self.options.getoption('search_csv_delimiter')}SONG/ALBUM/PLAYLIST{self.options.getoption('search_csv_delimiter')}TYPE OF SEARCH [S, A, P] (optional)")
      self.std_out_logger.print_cyan(f"If you're trying to use the free search, please pass the following option: 'enable-free-search'!")
      return None, None, None
  
  def __search_for_song__(self, artist, song, search_string):
    candidates = self.__yt_music__.search(f"{artist} - {song}", filter="songs", limit=self.options.getoption("search_limit"))
    self.std_out_logger.print_cyan(f"Processing search candidates (songs)")

    candidate_counter = 0
    if not self.options.getoption("disable_search_explicit_first"):
      for candidate in candidates[:self.options.getoption("search_explicit_limit")]:
        candidate_counter += 1
        if not candidate.get("isExplicit"):
          continue
        # print(std_out_colors.get_colored_string(f"Processing search candidate {candidate_counter} with ID {candidate.get("videoId")}", StdOutColors.CYAN))
        if self.__is_acceptable_candidate_song__(candidate, artist, song, self.options.getoption("search_acceptance_ratio")):
          self.std_out_logger.print_green(f"Candidate {candidate_counter} '{candidate.get('artists')[0].get('name')} - {candidate.get('title')}' (explicit) is acceptable. Its ID is: {candidate.get('videoId')}")
          return self.__youtube_base_href_video__ + candidate.get("videoId")
        
    candidate_counter = 0
    for candidate in candidates:
      candidate_counter += 1
      # print(std_out_colors.get_colored_string(f"Processing search candidate {candidate_counter} with ID {candidate.get("videoId")}", StdOutColors.CYAN))
      if self.__is_acceptable_candidate_song__(candidate, artist, song, self.options.getoption("search_acceptance_ratio")):
        self.std_out_logger.print_green(f"Candidate {candidate_counter} '{candidate.get('artists')[0].get('name')} - {candidate.get('title')}' is acceptable. Its ID is: {candidate.get('videoId')}")
        return self.__youtube_base_href_video__ + candidate.get("videoId")
      
    if self.options.getoption("search_force_candidate_selection"):
      candidate = candidates[0]
      self.std_out_logger.print_yellow(f"Forced selection to candidate '{candidate.get('artists')[0].get('name')} - {candidate.get('title')}' with ID {candidate.get('videoId')} because of the 'search-force-candidates-selection' option. This can lead to errors")
      return self.__youtube_base_href_video__ + candidates[0].get("videoId")
    
    self.std_out_logger.print_red(f"Unable to find a valid candidate for the search string '{search_string}'. Not forcing because the option 'search-force-candidates-selection' hasn't been passed (this is safer than using the option though)")
    return None

  def __search_for_album__(self, artist, album, search_string):
    candidates = self.__yt_music__.search(f"{artist} - {album}", filter="albums", limit=self.options.getoption("search_limit"))
    self.std_out_logger.print_cyan(f"Processing search candidates (albums)")

    candidate_counter = 0
    if not self.options.getoption("disable_search_explicit_first"):
      for candidate in candidates[:self.options.getoption("search_explicit_limit")]:
        candidate_counter += 1
        if not candidate.get("isExplicit"):
          continue
        # print(std_out_colors.get_colored_string(f"Processing search candidate {candidate_counter} with ID {candidate.get("videoId")}", StdOutColors.CYAN))
        if self.__is_acceptable_candidate_album__(candidate, artist, album, self.options.getoption("search_acceptance_ratio")):
          self.std_out_logger.print_green(f"Candidate {candidate_counter} '{candidate.get('artists')[0].get('name')} - {candidate.get('title')}' (explicit) is acceptable. Its ID is: {candidate.get('playlistId')}")
          return self.__youtube_base_href_video__ + candidate.get("playlistId")
        
    candidate_counter = 0
    for candidate in candidates:
      candidate_counter += 1
      # print(std_out_colors.get_colored_string(f"Processing search candidate {candidate_counter} with ID {candidate.get("videoId")}", StdOutColors.CYAN))
      if self.__is_acceptable_candidate_album__(candidate, artist, album, self.options.getoption("search_acceptance_ratio")):
        self.std_out_logger.print_green(f"Candidate {candidate_counter} '{candidate.get('artists')[0].get('name')} - {candidate.get('title')}' is acceptable. Its ID is: {candidate.get('playlistId')}")
        return self.__youtube_base_href_video__ + candidate.get("playlistId")
      
    if self.options.getoption("search_force_candidate_selection"):
      candidate = candidates[0]
      self.std_out_logger.print_yellow(f"Forced selection to candidate '{candidate.get('artists')[0].get('name')} - {candidate.get('title')}' with ID {candidate.get('playlistId')} because of the 'search-force-candidates-selection' option. This can lead to errors")
      return self.__youtube_base_href_video__ + candidates[0].get("playlistId")
    
    self.std_out_logger.print_red(f"Unable to find a valid candidate for the search string '{search_string}'. Not forcing because the option 'search-force-candidates-selection' hasn't been passed (this is safer than using the option though)")
    return None

  def __search_for_playlist__(self, author, playlist, search_string):
    candidates = self.__yt_music__.search(f"{author} - {playlist}", filter="playlists", limit=self.options.getoption("search_limit"))
    self.std_out_logger.print_cyan(f"Processing search candidates (playlists)")

    candidate_counter = 0
    if not self.options.getoption("disable_search_explicit_first"):
      for candidate in candidates[:self.options.getoption("search_explicit_limit")]:
        candidate_counter += 1
        if not candidate.get("isExplicit"):
          continue
        # print(std_out_colors.get_colored_string(f"Processing search candidate {candidate_counter} with ID {candidate.get("videoId")}", StdOutColors.CYAN))
        if self.__is_acceptable_candidate_playlist__(candidate, author, playlist, self.options.getoption("search_acceptance_ratio")):
          self.std_out_logger.print_green(f"Candidate {candidate_counter} '{candidate.get('artists')[0].get('name')} - {candidate.get('title')}' (explicit) is acceptable. Its ID is: {candidate.get('playlistId')}")
          return self.__youtube_base_href_video__ + candidate.get("playlistId")
        
    candidate_counter = 0
    for candidate in candidates:
      candidate_counter += 1
      # print(std_out_colors.get_colored_string(f"Processing search candidate {candidate_counter} with ID {candidate.get("videoId")}", StdOutColors.CYAN))
      if self.__is_acceptable_candidate_playlist__(candidate, author, playlist, self.options.getoption("search_acceptance_ratio")):
        self.std_out_logger.print_green(f"Candidate {candidate_counter} '{candidate.get('artists')[0].get('name')} - {candidate.get('title')}' is acceptable. Its ID is: {candidate.get('playlistId')}")
        return self.__youtube_base_href_video__ + candidate.get("playlistId")
      
    if self.options.getoption("search_force_candidate_selection"):
      candidate = candidates[0]
      self.std_out_logger.print_yellow(f"Forced selection to candidate '{candidate.get('artists')[0].get('name')} - {candidate.get('title')}' with ID {candidate.get('playlistId')} because of the 'search-force-candidates-selection' option. This can lead to errors")
      return self.__youtube_base_href_video__ + candidates[0].get("playlistId")
    
    self.std_out_logger.print_red(f"Unable to find a valid candidate for the search string '{search_string}'. Not forcing because the option 'search-force-candidates-selection' hasn't been passed (this is safer than using the option though)")
    return None

  def __free_search__(self, search_string):
    candidates = self.__yt_music__.search(f"{search_string}", limit=self.options.getoption("search_csv_delimiter"))
    # top_result = list(filter(lambda c: c.get("category") == "Top result", candidates))
    # if len(top_result) < 0:
    #   print(std_out_colors.get_colored_string(f"Top result not found. Aborting search for the given search string '{search_string}'", StdOutColors.RED))
    #   return None
    # top_result = top_result[0]
    top_results = list(filter(lambda c: c.get("category") in ["Top result", "Songs", "Videos", "Albums", "Community playlists"], candidates))
    first_top_result, second_top_result = top_results[0], top_results[1]
    if first_top_result.get("resultType") == "video" and second_top_result.get("resultType") != "video": # because the search returns videos often
      self.std_out_logger.print_green(f"Top result is '{second_top_result.get('artists')[0].get('name')} - {second_top_result.get('title')}' ({second_top_result.get('resultType')}). Its ID is: {self.__get_correct_id_from_result_type__(second_top_result)}")
      return self.__get_correct_href_from_result_type__(second_top_result)
    else:
      self.std_out_logger.print_green(f"Top result is '{first_top_result.get('artists')[0].get('name')} - {first_top_result.get('title')}' ({first_top_result.get('resultType')}). Its ID is: {self.__get_correct_id_from_result_type__(first_top_result)}")
      return self.__get_correct_href_from_result_type__(first_top_result)
    
  def search(self, search_string):
    if self.options.getoption("enable_free_search"):
      self.std_out_logger.print_cyan(f"Careful! Free search was enabled. Processing will proceed to extract the top result for the search query '{search_string}'")
      return self.__free_search__(search_string)
    
    artist, song_or_album, search_type = self.__get_search_values_from_csvlike__(search_string)
    if artist == None or song_or_album == None or search_type == None:
      return None
    
    match search_type:
      case "songs":
        return self.__search_for_song__(artist, song_or_album, search_string)
      case "albums":
        return self.__search_for_album__(artist, song_or_album, search_string)
      case "playlists":
        return self.__search_for_playlist__(artist, song_or_album, search_string)