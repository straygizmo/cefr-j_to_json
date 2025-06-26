# CEFR-J Vocabulary CSV to JSON Converter

[English](#english) | [日本語](#japanese)

## <a name="english"></a>English

### Overview
This project converts CEFR-J vocabulary list CSV files into JSON format, providing a system that can retrieve CEFR levels from various word forms (past tense, past participle, progressive form, spelling variations, etc.).

The vocabulary list CSV files:
- [CEFR-J Wordlist: Version 1.6 (2020.3.24 更新版)](https://www.cefr-j.org/download.html) — vocabulary list annotated with CEFR-J (for A1 - B2) levels, created by [CEFR-J project](https://www.cefr-j.org/download.html)
- [Octanove Vocabulary Profile C1/C2 (ver 1.0)](https://github.com/openlanguageprofiles/olp-en-cefrj) — vocabulary list annotated with CEFR-J levels (for C1/C2 levels), created by [Octanove Labs](https://www.octanove.com/)

### Features
- Returns corresponding CEFR levels for words in various forms
- Supports American/British spelling differences
- Identifies base forms from conjugated verbs
- Enables fast reverse lookup

### Project Structure
```
cefr-j_to_json/
├── assets/                    # Input CSV files directory
│   └── *.csv                 # CSV files with headers: headword, pos, CEFR
├── main.py                   # Main conversion script
├── vocabulary.json           # Output: Complete vocabulary database
├── word_lookup.json         # Output: Fast lookup index
└── README.md                # This document
```

### Requirements
- Python 3.6+
- No external dependencies required

### Usage
```bash
python main.py
```

The script will automatically:
1. Scan all CSV files in the `assets` directory
2. Process only files where the first 3 columns are: `headword`, `pos`, `CEFR`
3. Generate two JSON output files (vocabulary.json, word_lookup.json)

### Input CSV Format
CSV files must have at least these three columns in order:
- **headword**: Entry word (may include slash-separated variants)
- **pos**: Part of speech
- **CEFR**: CEFR level (A1, A2, B1, B2, C1, C2)

Additional columns are preserved but optional.

### Output JSON Schema

#### vocabulary.json
Contains complete vocabulary entries with all word forms and variants:
```json
{
  "vocabulary": [
    {
      "word": "color/colour",
      "pos": "noun",
      "CEFR": "A1",
      "base_form": "color",
      "word_family": ["color", "colour", "colors", "colours", "colored", "coloured"],
      "variants": {
        "american": ["color", "colored", "coloring"],
        "british": ["colour", "coloured", "colouring"]
      }
    }
  ]
}
```

#### word_lookup.json
Provides fast O(1) lookup from any word form to its base form and CEFR level:
```json
{
  "taken": {"base_form": "take", "pos": "verb", "CEFR": "A1"},
  "colour": {"base_form": "color", "pos": "noun", "CEFR": "A1"},
  "analyzing": {"base_form": "analyze", "pos": "verb", "CEFR": "B1"}
}
```

### Special Processing

#### Slash-separated Variants
- `color/colour` → Both spellings added to word_family
- `a.m./A.M./am/AM` → All variants preserved

#### Verb Conjugations
- Regular verbs: Automatically generates -s, -ed, -ing forms
- Irregular verbs: Uses predefined mapping table
- Special handling for "be" and "do" verbs

#### Word Family Grouping
Groups words with the same base form:
- abandon (verb) + abandoned (adjective) → same family
- accept (verb) + acceptable (adjective) + acceptance (noun) → same family

### Usage Example
```python
import json

# Load the lookup table
with open('word_lookup.json', 'r') as f:
    lookup = json.load(f)

# Retrieve base form and CEFR level from any word form
print(lookup["taken"])      # → {"base_form": "take", "pos": "verb", "CEFR": "A1"}
print(lookup["colour"])     # → {"base_form": "color", "pos": "noun", "CEFR": "A1"}
print(lookup["analyzing"])  # → {"base_form": "analyze", "pos": "verb", "CEFR": "B1"}
```

---

## <a name="japanese"></a>日本語

### 概要
このプロジェクトは、CEFR-J語彙リストCSVファイルをJSONフォーマットに変換し、様々な単語形式（過去形、過去分詞形、進行形、スペルバリエーション等）から単一のCEFRレベルを検索できるシステムを提供します。
CEFR-J語彙リストCSVファイルのオリジナルは以下です。
- [CEFR-J Wordlist: Version 1.6 (2020.3.24 更新版)](https://www.cefr-j.org/download.html) — CEFR-J (A1 - B2レベル) を割り当てた語彙リスト。作成者: [CEFR-J project](https://www.cefr-j.org/download.html)
- [Octanove Vocabulary Profile C1/C2 (ver 1.0)](https://github.com/openlanguageprofiles/olp-en-cefrj) — CEFR-J (C1/C2レベル) を割り当てた語彙リスト。作成者: [Octanove Labs](https://www.octanove.com/)

### 機能
- 様々な形式の単語を入力として、対応するCEFRレベルを返す
- 米英スペルの違いに対応
- 動詞の活用形から基本形を特定
- 高速な逆引き検索を実現

### ファイル構成
```
cefr-j_to_json/
├── assets/                    # 入力CSVファイルディレクトリ
│   └── *.csv                 # ヘッダー: headword, pos, CEFR のCSVファイル
├── main.py                   # メインの変換スクリプト
├── vocabulary.json           # 出力：完全な語彙データベース
├── word_lookup.json         # 出力：高速検索用インデックス
└── README.md                # このドキュメント
```

### 必要環境
- Python 3.6以上
- 外部ライブラリは不要

### 使用方法
```bash
python main.py
```

スクリプトは自動的に：
1. `assets`ディレクトリ内のすべてのCSVファイルをスキャン
2. 最初の3列が `headword`, `pos`, `CEFR` であるファイルのみを処理
3. 2つのJSON出力ファイルを生成 (vocabulary.json, word_lookup.json)

### 入力CSVフォーマット
CSVファイルには最低限、以下の3つの列がこの順序で必要です：
- **headword**: 見出し語（スラッシュ区切りでバリエーション含む）
- **pos**: 品詞
- **CEFR**: CEFRレベル（A1, A2, B1, B2, C1, C2）

追加の列は保持されますが、必須ではありません。

### 出力JSONスキーマ

#### vocabulary.json
すべての語形とバリエーションを含む完全な語彙エントリ：
```json
{
  "vocabulary": [
    {
      "word": "color/colour",
      "pos": "noun",
      "CEFR": "A1",
      "base_form": "color",
      "word_family": ["color", "colour", "colors", "colours", "colored", "coloured"],
      "variants": {
        "american": ["color", "colored", "coloring"],
        "british": ["colour", "coloured", "colouring"]
      }
    }
  ]
}
```

#### word_lookup.json
任意の語形から基本形とCEFRレベルへのO(1)高速検索を提供：
```json
{
  "taken": {"base_form": "take", "pos": "verb", "CEFR": "A1"},
  "colour": {"base_form": "color", "pos": "noun", "CEFR": "A1"},
  "analyzing": {"base_form": "analyze", "pos": "verb", "CEFR": "B1"}
}
```

### 特殊な処理

#### スラッシュ区切りのバリエーション
- `color/colour` → 両方のスペルをword_familyに追加
- `a.m./A.M./am/AM` → すべてのバリエーションを保持

#### 動詞の活用形
- 規則動詞：自動的に -s, -ed, -ing 形を生成
- 不規則動詞：定義済みマッピングテーブルを使用
- be動詞、do動詞：特殊処理

#### 語族のグループ化
同じ基本形を持つ単語をグループ化：
- abandon (動詞) + abandoned (形容詞) → 同じ語族
- accept (動詞) + acceptable (形容詞) + acceptance (名詞) → 同じ語族

### 使用例
```python
import json

# ルックアップテーブルを読み込む
with open('word_lookup.json', 'r', encoding='utf-8') as f:
    lookup = json.load(f)

# 任意の形式から基本形とCEFRレベルを取得
print(lookup["taken"])      # → {"base_form": "take", "pos": "verb", "CEFR": "A1"}
print(lookup["colour"])     # → {"base_form": "color", "pos": "noun", "CEFR": "A1"}
print(lookup["analyzing"])  # → {"base_form": "analyze", "pos": "verb", "CEFR": "B1"}
```

### 実装の詳細

#### UTF-8 BOM対応
CSVファイルの先頭にあるBOM（Byte Order Mark）を適切に処理

#### 重複の処理
- 同じ単語が複数のCSVファイルに存在する場合、最も低いCEFRレベルを採用
- 追加情報はマージして保持

#### パフォーマンス最適化
- word_lookup.jsonによる O(1) の検索時間
- 大文字小文字を区別しない検索に対応

## Terms of use
CEFR-J vocabulary and grammar profile datasets can be used for research and commercial purposes with no charge, provided that you cite the dataset properly. The copyright belongs to Tono Laboratory at TUFS (Tokyo University of Foreign Studies). Neither CEFR-J nor Open Language Profiles is responsible or liable for any inaccuracies in the dataset or any damage resulting from using the dataset.

The Octanove Vocabulary Profile for C1/C2 levels can be used under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).

## License
This project is for educational and research purposes. Please check the license terms of the original CEFR-J vocabulary data.

## Credits
『CEFR-J Wordlist Version 1.6』 東京外国語大学投野由紀夫研究室. （URL: http://www.cefr-j.org/download.html より 2022 年 2 月ダウンロード）
