"""food_roulette のユニットテスト。"""

import argparse
from unittest.mock import patch

from food_roulette import cmd_history


def test_cmd_history_zero_limit(capsys) -> None:
    dummy_results = [
        {"食材": "トマト", "国": "イタリア", "世界観": "カフェ", "アイデア": "パスタ"}
    ]
    with patch("food_roulette.load_results", return_value=dummy_results):
        args = argparse.Namespace(limit=0)
        cmd_history(args)
        captured = capsys.readouterr()
        assert "エラー: 件数 (-n) には1以上の整数を指定してください。" in captured.out


def test_cmd_history_negative_limit(capsys) -> None:
    dummy_results = [
        {"食材": "トマト", "国": "イタリア", "世界観": "カフェ", "アイデア": "パスタ"}
    ]
    with patch("food_roulette.load_results", return_value=dummy_results):
        args = argparse.Namespace(limit=-5)
        cmd_history(args)
        captured = capsys.readouterr()
        assert "エラー: 件数 (-n) には1以上の整数を指定してください。" in captured.out


def test_cmd_history_valid_limit(capsys) -> None:
    dummy_results = [
        {"食材": "トマト", "国": "イタリア", "世界観": "カフェ", "アイデア": "パスタ"},
        {"食材": "豆腐", "国": "日本", "世界観": "居酒屋", "アイデア": "冷奴"},
    ]
    with patch("food_roulette.load_results", return_value=dummy_results):
        args = argparse.Namespace(limit=1)
        cmd_history(args)
        captured = capsys.readouterr()
        assert "履歴 (最新 1 件 / 全 2 件)" in captured.out
        assert "冷奴" in captured.out
