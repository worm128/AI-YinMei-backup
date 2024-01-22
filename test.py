import glob
import os
import re
import chardet
# song_name="Kiss Me Goodbye [Originally Performed by Angela Aki]"
# my_dir_=""
# for c in song_name:
#     if c == '[':
#         c = '[[]'
#     elif c == ']':
#         c = '[]]'
#     else:
#         c = c
#     my_dir_ = my_dir_ + c
# search_pattern = os.path.join(f"output\\{my_dir_}\\" + my_dir_ + '*.wav')
# list = glob.glob(search_pattern)
# print(list)
# name = re.sub(r'[\[\]<>:"/\\|?*]', '', "[孤高の浮き雲]..../雲[雀恭]弥 (BGM Ver.)....").rstrip('. ')
# print(name)

def check_encoding(text):
    result = chardet.detect(text)
    encoding = result['encoding']
    
    if encoding is None or 'ascii' in encoding.lower():
        print("该文本没有明显的非ASCII字符")
    else:
        print("该文本的编码为:", encoding)

check_encoding('å\x8f\x88æ\x98¯æ¸\x85æ\x98\x8eé\x9b¨ä¸\x8a æ\x8a\x98è\x8f\x8aå¯\x84å\x88°ä½\xa0èº«æ\x97\x81')