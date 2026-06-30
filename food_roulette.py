#!/usr/bin/env python3
"""
食品アイデアルーレット
食材・国・世界観・ランダムワードの組み合わせで料理アイデアを生成するCLIツール

使い方:
  python food_roulette.py spin                   # ルーレットを回す
  python food_roulette.py spin --no-save         # 保存しない
  python food_roulette.py history                # 全履歴を表示
  python food_roulette.py history -n 10          # 直近10件を表示
  python food_roulette.py search 食材 鮭         # カテゴリ検索
  python food_roulette.py categories            # カテゴリ一覧を表示
"""

import argparse
import json
import random
import sys
from datetime import datetime
from pathlib import Path

# Windows環境でのUTF-8出力を強制
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# ─────────────────────────────────────────
# データ定義
# ─────────────────────────────────────────

INGREDIENTS: list[str] = [
    # 魚介
    "鮭", "マグロ", "タコ", "イカ", "サバ", "鯛", "ウナギ", "カツオ", "エビ", "ホタテ",
    "アジ", "ブリ", "ヒラメ", "カニ", "牡蠣",
    # 肉
    "牛肉", "豚肉", "鶏肉", "羊肉", "鴨肉", "ベーコン", "ラム肉", "猪肉",
    # 野菜
    "トマト", "じゃがいも", "なす", "ほうれん草", "かぼちゃ", "にんじん", "ゴーヤ",
    "れんこん", "ごぼう", "たけのこ",
    # その他
    "豆腐", "しいたけ", "舞茸", "卵", "チーズ", "米", "パスタ", "そば",
]

COUNTRIES: list[str] = [
    "アメリカ", "フランス", "イタリア", "日本", "中国", "インド",
    "メキシコ", "タイ", "スペイン", "モロッコ", "ブラジル", "ペルー",
    "エチオピア", "韓国", "トルコ", "ベトナム", "ギリシャ", "レバノン",
    "アルゼンチン", "ポルトガル",
]

WORLDS: list[str] = [
    "サイバーパンク", "ファンタジー中世", "スチームパンク", "近未来SF",
    "西部開拓時代", "江戸時代", "北欧神話時代", "ディストピア",
    "宇宙コロニー", "海底都市", "妖怪の世界", "レトロフューチャー",
    "ポスト・アポカリプス", "古代文明", "魔法学校",
]

RANDOM_WORDS: list[str] = [
    "雨季", "茶葉", "月光", "霧", "錆", "砂嵐", "桜吹雪", "深夜", "真夏", "雪解け",
    "廃墟", "蜃気楼", "満潮", "霜", "煙草の煙", "泥炭", "星屑", "珊瑚",
    "枯れ葉", "朝靄", "稲妻", "潮風", "蜂蜜", "火山灰", "永久凍土",
]

IDEA_TEMPLATES: list[str] = [
    "{世界観}の{国}風 {食材} 料理 ―― {ランダムワード} をテーマに",
    "{ランダムワード} の夜に生まれた、{国}×{世界観} の {食材} レシピ",
    "{国} の {世界観} 世界で食べられる {食材} 使いの一皿（{ランダムワード}）",
    "{世界観} 的解釈による {国} 料理：{食材} と {ランダムワード} の融合",
    "{ランダムワード} にインスパイアされた {世界観} の {国} × {食材}",
    "{国} 出身の {世界観} シェフが {ランダムワード} から着想した {食材} 料理",
]

RESULTS_FILE = Path(__file__).parent / "results.json"

CATEGORY_ALIASES: dict[str, str] = {
    "食材": "食材",
    "ingredient": "食材",
    "ingredients": "食材",
    "国": "国",
    "country": "国",
    "countries": "国",
    "世界観": "世界観",
    "world": "世界観",
    "worlds": "世界観",
    "ワード": "ランダムワード",
    "word": "ランダムワード",
    "words": "ランダムワード",
    "ランダムワード": "ランダムワード",
}

# ─────────────────────────────────────────
# ストレージ
# ─────────────────────────────────────────

def load_results() -> list[dict]:
    if not RESULTS_FILE.exists():
        return []
    try:
        data = RESULTS_FILE.read_text(encoding="utf-8")
        return json.loads(data)
    except (json.JSONDecodeError, OSError) as e:
        print(f"[警告] 履歴ファイルの読み込みに失敗しました: {e}", file=sys.stderr)
        return []


def save_result(entry: dict) -> None:
    results = load_results()
    results.append(entry)
    RESULTS_FILE.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

# ─────────────────────────────────────────
# ルーレット・アイデア生成
# ─────────────────────────────────────────

def spin() -> dict[str, str]:
    return {
        "食材": random.choice(INGREDIENTS),
        "国": random.choice(COUNTRIES),
        "世界観": random.choice(WORLDS),
        "ランダムワード": random.choice(RANDOM_WORDS),
    }


def generate_idea(combo: dict[str, str]) -> str:
    return random.choice(IDEA_TEMPLATES).format(**combo)

# ─────────────────────────────────────────
# 表示ヘルパー
# ─────────────────────────────────────────

SEP = "─" * 50

