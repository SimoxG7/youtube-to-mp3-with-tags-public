class StdOutColors:

  BLACK = "\033[0;30m"
  RED = "\033[0;31m"
  GREEN = "\033[0;32m"
  BROWN = "\033[0;33m"
  BLUE = "\033[0;34m"
  PURPLE = "\033[0;35m"
  CYAN = "\033[0;36m"
  YELLOW = "\033[1;33m"
  LIGHT_RED = "\033[1;31m"
  LIGHT_GREEN = "\033[1;32m"
  LIGHT_BLUE = "\033[1;34m"
  LIGHT_PURPLE = "\033[1;35m"
  LIGHT_CYAN = "\033[1;36m"
  LIGHT_WHITE = "\033[1;37m"
  LIGHT_GRAY = "\033[0;37m"
  DARK_GRAY = "\033[1;30m"
  BOLD = "\033[1m"
  FAINT = "\033[2m"
  ITALIC = "\033[3m"
  UNDERLINE = "\033[4m"
  BLINK = "\033[5m"
  NEGATIVE = "\033[7m"
  CROSSED = "\033[9m"
  END = "\033[0m"

  # Style
  __CEND__      = '\33[0m'
  __CBOLD__     = '\33[1m'
  __CITALIC__   = '\33[3m'
  __CURL__      = '\33[4m'
  __CBLINK__    = '\33[5m'
  __CBLINK2__   = '\33[6m'
  __CSELECTED__ = '\33[7m'

  # Colored
  __CBLACK__  = '\33[30m'
  __CRED__    = '\33[31m'
  __CGREEN__  = '\33[32m'
  __CYELLOW__ = '\33[33m'
  __CBLUE__   = '\33[34m'
  __CVIOLET__ = '\33[35m'
  __CBEIGE__  = '\33[36m'
  __CWHITE__  = '\33[37m'

  # Colored Background
  __CBLACKBG__  = '\33[40m'
  __CREDBG__    = '\33[41m'
  __CGREENBG__  = '\33[42m'
  __CYELLOWBG__ = '\33[43m'
  __CBLUEBG__   = '\33[44m'
  __CVIOLETBG__ = '\33[45m'
  __CBEIGEBG__  = '\33[46m'
  __CWHITEBG__  = '\33[47m'

  # Colored Background
  __CGREY__    = '\33[90m'
  __CRED2__    = '\33[91m'
  __CGREEN2__  = '\33[92m'
  __CYELLOW2__ = '\33[93m'
  __CBLUE2__   = '\33[94m'
  __CVIOLET2__ = '\33[95m'
  __CBEIGE2__  = '\33[96m'
  __CWHITE2__  = '\33[97m'

  # Colored Variant
  __CGREYBG__    = '\33[100m'
  __CREDBG2__    = '\33[101m'
  __CGREENBG2__  = '\33[102m'
  __CYELLOWBG2__ = '\33[103m'
  __CBLUEBG2__   = '\33[104m'
  __CVIOLETBG2__ = '\33[105m'
  __CBEIGEBG2__  = '\33[106m'
  __CWHITEBG2__  = '\33[107m'

  def get_colored_string(self, string_to_color, color):
    return color + string_to_color + self.END