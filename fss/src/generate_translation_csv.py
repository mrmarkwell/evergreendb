# Open the messages.xlf file and generate a csv where the first
# column is the word that needs to be translated, and the second
# is intended to be filled in with the chinese translation.
import re

with open('messages.xlf', 'r') as file:
    translation_file = file.read().replace('\n', '')

matches = re.findall(r'<source>(.*?)</source>', translation_file)

with open('translations.csv', 'w') as file:
    for match in matches:
        file.write(match.strip() + ",\n")
