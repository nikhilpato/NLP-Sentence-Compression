import json

def read_file(file_name, read_json=False):
  """ Reads in a JSON file or list from a specified
      file. This is used to read in the word vocabulary
      and the word, part-of-speech, and dependency relation
      dictionaries.

  Args:
    file_name: The name of the file to read.
    read_json: Whether the file contains a JSON object.

  Returns:
    data: A JSON object or a list (depends on read_json)

  """
  data = []
  with open('Assets/' + file_name) as document:
    if read_json:
      data = json.load(document)
    else:
      data += ([str(x) for x in document.read().split()])
  return data

