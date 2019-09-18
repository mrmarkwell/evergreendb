# Open the messages.xlf file and add <target> translations for each <source> translation.
# The translation csv file must contain the same translatable values in the same order for this to work properly.

# The output file is called messages_with_translations.xlf.
import sys
import re

with open('translations_from_claudia.csv', 'r') as file:
    translation_dict = dict()
    for line in file:
        values = [x.strip() for x in line.split(',')]
        if (len(values) != 2):
            print("More than 2 columns found in a row of the csv!")
            sys.exit()
        if not values[0]:
            continue
        translation_dict[values[0]] = values[1]
        print("Translation found! English: " + values[0] + " Chinese: " + values[1])

with open('messages.xlf', 'r') as file:
    filedata = file.read();
    filedata = re.sub(r'<source>\s+', r'<source>', filedata)
    filedata = re.sub(r'\s+</source>', r'</source>', filedata)

for key, value in translation_dict.items():
    search_string = "<source>" + key + "</source>"
    replace_string = search_string + "<target>" + value + "</target>"
    if search_string in filedata:
        filedata = filedata.replace(search_string, replace_string)
    else:
        print("Missing substring: " + search_string)
        print("Manually fix!! ^^")

with open('messages_with_translations.xlf', 'w') as file:
  file.write(filedata)
