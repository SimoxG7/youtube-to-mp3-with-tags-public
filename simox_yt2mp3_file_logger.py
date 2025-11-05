from datetime import datetime

from simox_yt2mp3_common_functions import CommonFunctions
from simox_yt2mp3_options import Options
from simox_yt2mp3_stdout_colors import StdOutColors

class FileLogger:
  
  def __init__(
    self,
    options: Options,
    std_out_colors: StdOutColors,
    common_functions: CommonFunctions,
  ):
    self.options = options
    self.std_out_colors = std_out_colors
    self.common_functions = common_functions

  log_container = [["URL", "DOWNLOAD STATUS", "METADATA STATUS", "RUN TIME", "FILENAME"]]
  log_current_iteration = []

  log_current_song_start = None
  log_error_during_playlist = False
  log_current_playlist_start = None

  log_possible_status = ["OK", "WARN", "ERR"]

  log_program_start = datetime.now()
  log_program_start_string = log_program_start.strftime("%Y-%m-%d %H-%M-%S")

  log_search_container = [["SEARCH STRING", "SEARCH STATUS", "SEARCH RESULT"]]
  log_search_current_iteration = []

  # start logs
  
  def __print_first_row_runtime__(self):
    with open(f"logs/logs {self.log_program_start_string}/log {self.log_program_start_string}.log", "a") as log_file:
      log_file.write("THIS IS A TEMPORARY LOG FILE WHICH IS BEING WRITTEN AS THE PROGRAM RUNS. AFTER THE COMPLETION OF THE PROGRAM, THE LOG WILL BE FORMATTED AND ITS COLUMNS JUSTIFIED.\n")
      log_file.write(f"Execution started at {self.log_program_start}.\n")
      log_file.write("| " + " | ".join(self.log_container[0]) + " |\n")

  def __print_first_row_csv_runtime__(self):
    with open(f"logs/logs {self.log_program_start_string}/log {self.log_program_start_string}.csv", "a") as log_file:
      log_file.write(";".join(self.log_container[0]) + "\n")

  def __print_first_row_search_runtime__(self):
    with open(f"logs/logs {self.log_program_start_string}/log_search {self.log_program_start_string}.log", "a") as log_file:
      log_file.write("THIS IS A TEMPORARY LOG FILE WHICH IS BEING WRITTEN AS THE PROGRAM RUNS. AFTER THE COMPLETION OF THE PROGRAM, THE LOG WILL BE FORMATTED AND ITS COLUMNS JUSTIFIED.\n")
      log_file.write("| " + " | ".join(self.log_search_container[0]) + " |\n")

  def __print_last_row_runtime__(self):
    with open(f"logs/logs {self.log_program_start_string}/log {self.log_program_start_string}.log", "a") as log_file:
      now = datetime.now()
      log_file.write(f"Execution terminated at {now}.\n")
      total_elapsed = self.common_functions.elapsed_time_float_seconds(self.log_program_start, now)
      log_file.write(f"Execution took {total_elapsed} seconds (equivalent to {int(total_elapsed / 60)} minutes and {int(total_elapsed % 60)} seconds).\n")

  def __print_log_row_runtime__(self, to_be_logged):
    with open(f"logs/logs {self.log_program_start_string}/log {self.log_program_start_string}.log", "a") as log_file:
      log_file.write("| " + " | ".join(str(s) for s in to_be_logged) + " |\n")

  def __print_log_row_csv_runtime__(self, to_be_logged):
    with open(f"logs/logs {self.log_program_start_string}/log {self.log_program_start_string}.csv", "a") as log_file:
      log_file.write(";".join(str(s) for s in to_be_logged) + "\n")

  def __print_log__(self):
    with open(f"logs/logs {self.log_program_start_string}/log {self.log_program_start_string}.log", "w") as log_file:
      log_file.write(f"Execution started at {self.log_program_start}.\n")
      tuple_col_len = self.__get_logger_max_len_per_column__()
      for log_entry in self.log_container:
        justified_cols = []
        for i in range(5):
          justified_cols.append(str(log_entry[i]).ljust(tuple_col_len[i]))
        log_file.write("| " + " | ".join(justified_cols) + " |\n")
      now = datetime.now()
      log_file.write(f"Execution terminated at {now}.\n")
      total_elapsed = self.common_functions.elapsed_time_float_seconds(self.log_program_start, now)
      log_file.write(f"Execution took {total_elapsed} seconds (equivalent to {int(total_elapsed / 60)} minutes and {int(total_elapsed % 60)} seconds).\n")

  def __print_log_csv__(self):
    with open(f"logs/logs {self.log_program_start_string}/log {self.log_program_start_string}.csv", "w") as log_file:
      for log_entry in self.log_container:
        log_file.write(";".join(str(s) for s in log_entry) + "\n")

  def __print_log_urls__(self, urls):
    with open(f"logs/logs {self.log_program_start_string}/log_url {self.log_program_start_string}.txt", "a") as log_file:
      log_file.write("\n".join(urls))

  def __print_log_url__(self, url):
    with open(f"logs/logs {self.log_program_start_string}/log_url {self.log_program_start_string}.txt", "a") as log_file:
      log_file.write(f"{url}\n")

  def __get_logger_max_len_per_column__(self):
    max_url = 0
    max_download = 0
    max_metadata = 0
    max_run = 0
    max_filename = 0
    for url, download, metadata, run, filename in self.log_container:
      max_url = max(max_url, len(url))
      max_download = max(max_download, len(download))
      max_metadata = max(max_metadata, len(metadata))
      max_run = max(max_run, len(str(run)))
      max_filename = max(max_filename, len(filename))
    return max_url, max_download, max_metadata, max_run, max_filename
  
  def __get_logger_search_max_len_per_column__(self):
    max_search_string = 0
    max_search_status = 0
    max_search_result = 0
    for search_string, search_status, search_result in self.log_search_container:
      max_search_string = max(max_search_string, len(search_string))
      max_search_status = max(max_search_status, len(search_status))
      max_search_result = max(max_search_result, len(search_result))
    return max_search_string, max_search_status, max_search_result
  
  def log_start(self):
    if not self.options.getoption("no_log_files"):
      self.common_functions.create_main_log_dir()
      self.common_functions.create_log_dir(self.log_program_start_string)
      self.__print_first_row_runtime__()
      self.__print_first_row_csv_runtime__()
      self.__print_first_row_search_runtime__()
      
  def log_url_list(self, url_list):
    if not self.options.getoption("no_log_files"):
      self.__print_log_urls__(url_list)

  def log_url_single(self, url):
    if not self.options.getoption("no_log_files"):
      self.__print_log_url__(url)
      
  def print_log_row_runtime(self):
    if not self.options.getoption("no_log_files"):
      self.__print_log_row_runtime__(self.log_current_iteration)
      self.__print_log_row_csv_runtime__(self.log_current_iteration)
      
  def log_end(self):
    if not self.options.getoption("no_log_files"):
      self.__print_last_row_runtime__()
      self.__print_log__()
      self.__print_log_csv__()
      
  def append_log_iteration(self):
    self.log_container.append(self.log_current_iteration)

  def print_log_search(self):
    with open(f"logs/logs {self.log_program_start_string}/log_search {self.log_program_start_string}.log", "w") as log_file:
      tuple_col_len = self.__get_logger_search_max_len_per_column__()
      for log_entry in self.log_search_container:
        justified_cols = []
        for i in range(3):
          justified_cols.append(str(log_entry[i]).ljust(tuple_col_len[i]))
        log_file.write("| " + " | ".join(justified_cols) + " |\n")
  
  def print_log_search_runtime(self):
    with open(f"logs/logs {self.log_program_start_string}/log_search {self.log_program_start_string}.log", "a") as log_file:
      log_file.write("| " + " | ".join(str(s) for s in self.log_search_current_iteration) + " |\n")

  def append_log_search_iteration_and_clear(self):
    self.log_search_container.append(self.log_search_current_iteration)
    self.log_search_current_iteration = []