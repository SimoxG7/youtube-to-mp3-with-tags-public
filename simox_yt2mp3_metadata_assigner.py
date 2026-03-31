import difflib
from io import BytesIO
from PIL import Image, ImageChops
import requests

from simox_yt2mp3_common_functions import CommonFunctions
from simox_yt2mp3_file_logger import FileLogger
from simox_yt2mp3_options import Options
from simox_yt2mp3_stdout_colors import StdOutColors
from simox_yt2mp3_stdout_logger import StdOutLogger

class MetadataAssigner:
  
  artist_tag_separator = ", "

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

  def __find_best_cover__(self, info: dict):
    thumbnails: list[dict] = info.get("thumbnails")
    thumbnails_with_resolution = list(filter(lambda thumbnail: thumbnail.get("resolution") != None and thumbnail.get("height") == thumbnail.get("width") and thumbnail.get("height") <= self.options.getoption("max_res"), thumbnails))
  
    if thumbnails_with_resolution != []:
      cover_with_best_resolution = max(thumbnails_with_resolution, key=lambda thumbnail: thumbnail.get("height"))
      return cover_with_best_resolution
    
    if self.options.getoption("crop_non_squared_covers"):
      thumbnails_to_be_cropped = [thumbnail for thumbnail in thumbnails if thumbnail.get("height") and thumbnail.get("height") <= self.options.getoption("max_res")]
      if thumbnails_to_be_cropped:
        return max(thumbnails_to_be_cropped, key=lambda thumbnail: thumbnail.get("height", 0))
      
    if not self.options.getoption("allow_non_squared_covers"):
      return None
    thumbnails_not_necessarily_squared = list(filter(lambda thumbnail: thumbnail.get("height") != None and thumbnail.get("height") <= self.options.getoption("max_res"), thumbnails))
    if thumbnails_not_necessarily_squared == []:
      return None
    cover_with_best_resolution = max(thumbnails_not_necessarily_squared, key=lambda thumbnail: thumbnail.get("height"))
    return cover_with_best_resolution
  
  def __download_cover__(self, url):
    image = Image.open(requests.get(url, stream=True).raw)
    bytes_io = BytesIO()
    width, height = image.size
    
    if (width != height and self.options.getoption("crop_non_squared_covers")):
      self.std_out_logger.print_yellow("Cropping the thumbnail as it is not squared")
      # detects borders that aren't perfectly black
      # use a point transform to turn dark pixels (0-40) into pure black
      threshold = 40
      grayscale = image.convert('L')
      mask = grayscale.point(lambda p: p > threshold and 255)
      bbox = mask.getbbox()
      
      if bbox:
        image = image.crop(bbox)

      # applying square crop to the cleaned image
      if (self.options.getoption("crop_non_squared_covers")):
        new_edge = min(width, height)
        left = (width - new_edge) / 2
        top = (height - new_edge) / 2
        image = image.crop((left, top, left + new_edge, top + new_edge))
    
    image.save(bytes_io, format="JPEG")
    bytes_value = bytes_io.getvalue()
    return bytes_value

  def assign_metadata(self, mp3_file, info: dict):
    # album
    album = info.get("album")
    if album != None:
      mp3_file["album"] = album
    
    # album artist
    main_artist = info.get("artist")
    album_artist = info.get("albumartist")
    if album_artist != None:
      mp3_file["albumartist"] = album_artist
    else:
      mp3_file["albumartist"] = main_artist

    # artists
    artists = info.get("artists")
    title = info.get("title")
    if artists != None:
      mp3_file["artist"] = self.artist_tag_separator.join(artists)
    else:
      channel = info.get("channel")
      if " - " in title:
        mp3_file["artist"] = title.split(" - ")[0]
      else:
        mp3_file["artist"] = channel

    # track_number
    playlist_index = info.get("playlist_index")
    playlist = info.get("playlist")
    prefixed_album = "Album - " + str(album)
    if playlist_index != None and album != None and (album == playlist or prefixed_album == playlist or self.common_functions.is_similar_string(album, playlist, self.options.getoption("general_acceptance_ratio")) or self.common_functions.is_similar_string(prefixed_album, playlist, self.options.getoption("general_acceptance_ratio"))):
      mp3_file["tracknumber"] = playlist_index

    # track_title
    track = info.get("track")
    if track != None:
      mp3_file["tracktitle"] = track
    else:
      title_ = title
      if " - " in title_:
        title_ = title_.split(" - ")[1]
      mp3_file["tracktitle"] = title_
    
    # cover
    best_cover = self.__find_best_cover__(info)
    if best_cover != None:
      image = self.__download_cover__(best_cover.get("url"))
      mp3_file["artwork"] = image

    # release_year
    release_year = info.get("release_year")
    if release_year != None:
      mp3_file["year"] = release_year
    
    # save metadata
    mp3_file.save()