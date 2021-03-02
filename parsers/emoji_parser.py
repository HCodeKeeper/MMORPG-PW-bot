import requests
from bs4 import BeautifulSoup
import re
import emoji

'''
Need in working unicode formating. Instead using emojize with emoji name

triple " ' " - working code but useless without good decoding
'''
#### means added strings to replace useless code




url = 'http://www.fileformat.info/info/emoji/list.htm'

regexp = r"row"
#regexp2 = r"^/info/unicode"
regexp3 = r"\w+/index.htm"

source = requests.get(url)
main_text = source.text
soup = BeautifulSoup(main_text)

tables = soup.findAll('tr', {'class' : re.compile(regexp)})
####
emoji_id = []
####
emoji_names = []
#emoji_unicodes = []
'''
for table in tables: #initialize emoji_unicodes list
    table = str(table.find('a',  href = re.compile(regexp2)))
    try:
        table = table[table.index('>')+1 : -4]
        table = table.replace('+', '', 1)
        table = "u" + table[1:]
        emoji_unicodes.append(table)
    except:
        continue
'''

for name in tables:
    name = str(name.find('a', href = re.compile(regexp3)))
    try:
        name = name[name.index('>')+1 : -4]
        if name not in ['U+2002','U+2003', 'U+2005','copyright', 'registered', 'tm']:
            emoji_names.append(name)
        else:
            continue
    except:
        continue


####
for x in emoji_names:
    x = emoji.emojize(':'+ x + ':', use_aliases = True)
    emoji_id.append(x)
####
'''
emoji_dict = dict(zip(emoji_names, emoji_unicodes))
'''
emoji_dict = dict(zip(emoji_names, emoji_id))