def print_entry(index: int | None, entry: dict) -> None:
    ts = entry.get("timestamp", "")[:16].replace("T", " ")
    prefix = f"[{index:>4}] " if index is not None else "      "
    print(f"{prefix}{ts}")
    print(f"       食材: {entry.get('食材', '-')}")
    print(f"         国: {entry.get('国', '-')}")
    print(f"      世界観: {entry.get('世界観', '-')}")
    print(f"    ランダムワード: {entry.get('ランダムワード', '-')}")
    print(f"      アイデア: {entry.get('アイデア', '-')}")
    print()

# ─────────────────────────────────────────
# サブコマンド実装
# ─────────────────────────────────────────

def cmd_spin(args: argparse.Namespace) -> None:
    combo = spin()
    idea = generate_idea(combo)

    print(f"\n{SEP}")
    print("  ルーレット結果")
    print(SEP)
    print(f"  食材        : {combo['食材']}")
    print(f"  国          : {combo['国']}")
    print(f"  世界観      : {combo['世界観']}")
    print(f"  ランダムワード: {combo['ランダムワード']}")
    print(SEP)
    print(f"  アイデア: {idea}")

    if not args.no_save:
        entry = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "timestamp": datetime.now().isoformat(),
            **combo,
            "アイデア": idea,
        }
        save_result(entry)
        print("  [結果を保存しました -> results.json]")

    print(f"{SEP}\n")


def cmd_history(args: argparse.Namespace) -> None:
    results = load_results()
    if not results:
        print("保存済みの結果はありません。まず 'spin' コマンドを実行してください。")
        return

    limit = args.limit or len(results)
    recent = list(reversed(results[-limit:]))

    print(f"\n履歴 (最新 {len(recent)} 件 / 全 {len(results)} 件)\n{SEP}\n")
    for i, entry in enumerate(recent, 1):
        print_entry(i, entry)


def cmd_search(args: argparse.Namespace) -> None:
    results = load_results()
    if not results:
        print("保存済みの結果はありません。まず 'spin' コマンドを実行してください。")
        return

    category = CATEGORY_ALIASES.get(args.category)
    if not category:
        valid = "食材/ingredient, 国/country, 世界観/world, ワード/word"
        print(f"エラー: カテゴリ '{args.category}' は無効です。\n利用可能: {valid}")
        sys.exit(1)

    query = args.query
    matched = [r for r in results if query in r.get(category, "")]

    if not matched:
        print(f"'{query}' ({category}) に一致する結果は見つかりませんでした。")
        return

    print(f"\n検索結果: {category} = '{query}' ({len(matched)} 件)\n{SEP}\n")
    for i, entry in enumerate(reversed(matched), 1):
        print_entry(i, entry)


def cmd_categories(_args: argparse.Namespace) -> None:
    def fmt(items: list[str], cols: int = 5) -> str:
        rows = [items[i:i + cols] for i in range(0, len(items), cols)]
        return "\n    ".join("  ".join(f"{v:<12}" for v in row) for row in rows)

    print(f"\nカテゴリ一覧\n{SEP}")
    print(f"\n[食材] ({len(INGREDIENTS)} 種)")
    print(f"    {fmt(INGREDIENTS)}")
    print(f"\n[国] ({len(COUNTRIES)} 種)")
    print(f"    {fmt(COUNTRIES)}")
    print(f"\n[世界観] ({len(WORLDS)} 種)")
    print(f"    {fmt(WORLDS)}")
    print(f"\n[ランダムワード] ({len(RANDOM_WORDS)} 種)")
    print(f"    {fmt(RANDOM_WORDS)}")
    print()

# ─────────────────────────────────────────
# エントリーポイント
# ─────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="food_roulette",
        description="食品アイデアルーレット - 食材・国・世界観・ランダムワードの組み合わせで料理アイデアを生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
コマンド例:
  python food_roulette.py spin
  python food_roulette.py spin --no-save
  python food_roulette.py history
  python food_roulette.py history -n 5
  python food_roulette.py search 食材 鮭
  python food_roulette.py search country フランス
  python food_roulette.py categories
        """,
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True

    p_spin = sub.add_parser("spin", help="ルーレットを回してアイデアを生成・保存")
    p_spin.add_argument("--no-save", action="store_true", help="結果を results.json に保存しない")
    p_spin.set_defaults(func=cmd_spin)

    p_hist = sub.add_parser("history", help="過去の抽選結果を新しい順に表示")
    p_hist.add_argument("-n", "--limit", type=int, metavar="N", help="表示する件数 (省略時: 全件)")
    p_hist.set_defaults(func=cmd_history)

    p_search = sub.add_parser("search", help="カテゴリと検索ワードで過去の結果を絞り込む")
    p_search.add_argument(
        "category",
        help="カテゴリ名 (食材/ingredient, 国/country, 世界観/world, ワード/word)",
    )
    p_search.add_argument("query", help="検索キーワード (例: 鮭, フランス)")
    p_search.set_defaults(func=cmd_search)

    p_cats = sub.add_parser("categories", help="全カテゴリのアイテム一覧を表示")
    p_cats.set_defaults(func=cmd_categories)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
