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

from collections import defaultdict
import os
import os.path
import urllib.error
import urllib.request

TONES = (1, 2, 3, 4)

class PinyinLink:
    def pinyin(self):
        raise NotImplemented()
    def pinyin_tone(self):
        raise NotImplemented()
    def url(self):
        raise NotImplemented()

def get_existing_pinyin_tones(datadir, prefix, fmt):
    return set([os.path.basename(fname).replace(fmt, '').replace(prefix, '') \
                for fname in os.listdir(datadir) \
                if fname.endswith(fmt) and fname.startswith(prefix)])

def download_files(all_links, datadir, prefix, fmt, error_fn=None):
    os.makedirs(datadir, exist_ok=True)
    skip = get_existing_pinyin_tones(datadir, prefix, fmt)
    skip_other_tones = set()
    links = [l for l in all_links if l.pinyin_tone() not in skip]
    print('Downloading %d sound files (%d total files, %d already downloaded '\
          'in %s)' % (len(links), len(all_links), len(skip), datadir))
    for i, l in enumerate(links):
        outfname = '%s/%s%s%s' % (datadir, prefix, l.pinyin_tone(), fmt)
        if l.pinyin() in skip_other_tones:
            print('%d/%d Skipping %s: failure on pinyin' %\
                  (i+1, len(links), outfname))
            continue
        print('%d/%d Downloading %s into %s' %\
              (i+1, len(links), l.url(), outfname))
        try:
            urllib.request.urlretrieve(l.url(), outfname)
            if error_fn and error_fn(outfname):
                os.unlink(outfname)
                skip_other_tones.add(l.pinyin())
                print('not a sound file, skiping other tones of same pinyin')
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                skip_other_tones.add(l.pinyin())
                print('not found, skiping other tones of same pinyin')
            else:
                raise

def create_anki_text_file(datadir, prefix, fmt, tag, ankifile):
    pinyin_tones = get_existing_pinyin_tones(datadir, prefix, fmt)
    pinyin2tones = defaultdict(set)
    for pyt in pinyin_tones:
        py, t = pyt[:-1], int(pyt[-1])
        pinyin2tones[py].add(t)
    print('Writing to: %s' % ankifile)
    with open(ankifile, 'w') as fanki:
        for py, tones in pinyin2tones.items():
            if len(tones) != len(TONES):
                print('WARN: found %d tones for %s' % (len(tones), py))
                continue
            fields = [py,] \
                   + ['[sound:%s%s%d%s]' % (prefix, py, t, fmt) for t in TONES] \
                   + ['', tag]
            fanki.write('%s\n' % '\t'.join(fields))
