import os
import csv
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tool.settings')

import django
django.setup()

from register import models

PATHS = (
    '../data/application.csv',
    '../data/audio.csv',
    '../data/font.csv',
    '../data/image.csv',
    '../data/message.csv',
    '../data/multipart.csv',
    '../data/text.csv',
    '../data/video.csv',
    )


import json
def main():

    dev_wipe()

    render_manual_csvs(('../data/ext-assoc.txt',))
    render_manuals()
    render_iana_csvs(PATHS)


def dev_wipe():
    models.Entry.objects.all().delete()
    models.Type.objects.all().delete()


def render_manuals():
    p = Path('../data/mimes.json')
    content = json.loads(p.read_text())

    res = ()
    for tname, entries in content.items():
        ms = manual_mimes_json_generate(tname, entries, p.name)
        res += ms
    models.Entry.objects.bulk_create(res, batch_size=900)


def render_iana_csvs(paths):
    l = len(paths)
    s = '' if l == 1 else 's'
    print(f'Parsing {l} file{s}')

    for path in paths:
        iana_csv_generate(path)


def render_manual_csvs(paths):
    l = len(paths)
    s = '' if l == 1 else 's'
    print(f'Parsing {l} file{s}')

    for path in paths:
        manual_csv_generate(path)


def manual_csv_generate(path):
    app_file = Path(path)
    Entry = models.Entry

    print('Generating', app_file)
    # build a type model
    # typename = template_name.split('/')[0]
    # tm, _ = models.Type.objects.get_or_create(name=typename)

    types = set()
    res = ()
    c = 0
    filename = app_file.name

    with open(app_file, 'r', newline='') as stream:
        # fieldnames = ['first_name', 'last_name']
        reader = csv.DictReader(stream)#, fieldnames=fieldnames)
        for c, row in enumerate(reader):
            text = row['row']
            _type = text.split('/')[0]
            types.add(_type)
            splits = text.split(' ')

            exts = splits[1:]
            template = splits[0]

            for ext in exts:
                clean = ext.strip()
                if len(clean) == 0:
                    continue

                m = Entry(
                        name=ext,
                        template=template,
                        reference=f'manual::{filename}'
                    )
                res += (m,)

    typemap = {}
    # Make types from all the captures words
    for typename in types:
        tm, _ = models.Type.objects.get_or_create(name=typename)
        typemap[typename] = tm

    # rebind the Type to each Entry model
    for m in res:
        name = m.template.split('/')[0]
        m.type = typemap[name]

    v = 'entry' if c == 1 else 'entries'
    print('Inserting', c, v)
    Entry.objects.bulk_create(res, batch_size=900)


def iana_csv_generate(path):
    app_file = Path(path)
    Entry = models.Entry

    print('Generating', app_file)
    # build a type model
    typename = app_file.stem
    tm, _ = models.Type.objects.get_or_create(name=typename)

    res = ()
    c = 0
    with open(app_file, 'r', newline='') as stream:
        # fieldnames = ['first_name', 'last_name']
        reader = csv.DictReader(stream)#, fieldnames=fieldnames)
        for c, row in enumerate(reader):
            m = Entry(**{x.lower():y for x,y in row.items()}, type=tm)
            res += (m,)

    v = 'entry' if c == 1 else 'entries'
    print('Inserting', c, v)
    Entry.objects.bulk_create(res, batch_size=900)


def manual_mimes_json_generate(template_name, entries, filename):
    typename = template_name.split('/')[0]

    Entry = models.Entry

    res = ()
    tm, _ = models.Type.objects.get_or_create(name=typename)
    for name in entries:
        m = Entry(
            name=name,
            type=tm,
            template=template_name,
            reference=f'manual::{filename}'
        )
        res += (m,)

    return res

if __name__ == '__main__':
    main()
