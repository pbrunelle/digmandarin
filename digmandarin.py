#!/usr/bin/env python3

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

import argparse
import random
import pinyin

INITIALS = {
    '': 'row1',
    'b': 'BPMF', 'p': 'BPMF', 'm': 'BPMF', 'f': 'BPMF',
    'd': 'DTNL', 't': 'DTNL', 'n': 'DTNL', 'l': 'DTNL',
    'g': 'GKH', 'k': 'GKH', 'h': 'GKH',
    'z': 'ZCS', 'c': 'ZCS', 's': 'ZCS',
    'zh': 'ZHCHSH', 'ch': 'ZHCHSH', 'sh': 'ZHCHSH', 'r': 'ZHCHSH',
    'j': 'JQX', 'q': 'JQX', 'x': 'JQX',
}

FINALS = [
    'a', 'ai', 'an', 'ang', 'ao',
    'e', 'ei', 'en', 'eng', 'er',
    'i', 'ia', 'iao', 'ie', 'iu', 'ian', 'in', 'iang', 'ing', 'iong',
    'o', 'ong', 'ou',
    'u', 'ua', 'uo', 'uai', 'ui', 'uan', 'un', 'uang', 'ueng',
    'v', 've', 'van', 'vn',
]

AUDIO_FORMAT = '.mp3'

class DigMandarinLink(pinyin.PinyinLink):
    def pinyin(self):
        return self._pinyin
    def pinyin_tone(self):
        return self._pinyin_tone
    def url(self):
        return self._url
    def __init__(self, initial, final, tone):
        self._initial = initial
        self._final = final
        self._tone = tone
        self._pinyin = self.get_pinyin(initial, final)
        self._pinyin_tone = '%s%d' % (self.get_pinyin(initial, final), tone)
        self._url = 'https://www.digmandarin.com/tools/sounds/%s/%s/Audio%s' %\
                    (INITIALS[initial], self._pinyin_tone, AUDIO_FORMAT)
    def get_pinyin(self, initial, final):
        if initial != '':
            return '%s%s' % (initial, final)
        if final in ('a', 'e', 'o', 'er', 'ai', 'ao', 'ou', 'an', 'en', 'ang',
                     'eng', 'ei', 'ong',):
            return final
        if final in ('i', 'in', 'ing',):
            return 'y%s' % final
        if final in ('ia', 'iao', 'ie', 'ian', 'iang', 'iong',):
            return 'y%s' % final[1:]
        if final == 'iu':
            return 'you'
        if final == 'un':
            return 'wen'
        if final.startswith('u'):
            return 'w%s' % final[1:]
        if final.startswith('v'):
            return 'y%s' % final[1:]
        raise Exception('Unexpected (initial, final) = (%s, %s)' %\
                        (initial, final))

def get_links():
    '''
    Return [PinyinLink, ...] for valid combinations (final, initial)
    from https://www.digmandarin.com/chinese-pinyin-chart
    '''
    ret = [ ]
    for initial in INITIALS.keys():
        for final in FINALS:
            for tone in pinyin.TONES:
                ret.append(DigMandarinLink(initial, final, tone))
    return ret

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Digmandarin pinyin sounds')
    parser.add_argument('--download', dest='download', action='store_true')
    parser.add_argument('--no-download', dest='download', action='store_false')
    parser.set_defaults(download=False)
    parser.add_argument('--anki', dest='anki', action='store_true')
    parser.add_argument('--no-anki', dest='anki', action='store_false')
    parser.set_defaults(anki=False)
    parser.add_argument('--datadir', default='./sounds-digmandarin', help='sound files path')
    parser.add_argument('--prefix', default='', help='prefix to add to all sound files')
    parser.add_argument('--ankifile', default='./anki-digmandarin.txt', help='anki file path')
    args = parser.parse_args()
    if args.download:
        links = get_links()
        random.shuffle(links)
        pinyin.download_files(links, args.datadir, args.prefix, AUDIO_FORMAT)
    if args.anki:
        pinyin.create_anki_text_file(args.datadir, args.prefix, AUDIO_FORMAT, 'digmandarin', args.ankifile)
