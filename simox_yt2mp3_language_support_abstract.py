from abc import ABC, abstractmethod

class AbstractLanguageSupport(ABC):
  
  # __translation_map__ = {}
  
  @abstractmethod
  def __substitute__(self, match):
    pass
    # char = match.group(0)
    # return self.__translation_map__.get(char, char)  # returns the original char if not found

  @abstractmethod
  def translate_regex(self, original_text):
    pass
    # pattern = '|'.join(re.escape(key) for key in self.__translation_map__)
    # result_text = re.sub(pattern, self.__substitute__, original_text)
    # return result_text

# # Utilization Example
# text_to_be_mapped = "Привет, как дела? Ciao scemo"
# mapped_text = translate_regex(text_to_be_mapped)
# print(f"Text to be mapped: {text_to_be_mapped}")
# print(f"Mapped text: {mapped_text}")