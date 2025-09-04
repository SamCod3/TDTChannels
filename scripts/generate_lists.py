#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / 'data'


def write_table(out, channels, headers, fields):
    out.write('| ' + ' | '.join(headers) + ' |\n')
    out.write('| ' + ' | '.join(['-'] * len(headers)) + ' |\n')
    for ch in channels:
        out.write('| ' + ' | '.join(ch.get(f, '-') for f in fields) + ' |\n')
    out.write('\n')


def generate(config):
    data_path = DATA_DIR / config['data']
    output_path = ROOT / config['output']
    with open(data_path, encoding='utf-8') as f:
        data = json.load(f)
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write(f"# {config['title']}\n\n")
        for cat in data:
            out.write(f"## {cat['name']}\n\n")
            if cat.get('channels'):
                write_table(out, cat['channels'], config['headers'], config['fields'])
            if 'subcategories' in cat:
                for sub in cat['subcategories']:
                    out.write(f"### {sub['name']}\n\n")
                    write_table(out, sub['channels'], config['headers'], config['fields'])


CONFIGS = [
    {
        'data': 'television.yml',
        'output': 'TELEVISION.md',
        'title': 'Canales de Televisión',
        'headers': ['Canal', 'M3U8', 'Web', 'Logo', 'EPG ID', 'Info'],
        'fields': ['name', 'm3u8', 'web', 'logo', 'epg_id', 'info'],
    },
    {
        'data': 'radio.yml',
        'output': 'RADIO.md',
        'title': 'Emisoras de Radio',
        'headers': ['Emisoras', 'Stream', 'Web', 'Logo', 'Info'],
        'fields': ['name', 'stream', 'web', 'logo', 'info'],
    },
]


def main():
    for config in CONFIGS:
        generate(config)


if __name__ == '__main__':
    main()
