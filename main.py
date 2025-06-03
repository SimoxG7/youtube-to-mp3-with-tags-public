from simox_yt2mp3_common_functions import CommonFunctions
from simox_yt2mp3_downloader import Downloader
from simox_yt2mp3_extractor import Extractor
from simox_yt2mp3_metadata_assigner import MetadataAssigner
from simox_yt2mp3_options import Options
from simox_yt2mp3_file_logger import FileLogger
from simox_yt2mp3_language_support_russian import RussianLanguageSupport
from simox_yt2mp3_processor import Processor
from simox_yt2mp3_searcher import Searcher
from simox_yt2mp3_stdout_colors import StdOutColors
from simox_yt2mp3_stdout_logger import StdOutLogger

# first level dependencies
std_out_colors = StdOutColors()
options = Options(std_out_colors)
options.parse_options()
language_supports = [RussianLanguageSupport()]
common_functions = CommonFunctions(options, std_out_colors, language_supports)

# second level dependencies (might need to use options or std_out_colors)
file_logger = FileLogger(options, std_out_colors, common_functions)
std_out_logger = StdOutLogger(options, std_out_colors, common_functions)

# third level dependencies
metadata_assigner = MetadataAssigner(options, std_out_colors, file_logger, std_out_logger, common_functions)
searcher = Searcher(options, std_out_colors, file_logger, std_out_logger, common_functions)
extractor = Extractor(options, std_out_colors, file_logger, std_out_logger, common_functions)

# fourth level dependencies
downloader = Downloader(options, std_out_colors, file_logger, std_out_logger, metadata_assigner, language_supports, common_functions)

# fifth level depdendencies
processor = Processor(options, std_out_colors, file_logger, std_out_logger, metadata_assigner, language_supports, downloader, searcher, extractor, common_functions)

# constants
log_program_start_string = file_logger.log_program_start_string

def main():
  file_logger.log_start()

  url_list = []

    # for url in url_file:
    #   url = url.strip()
      # if url == "" or url.startswith("#"):
      #   continue
      
      # if common_functions.check_url_validity(url):
      #   url_list.append(url)
      # else:
      #   print(std_out_colors.get_colored_string(f"The entry '{url}' does not seem to conform to a YouTube URL with a specified video and/or playlist. If you think that's not the case, then contact the developer. Program will now proceed using the entry as a search term", StdOutColors.YELLOW))
      #   print(std_out_colors.get_colored_string(f"Proceding with a search on Youtube Music of the given string '{url}'", StdOutColors.CYAN))
      #   new_url = searcher.search(url)
      #   if new_url == None:
      #     print(std_out_colors.get_colored_string(f"Unable to complete search with the string '{url}'. Please use an URL for this specific download", StdOutColors.RED))
      #     file_logger.log_search_current_iteration = [url, "UNABLE", ""]
      #     continue
      #   else:
      #     url_list.append(new_url)
      #     print(std_out_colors.get_colored_string(f"Executed search on Youtube Music of the given string '{url}'. Found the best corresponding result with the following URL: {new_url}", StdOutColors.GREEN))
      #     file_logger.log_search_current_iteration = [url, "OK", new_url]
      #   file_logger.print_log_search_runtime()
      #   file_logger.append_log_search_iteration_and_clear()

  with open("to_download_urls_and_queries.txt", "r") as url_file:
    for url in url_file:
      url = url.strip()
      if url == "" or url.startswith("#"):
        continue
      
      if common_functions.check_url_validity(url):
        url_list.append(url)
      else:
        std_out_logger.print_yellow(f"The entry '{url}' does not seem to conform to a YouTube URL with a specified video and/or playlist. If you think that's not the case, then contact the developer. Program will now proceed using the entry as a search term")
        std_out_logger.print_cyan(f"Proceding with a search on Youtube Music of the given string '{url}'")
        new_url = searcher.search(url)
        if new_url == None:
          std_out_logger.print_red(f"Unable to complete search with the string '{url}'. Please use an URL for this specific download")
          file_logger.log_search_current_iteration = [url, "UNABLE", ""]
          continue
        else:
          url_list.append(new_url)
          std_out_logger.print_green(f"Executed search on Youtube Music of the given string '{url}'. Found the best corresponding result with the following URL: {new_url}")
          file_logger.log_search_current_iteration = [url, "OK", new_url]
        file_logger.print_log_search_runtime()
        file_logger.append_log_search_iteration_and_clear()
  
  file_logger.log_url_list(url_list)
  file_logger.print_log_search()

  common_functions.create_destination_dir()

  # with open("to_download_urls_and_queries.txt", "r") as url_file:
  #   for yt_url in url_file:
  #     yt_url: str = yt_url.strip()
  #     if yt_url == "" or yt_url.startswith("#"): 
  #       continue
  #     processor.process(yt_url)

  for yt_url in url_list:
    processor.process(yt_url)

  file_logger.log_end()


main()