#!/usr/bin/env python3
"""平密 (Pingmi), Beijing - Taiyuan, 1926: the key, and a check of the reading of 116-010108-0566-005.

  python3 pingmi.py verify            reproduce every number in README.md from data/
  python3 pingmi.py enc 6511 ...      standard telegraph code -> 平密 group
  python3 pingmi.py dec 8382 ...      平密 group -> standard telegraph code
  python3 pingmi.py pages             the 81-page table (codebook page -> 平密 page number)

  --ctc FILE  a code table CSV "code,character,..." (for example tw.csv from
              github.com/kirklin/chinese-telegraph-code) to print characters too.

Python 3 standard library only.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')

# Tens and units substitutions, read off the January and April pairs (data/key_pairs.tsv).
TENS = {0: 0, 1: 8, 2: 6, 3: 4, 4: 2, 5: 9, 6: 7, 7: 5, 8: 3, 9: 1}
UNITS = {0: 2, 1: 4, 2: 6, 3: 8, 4: 0, 5: 1, 6: 3, 7: 5, 8: 7, 9: 9}
TENS_INV = {v: k for k, v in TENS.items()}
UNITS_INV = {v: k for k, v in UNITS.items()}


def page_number(page):
    """Codebook page 0..80 -> two digits 1..9 (base 9 without zero)."""
    return f"{page // 9 + 1}{page % 9 + 1}"


def enc(code):
    """Standard telegraph code (4 digits) -> 平密 group."""
    i = int(code) - 1                      # cells on a page run 01..99, 00
    page, tens, units = i // 100, i // 10 % 10, i % 10
    return f"{page_number(page)}{TENS[tens]}{UNITS[units]}"


def dec(group):
    """平密 group -> standard telegraph code, or None if the group is not a valid 平密 group."""
    if len(group) != 4 or not group.isdigit() or '0' in group[:2]:
        return None
    a, b, t, u = map(int, group)
    i = 100 * (9 * (a - 1) + (b - 1)) + 10 * TENS_INV[t] + UNITS_INV[u]
    return f"{i + 1:04d}"


# How the copyist of 0566-005 (Kong Fanwei's office) writes digits: P(true digit | digit as read).
# Set by hand from his confusions: 3 and 7 look the same, 8 is written like 3, 6 or 0, and so on.
HAND = {'7': {'7': .6, '3': .3, '2': .05, '1': .05}, '3': {'3': .6, '7': .25, '8': .15},
        '8': {'8': .6, '3': .15, '6': .15, '0': .1}, '1': {'1': .7, '6': .15, '7': .15},
        '6': {'6': .75, '8': .1, '1': .1, '0': .05}, '2': {'2': .8, '7': .15, '0': .05},
        '0': {'0': .8, '8': .1, '6': .1}, '4': {'4': .8, '8': .1, '6': .1},
        '9': {'9': .85, '5': .1, '4': .05}, '5': {'5': .85, '9': .1, '2': .05}}


def hand_p(read, true):
    p = 1.0
    for r, t in zip(read, true):
        p *= HAND[r].get(t, 0.004)
    return p


def classify(group, key_group):
    diff = sum(a != b for a, b in zip(group, key_group))
    if diff == 0:
        return 'exact'
    if diff == 1:
        return 'one digit'
    if hand_p(group, key_group) > 1e-4:
        return 'handwriting'
    return 'disagree'


def tsv(name):
    with open(os.path.join(DATA, name), encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def verify():
    bad = 0
    pairs = tsv('key_pairs.tsv')
    ok = 0
    for r in pairs:
        kg = enc(r['stc'])
        assert kg == r['key_group'], r
        if all(a == '?' or a == b for a, b in zip(r['group_on_sheet'], kg)):
            ok += 1
        else:
            bad += 1
            print('  pair does not fit:', r['source'], r['char'], r['stc'], r['group_on_sheet'], kg)
    print(f"Key pairs (char written beside the group): {ok} of {len(pairs)} fit the key.")

    rows = tsv('alignment.tsv')
    assert len(rows) == 106
    aligned = [r for r in rows if r['plain_char']]
    for r in aligned:
        assert enc(r['stc']) == r['key_group'], r
    full = [r for r in aligned if '?' not in r['group']]
    part = [r for r in aligned if '?' in r['group']]
    print(f"\nGroups: 106. Aligned with the plaintext of 116-010101-0027-164: {len(aligned)} "
          f"(groups 1-89 and 92-106). Not aligned: groups 90-91 at the join.")
    print(f"Aligned groups with an illegible digit (?): {len(part)} "
          f"({', '.join(r['idx'] for r in part)}), left out of the count.")
    counts = {'exact': 0, 'one digit': 0, 'handwriting': 0, 'disagree': 0}
    for r in full:
        r['class'] = classify(r['group'], r['key_group'])
        counts[r['class']] += 1
    print(f"Read in full: {len(full)}. Under the key: " +
          ', '.join(f"{k} {v}" for k, v in counts.items()) +
          f" ({len(full) - counts['disagree']} of {len(full)} consistent).")

    print("\nBlind reading, graded before the plaintext was found:")
    for g in 'ABC':
        xs = [r for r in aligned if r['blind_grade'] == g]
        right = [r for r in xs if r['blind_reading'] == r['plain_char']]
        wrong = ' '.join(f"#{r['idx']} {r['blind_reading']}->{r['plain_char']}" for r in xs if r not in right)
        print(f"  {g}: {len(right)} of {len(xs)} right" + (f"; wrong: {wrong}" if wrong else ''))

    exact = [r for r in full if r['class'] == 'exact']
    seen_t, seen_u = set(), set()
    for r in exact:
        i = int(r['stc']) - 1
        seen_t.add(i // 10 % 10)
        seen_u.add(i % 10)
    print(f"\nTens substitutions confirmed by an exact match: {len(seen_t)} of 10; "
          f"units: {len(seen_u)} of 10.")
    if bad:
        sys.exit(1)


def load_ctc(path):
    table = {}
    with open(path, encoding='utf-8') as f:
        for row in csv.reader(f):
            if row and row[0].isdigit():
                table[row[0].zfill(4)] = row[1]
    return table


def main(argv):
    ctc = {}
    if '--ctc' in argv:
        k = argv.index('--ctc')
        ctc = load_ctc(argv[k + 1])
        argv = argv[:k] + argv[k + 2:]
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__)
        return
    cmd, args = argv[0], argv[1:]
    if cmd == 'verify':
        verify()
    elif cmd == 'enc':
        for a in args:
            print(a, '->', enc(a), ctc.get(a.zfill(4), ''))
    elif cmd == 'dec':
        for a in args:
            c = dec(a)
            print(a, '->', c or 'not a 平密 group', ctc.get(c, '') if c else '')
    elif cmd == 'pages':
        print('codebook page -> 平密 page number')
        for row in range(9):
            print('  '.join(f"{p:02d}>{page_number(p)}" for p in range(row * 9, row * 9 + 9)))
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == '__main__':
    main(sys.argv[1:])
