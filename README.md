# 平密 1926: an "undecipherable" telegram in the Yan Xishan papers, read and checked

On 16 May 1926 the office of Kong Fanwei (孔繁霨) and Li Demao (李德懋) forwarded to Yan Xishan a telegram in the 平密 (Pingmi) code that they could not read (職部無法譯出), and copied out all 106 four-digit groups. This repository gives the key to 平密, the groups, the reading, and its check against an independent plaintext: the same telegram in Yan's own register of received telegrams.

In short: the 平密 group of a character is its standard telegraph code minus 1, with the page written in base 9 (digits 1–9) and the tens and units passed through two fixed substitutions. The forwarded groups are the opening and the close of Li Shimao's (李實茂) telegram from Beijing of 11 May 1926.

## Documents

All four are in the Yan Xishan papers (閻錫山史料) at Academia Historica (國史館). Scans can be viewed online at [ahonline.drnh.gov.tw](http://ahonline.drnh.gov.tw) by item number. No scans are included here.

| Item | Date | What it is |
|---|---|---|
| 116-010108-0566-005 | 16 May 1926 | Kong Fanwei and Li Demao to Yan, in plain telegraph code: they forward a 平密 telegram they cannot read and copy its 106 groups. Covering slip and forms No. 1750 and 1751. |
| 116-010108-0568-014 | January 1926 | Telegrams from Wang Zhiping (王治平) to Yan with 平密 groups and the characters written beside them. Source of the key. |
| 116-010108-0569-005 | 29 April 1926 | Wang Zhiping to Yan, on forms of 中國電報局 with the decipherment above the groups. The same key. |
| 116-010101-0027-164 | 14 May 1926 | Fair copy in Yan's register 「閻伯川先生要電錄存」, headed 「北京李實茂平密軫電　五月十四日到」. The plaintext. |

## The covering telegram

Kong's covering telegram is in the standard code, and its text reads:

> 督辦閻鈞鑒：頃接轉來平密電一件。查平密係北京常駐員王治平所用密碼，此項電本存鈞署密電室張先生處，職部無法譯出，謹此轉呈。原電文曰：督辦閻、軍長孔鈞鑒：平密 [106 groups] 等語。伏乞鑒核電示。孔繁霨、李德懋叩。銑印

"To Duban Yan. We have just received a 平密 telegram passed on to us. 平密 is the code used by Wang Zhiping, the resident agent in Beijing. Its codebook is kept by Mr Zhang in the cipher room of your office, and our department cannot decipher it. We forward it. The original reads: 'To Duban Yan and Corps Commander Kong: 平密 [106 groups]'. We ask for your instructions. Kong Fanwei, Li Demao. 銑 [16th]."

## The key

From the January pairs (character written beside its group):

1. Take the standard telegraph code of the character and subtract 1.
2. The hundreds give the codebook page, 0–80. Write it in base 9 with the digits 1–9. This gives the first two digits.
3. Pass the tens digit and the units digit through fixed substitutions:

```
tens    0>0 1>8 2>6 3>4 4>2 5>9 6>7 7>5 8>3 9>1
units   0>2 1>4 2>6 3>8 4>0 5>1 6>3 7>5 8>7 9>9
```

Example: 軍 6511 → 6510 → page 65 = "83", tens 1 → 8, units 0 → 2 → **8382**.

Subtracting 1 matters for codes ending in 0. A row of the codebook runs from …1 to …0 (0351–0360 is one row), so a code ending in 0 is the tenth cell of its row. In the January pairs: 八 0360 → 1499, 開 7030 → 8869, 持 2170 → 3479, 謹 6210 → 7909, 日 2480 → 3759.

Page by page, step 2 is this table (codebook page > 平密 page number):

```
00>11  01>12  02>13  03>14  04>15  05>16  06>17  07>18  08>19
09>21  10>22  11>23  12>24  13>25  14>26  15>27  16>28  17>29
18>31  19>32  20>33  21>34  22>35  23>36  24>37  25>38  26>39
27>41  28>42  29>43  30>44  31>45  32>46  33>47  34>48  35>49
36>51  37>52  38>53  39>54  40>55  41>56  42>57  43>58  44>59
45>61  46>62  47>63  48>64  49>65  50>66  51>67  52>68  53>69
54>71  55>72  56>73  57>74  58>75  59>76  60>77  61>78  62>79
63>81  64>82  65>83  66>84  67>85  68>86  69>87  70>88  71>89
72>91  73>92  74>93  75>94  76>95  77>96  78>97  79>98  80>99
```

A 平密 group never has 0 in its first two digits. For related Chinese codes with renumbered pages (共密, 容密, 辰密) see S. Tomokiyo, [Cryptiana: Chinese codes](https://cryptiana.web.fc2.com/code/chinesecrypto_e2.htm).

`data/key_pairs.tsv` has the 26 pairs that were read clearly: 15 from January (0568-014) and 11 from April (0569-005). All 26 fit the key. The April telegram uses the same key as January.

## Reading the May groups

The copyist's figures are hard to read: 3 and 7 look alike, 8 is written like 3, 6 or 0, 6 like 1 or 8, 1 like 6 or 7, 2 like 7. Groups 83 and 91 are under the archive's stamp. The transcription is in `data/groups.tsv` (sheet, row, column; `?` is an illegible digit).

Applied to the groups, the key gave readable fragments. I made a blind reading and graded every character A, B or C by confidence before looking for any plaintext. Then I searched the catalogue for telegrams of mid-May 1926 about Yan Huiqing's cabinet and found 116-010101-0027-164. It is the same telegram.

## Result

- Kong's 106 groups are the opening and the close of Li Shimao's telegram of the 11th (軫):
  groups 1–89 = 「顏駿人因雨帥致玉帥魚電……增進中俄親善」,
  groups 92–106 = 「……帶反攻已被聯軍擊退云李實茂叩軫」.
- The middle, 162 characters, is not in the forwarded copy. Groups 90–91 sit at the join and are not resolved.
- 98 of the aligned groups can be read in full. Under the key, 36 match the plaintext exactly, 35 differ in one digit, 11 differ only by the copyist's usual confusions, and 16 disagree.
- Blind readings graded A were right in 42 cases out of 43 (B: 8 of 18, C: 3 of 13).
- Each of the ten tens substitutions and each of the ten units substitutions is confirmed by at least one exact match.
- Group 64 is 于 in the cipher; the register has 於.

Dates: 軫 is the 11th. The telegram reached Yan on 14 May (「五月十四日到」), and Kong's office forwarded its copy as unreadable on 16 May (銑). Kong's own covering telegram says why: the 平密 codebook was kept in Yan's office.

What the telegram says: Yan Huiqing has agreed to return to office; Feng Yuxiang reached Moscow on the 9th; Zhang Shusheng has gone to Mukden to sue for peace, and six terms are listed; the headquarters of the 討赤聯軍 opened on the 10th; guns were heard in Beijing from 3 a.m. — a counterattack of the Northwest Army (西北軍) near Changping and Shahe, repulsed by the Allied armies.

`data/alignment.tsv` has every group with the plaintext character, its standard code, the group the key gives, the class, and my blind reading with its grade.

## Check it yourself

```
python3 pingmi.py verify
```

prints every number above from the files in `data/`. Python 3, standard library only.

```
python3 pingmi.py enc 6511          # 6511 -> 8382
python3 pingmi.py dec 8382 --ctc tw.csv   # 8382 -> 6511 軍
python3 pingmi.py pages             # the page table
```

`--ctc` takes a code table such as `tw.csv` from [kirklin/chinese-telegraph-code](https://github.com/kirklin/chinese-telegraph-code). The standard codes in `data/` were taken from that table.

## Files

| File | What |
|---|---|
| `data/groups.tsv` | the 106 groups of 0566-005 as transcribed |
| `data/alignment.tsv` | group by group: plaintext character, standard code, key group, class, blind reading |
| `data/key_pairs.tsv` | January and April pairs, character and group |
| `data/plaintext_0027-164.txt` | the plaintext from Yan's register |
| `pingmi.py` | the key and the check |

## Credits and license

Ivan Sourvillo, November 2026. I did this work with Claude agents (Anthropic), and every step is documented.

Code: MIT. Transcriptions, tables and text: CC BY 4.0.
