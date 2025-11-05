from simox_yt2mp3_options import Options
from simox_yt2mp3_stdout_colors import StdOutColors
from simox_yt2mp3_common_functions import CommonFunctions

class StdOutLogger:
  
  def __init__(
    self,
    options: Options,
    std_out_colors: StdOutColors,
    common_functions: CommonFunctions,
  ):
    self.options = options
    self.std_out_colors = std_out_colors
    self.common_functions = common_functions

  def print_red(self, string_to_print):
    if not self.options.getoption("no_stdout"):
      print(self.std_out_colors.get_colored_string(string_to_print, StdOutColors.RED))

  def print_yellow(self, string_to_print):
    if not self.options.getoption("no_stdout"):
      print(self.std_out_colors.get_colored_string(string_to_print, StdOutColors.YELLOW))

  def print_green(self, string_to_print):
    if not self.options.getoption("no_stdout"):
      print(self.std_out_colors.get_colored_string(string_to_print, StdOutColors.GREEN))

  def print_cyan(self, string_to_print):
    if not self.options.getoption("no_stdout"):
      print(self.std_out_colors.get_colored_string(string_to_print, StdOutColors.CYAN))

  def print(self, string_to_print):
    if not self.options.getoption("no_stdout"):
      print(string_to_print)