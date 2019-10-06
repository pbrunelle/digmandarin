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

import os
import os.path
import random
import urllib.error
import urllib.request

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

class PinyinLink:
    def __init__(self, initial, final, tone):
        self.initial = initial
        self.final = final
        self.tone = tone
        self.pinyin_tone = self.get_pinyin_tone(initial, final, tone)
        self.url = self.get_url(initial, self.pinyin_tone)
        self.filename = '%s%s' % (self.pinyin_tone, AUDIO_FORMAT)

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

    def get_pinyin_tone(self, initial, final, tone):
        initial_final = '%s%s' % (initial, final)
        if initial == '':
            initial_final = self.get_pinyin(initial, final)
        return '%s%d' % (initial_final, tone)

    def get_url(self, initial, pinyin_tone):
        return 'https://www.digmandarin.com/tools/sounds/%s/%s/Audio%s' %\
               (INITIALS[initial], pinyin_tone, AUDIO_FORMAT)

def UNUSED_is_valid_initial_final(initial, final):
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
               final != 'o'
    return True

def get_links():
    '''
    Return [PinyinLink, ...] for valid combinations (final, initial)
    from https://www.digmandarin.com/chinese-pinyin-chart
    '''
    ret = [ ]
    for initial in INITIALS.keys():
        for final in FINALS:
            for tone in (1, 2, 3, 4):
                ret.append(PinyinLink(initial, final, tone))
    return ret

def get_existing_pinyin_tones(datadir):
    return set([os.path.basename(fname).replace(AUDIO_FORMAT, '') \
                for fname in os.listdir(datadir) \
                if fname.endswith(AUDIO_FORMAT)])

def download_files(datadir):
    os.makedirs(datadir, exist_ok=True)
    skip = get_existing_pinyin_tones(datadir)
    skip_other_tones = set()
    all_links = get_links()
    random.shuffle(all_links)
    links = [l for l in all_links if l.pinyin_tone not in skip]
    print('Downloading %d sound files (%d total files, %d already downloaded '\
          'in %s' % (len(links), len(all_links), len(skip), datadir))
    for i, l in enumerate(links):
        outfname = '%s/%s%s' % (datadir, l.pinyin_tone, AUDIO_FORMAT)
        if (l.initial, l.final) in skip_other_tones:
            print('%d/%d Skipping %s: failure on (initial, final)' %\
                  (i+1, len(links), outfname))
            continue
        print('%d/%d Downloading %s into %s' % (i+1, len(links), l.url, outfname))
        try:
            urllib.request.urlretrieve(l.url, outfname)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                skip_other_tones.add((l.initial, l.final))
                print('not found, skiping other tones of same (initial, final)')
            else:
                raise

if __name__ == '__main__':
    datadir = './sounds'
    download_files(datadir)
