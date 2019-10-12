#!/usr/bin/env python3

'''
Download sound files from yabla and create Anki cards

https://yabla.vo.llnwd.net/media.yabla.com/chinese_static/audio/alicia/qu4.mp3
'''

import argparse
import random
import pinyin

INITIALS = [
    '',
    'b', 'p', 'm', 'f',
    'd', 't', 'n', 'l',
    'g', 'k', 'h',
    'z', 'c', 's',
    'zh', 'ch', 'sh', 'r',
    'j', 'q', 'x',
]

FINALS = [
    'a', 'ai', 'an', 'ang', 'ao',
    'e', 'ei', 'en', 'eng', 'er',
    'i', 'ia', 'iao', 'ie', 'iu', 'ian', 'in', 'iang', 'ing', 'iong',
    'o', 'ong', 'ou',
    'u', 'ua', 'uo', 'uai', 'ui', 'uan', 'un', 'uang', 'ueng',
    'v', 've', 'van', 'vn',
]

AUDIO_FORMAT = '.mp3'

class YablaLink(pinyin.PinyinLink):
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
        self._url = 'https://yabla.vo.llnwd.net/media.yabla.com/chinese_static/audio/alicia/%s%s' %\
                    (self._pinyin_tone, AUDIO_FORMAT)
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
    ret = [ ]
    for initial in INITIALS:
        for final in FINALS:
            for tone in pinyin.TONES:
                ret.append(YablaLink(initial, final, tone))
    return ret

if __name__ == '__main__':
    SITE = 'yabla'
    parser = argparse.ArgumentParser(description='Yabla pinyin sounds')
    parser.add_argument('--download', dest='download', action='store_true')
    parser.add_argument('--no-download', dest='download', action='store_false')
    parser.set_defaults(download=False)
    parser.add_argument('--anki', dest='anki', action='store_true')
    parser.add_argument('--no-anki', dest='anki', action='store_false')
    parser.set_defaults(anki=False)
    parser.add_argument('--datadir', default='./sounds-%s' % SITE, help='sound files path')
    parser.add_argument('--prefix', default='%s-' % SITE, help='prefix to add to all sound files')
    parser.add_argument('--ankifile', default='./anki-%s.txt' % SITE, help='anki file path')
    args = parser.parse_args()
    if args.download:
        links = get_links()
        # random.shuffle(links)
        pinyin.download_files(links, args.datadir, args.prefix, AUDIO_FORMAT)
    if args.anki:
        pinyin.create_anki_text_file(args.datadir, args.prefix, AUDIO_FORMAT, SITE, args.ankifile)
