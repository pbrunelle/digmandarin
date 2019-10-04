#!/bin/env python3

'''
Here are the patterns I have observed:

Initial  Final  Tone  URL
-----------------------------------------------
<none>   ai     2     .../row1/wai2/Audio.mp3
p        eng    4     .../BPMF/peng4/Audio.mp3
f        u      2     .../BPMF/fu2/Audio.mp3
n        ve*    1     .../DTNL/nve1/Audio.mp3
t        ou     1     .../DTNL/tou1/Audio.mp3
k        uang   4     .../GKH/kuang4/Audio.mp3
c        ui     3     .../ZCS/cui3/Audio.mp3
r        ua     1     .../ZHCHSH/rua1/Audio.mp3
x        iong   3     .../JQX/xiong3/Audio.mp3

Notes:
- All URLs start with https://www.digmandarin.com/tools/sounds
- v = u with double dot
'''

import urllib.request

urllib.request.urlretrieve(url, file_name)


inital2row = {
    '': 'row1',
    'b': 'BPMF', 'p': 'BPMF', 'm': 'BPMF', 'f': 'BPMF',
    'd': 'DTNL', 't': 'DTNL', 'n': 'DTNL', 'l': 'DTNL',
    'g': 'GKH', 'k': 'GKH', 'h': 'GKH',
    'z': 'ZCS', 'c': 'ZCS', 's': 'ZCS',
    'zh': 'ZHCHSH', 'ch': 'ZHCHSH', 'sh': 'ZHCHSH', 'r': 'ZHCHSH',
    'j': 'JQX', 'q': 'JQX', 'x': 'JQX',
}

finals = [
    'a', 'ai', 'an', 'ang', 'ao',
    'e', 'ei', 'en', 'eng', 'er',
    'i', 'ia', 'iao', 'ie', 'iu', 'ian', 'in', 'iang', 'ing', 'iong',
    'o', 'ong', 'ou',
    'u', 'ua', 'uo', 'uai', 'ui', 'uan', 'un', 'uang', 'ueng',
    'v', 've', 'van', 'vn',
]

def get_pinyin(initial, final):
    if initial != '':
        return '%s%s' % (initial, final)
    if final in ('a', 'e', 'o', 'er', 'ai', 'ao', 'ou', 'an', 'en', 'ang', 'eng',):
        return final
    if final in ('i', 'in', 'ing',):
        return 'y%s' % final
    if final in ('ia', 'iao', 'ie', 'ian', 'iang', 'iong',):
        return 'y%s' % final{1:]
    if final == 'iu':
        return 'you'
    if final == 'un':
        return 'wen'
    if final.startswith('u'):
        return 'w%s' % final[1:]
    if final.startswith('v'):
        return 'y%s' % final[1:]
    raise Exception('Unexpected (initial, final) = (%s, %s)' % (initial, final))

def get_pinyin_tone(initial, final, tone):
    initial_final = '%s%s' % (initial, final)
    if initial == '':
        initial_final = get_initial_final(final)
    return '%s%d' % (initial_final, tone)

def get_url(initial, final, tone):
    return 'https://www.digmandarin.com/tools/sounds/%s/%s/Audio.mp3' %\
           (inital2row[initial], get_pinyin(initial, final, tone))

class PinyinLink:
    def __init__(self, initial, final, tone, row, url):
        self.initial = initial
        self.final = final
        self.tone = tone
        self.row = row
        self.url = url

def is_valid_initial_final(initial, final):
    '''
    Return whether the combination (initial, final) is valid according to
    from https://www.digmandarin.com/chinese-pinyin-chart.

    Pre-conditions: initial is valid and final is valid
    '''
    if initial in ('j', 'q', 'x',):
        return final.startswith('i') or final.startswith('v')
    if initial in ('zh', 'ch', 'sh',):
        return not final.startswith('i') and \
               not final.startswith('v') and \
               final != 'ueng' and \
               final != 'er' and \
               final != 'o':
    return True

def get_links():
    '''
    Return [PinyinLink, ...] for valid combinations (final, initial)
    from https://www.digmandarin.com/chinese-pinyin-chart
    '''

if __name__ == '__main__':
    datadir = './sounds'
    download_files(datadir)
