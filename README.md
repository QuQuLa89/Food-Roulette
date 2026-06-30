# Food Roulette

食材・国・世界観・ランダムワードのランダムな組み合わせで、ユニークな料理アイデアを生成するCLIツールです。

## 特徴

- 4カテゴリ（食材 / 国 / 世界観 / ランダムワード）から1つずつランダム抽選
- 抽選結果と生成アイデアを `results.json` に自動保存
- 過去の結果をカテゴリ別に検索
- 外部依存ゼロ（Python 3.10+ 標準ライブラリのみ）

## 使い方

```bash
# ルーレットを回す（結果は自動保存）
python food_roulette.py spin

# 保存しないで回す
python food_roulette.py spin --no-save

# 履歴を全件表示（新しい順）
python food_roulette.py history

# 直近5件だけ表示
python food_roulette.py history -n 5

# カテゴリで検索
python food_roulette.py search 食材 鮭
python food_roulette.py search 国 フランス
python food_roulette.py search 世界観 サイバーパンク
python food_roulette.py search ワード 雨季

# カテゴリ名は英語も使えます
python food_roulette.py search ingredient 牛肉
python food_roulette.py search country タイ
python food_roulette.py search world 江戸時代
python food_roulette.py search word 月光

# カテゴリ一覧（全アイテム）を表示
python food_roulette.py categories
```

## 実行例

```
──────────────────────────────────────────────────
  ルーレット結果
──────────────────────────────────────────────────
  食材        : ホタテ
  国          : モロッコ
  世界観      : スチームパンク
  ランダムワード: 霧
──────────────────────────────────────────────────
  アイデア: 霧 の夜に生まれた、モロッコ×スチームパンク の ホタテ レシピ
  [結果を保存しました -> results.json]
──────────────────────────────────────────────────
```

## カテゴリ（抜粋）

| カテゴリ | 例 |
|---|---|
| 食材 | 鮭・マグロ・牛肉・なす・豆腐 … (38種) |
| 国 | アメリカ・フランス・インド・タイ … (20種) |
| 世界観 | サイバーパンク・江戸時代・宇宙コロニー … (15種) |
| ランダムワード | 雨季・月光・霧・桜吹雪 … (25種) |

## ファイル構成

```
Food-Roulette/
├── food_roulette.py   # メインスクリプト（依存なし）
├── results.json       # 抽選結果（自動生成・.gitignore対象）
├── .gitignore
└── README.md
```

## 要件

- Python 3.10 以上
