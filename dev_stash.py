#!/usr/bin/env python3
"""
dev_stash.py — Mod本体データ以外（.git・隠しフォルダ・開発ツール類）を退避/復元する

Steam Workshop アップロード用に、HOI4 が読み込む「Mod本体データ」だけを
ルートに残し、それ以外（.git, .venv, .idea, .claude, documents, scripts,
codex, tools, 一時ファイル等）を **リポジトリルートの外** にある退避先
ディレクトリへ丸ごと移動する。

このプロジェクトの構造:
  HOI4-Bakasekaitizu-MOD/          ← リポジトリルート（ここにこのスクリプト）
    bakasekai/                      ← HOI4 が読む Mod 本体（whitelist）
      descriptor.mod
      common/, events/, gfx/ …
    .git/, .claude/, documents/ …   ← 退避対象

退避先は リポジトリルートの外（兄弟ディレクトリ）に作るため、退避後には
「bakasekai/ ＋ このスクリプト1個」だけが残り、bakasekai/ をそのまま
Steam にアップできる。
移動内容は退避先の manifest.json に記録され、--restore で完全に元へ戻せる。

  退避先（既定）:  <ルートの親>/<ルート名>.devstash/

ホワイトリスト方式:
    MOD_WHITELIST（＋このスクリプト）以外をすべて退避する。新しい開発用
    ファイル/フォルダが増えても自動的に退避対象になる（取りこぼさない）。

使い方:
    python3 dev_stash.py                   # 退避ドライラン（表示のみ・既定）
    python3 dev_stash.py --apply           # 実際に退避を実行
    python3 dev_stash.py --restore         # 復元ドライラン
    python3 dev_stash.py --restore --apply # 実際に復元を実行
    python3 dev_stash.py --list            # 現在の分類を一覧表示
    python3 dev_stash.py --stash-dir PATH  # 退避先を明示指定
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 設定
# ---------------------------------------------------------------------------

MANIFEST_NAME = "manifest.json"

# HOI4 が読み込む Mod 本体データのみをここに挙げる。
# bakasekai/ の中に descriptor.mod・common・events・gfx 等が入っている。
MOD_WHITELIST = {
    "bakasekai",
}

# Mod 本体ではないがルートに残したいもの（任意で追加）。
# Steam アップ時に同梱が必要なファイルがあればここへ。
ALWAYS_KEEP: set[str] = set()


# ---------------------------------------------------------------------------
# 内部ユーティリティ
# ---------------------------------------------------------------------------

def repo_root() -> Path:
    """このスクリプトが置かれた場所＝リポジトリルートとみなす。"""
    return Path(__file__).resolve().parent


def script_basename() -> str:
    return Path(__file__).resolve().name


def default_stash_dir(root: Path) -> Path:
    """退避先（ルートの外＝兄弟ディレクトリ）。"""
    return root.parent / f"{root.name}.devstash"


def protected_names() -> set[str]:
    """退避してはいけない top-level エントリ名の集合。"""
    keep = set(MOD_WHITELIST) | set(ALWAYS_KEEP)
    keep.add(script_basename())  # スクリプト自身は復元に必要なので残す
    return keep


def classify(root: Path) -> tuple[list[str], list[str]]:
    """ルート直下を (残す, 退避する) に分類して返す。"""
    keep_names = protected_names()
    keep: list[str] = []
    stash: list[str] = []
    for name in sorted(os.listdir(root)):
        (keep if name in keep_names else stash).append(name)
    return keep, stash


def load_manifest(stash_dir: Path) -> list[str]:
    mf = stash_dir / MANIFEST_NAME
    if not mf.exists():
        return []
    try:
        data = json.loads(mf.read_text(encoding="utf-8"))
        return list(data.get("stashed", []))
    except (json.JSONDecodeError, OSError):
        return []


def save_manifest(stash_dir: Path, names: list[str]) -> None:
    (stash_dir / MANIFEST_NAME).write_text(
        json.dumps({"stashed": sorted(names)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# コマンド
# ---------------------------------------------------------------------------

def cmd_list(root: Path, stash_dir: Path) -> int:
    keep, stash = classify(root)
    print(f"リポジトリルート: {root}")
    print(f"退避先          : {stash_dir}/\n")
    print(f"■ 残す（Mod本体データ等）: {len(keep)} 件")
    for n in keep:
        print(f"    KEEP   {n}")
    print(f"\n■ 退避対象: {len(stash)} 件")
    for n in stash:
        print(f"    STASH  {n}")
    return 0


def cmd_stash(root: Path, stash_dir: Path, apply: bool) -> int:
    keep, to_stash = classify(root)

    if not to_stash:
        print("退避対象はありません。すでにクリーンです。")
        return 0

    mode = "実行" if apply else "ドライラン（--apply で実際に移動）"
    print(f"=== 退避 [{mode}] ===")
    print(f"退避先: {stash_dir}/\n")

    already = set(load_manifest(stash_dir)) if stash_dir.exists() else set()
    moved: list[str] = list(already)
    errors = 0

    for name in to_stash:
        src = root / name
        dst = stash_dir / name
        if dst.exists():
            print(f"  SKIP   {name}  (退避先に同名あり)")
            errors += 1
            continue
        print(f"  MOVE   {name}  ->  {stash_dir.name}/{name}")
        if apply:
            try:
                stash_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                moved.append(name)
            except OSError as e:
                print(f"  ERROR  {name}: {e}")
                errors += 1

    if apply and moved:
        save_manifest(stash_dir, moved)
        ok = len(to_stash) - errors
        print(f"\n{ok} 件を退避しました。ルートは Mod本体データのみになりました。")
        print(f"復元: python3 {script_basename()} --restore --apply")
    elif not apply:
        print(f"\n{len(to_stash)} 件が退避されます（ドライラン）。")
    if errors:
        print(f"警告: {errors} 件はスキップ/失敗しました。")
    return 1 if errors else 0


def cmd_restore(root: Path, stash_dir: Path, apply: bool) -> int:
    if not stash_dir.exists():
        print(f"退避ディレクトリ {stash_dir} がありません。復元するものはありません。")
        return 0

    names = load_manifest(stash_dir)
    if not names:
        print("manifest が空です。復元するものはありません。")
        return 0

    mode = "実行" if apply else "ドライラン（--apply で実際に移動）"
    print(f"=== 復元 [{mode}] ===")
    print(f"退避元: {stash_dir}/\n")

    restored: list[str] = []
    errors = 0
    for name in names:
        src = stash_dir / name
        dst = root / name
        if not src.exists():
            print(f"  MISS   {name}  (退避先に存在しない)")
            errors += 1
            continue
        if dst.exists():
            print(f"  SKIP   {name}  (復元先に同名あり)")
            errors += 1
            continue
        print(f"  MOVE   {stash_dir.name}/{name}  ->  {name}")
        if apply:
            try:
                shutil.move(str(src), str(dst))
                restored.append(name)
            except OSError as e:
                print(f"  ERROR  {name}: {e}")
                errors += 1

    if apply:
        remaining = [n for n in names if n not in restored]
        if remaining:
            save_manifest(stash_dir, remaining)
        else:
            # すべて戻したら manifest と（空なら）退避先を片付ける
            (stash_dir / MANIFEST_NAME).unlink(missing_ok=True)
            try:
                if not any(stash_dir.iterdir()):
                    stash_dir.rmdir()
            except OSError:
                pass
        print(f"\n{len(restored)} 件を復元しました。")
    else:
        print(f"\n{len(names)} 件が復元されます（ドライラン）。")
    if errors:
        print(f"警告: {errors} 件はスキップ/失敗しました。")
    return 1 if errors else 0


# ---------------------------------------------------------------------------
# エントリポイント
# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Mod本体データ以外（.git・隠しフォルダ・開発ツール）を退避/復元する",
    )
    parser.add_argument("--apply", action="store_true",
                        help="実際にファイルを移動する（既定はドライラン）")
    parser.add_argument("--restore", action="store_true",
                        help="退避したものを元の場所へ戻す")
    parser.add_argument("--list", action="store_true",
                        help="現在の分類（残す/退避）を一覧表示する")
    parser.add_argument("--stash-dir", metavar="PATH", default=None,
                        help="退避先ディレクトリを明示指定（既定: <親>/<ルート名>.devstash）")
    args = parser.parse_args(argv)

    root = repo_root()
    stash_dir = Path(args.stash_dir).resolve() if args.stash_dir else default_stash_dir(root)

    # 安全確認: bakasekai/descriptor.mod が存在するか確認
    if not (root / "bakasekai" / "descriptor.mod").exists():
        print(f"エラー: {root}/bakasekai/descriptor.mod が見つかりません。"
              " リポジトリルートでスクリプトを実行してください。", file=sys.stderr)
        return 2

    # 安全確認: 退避先がルート内だと自己参照で壊れるため拒否
    if root == stash_dir or root in stash_dir.parents:
        print(f"エラー: 退避先 {stash_dir} はリポジトリルートの外を指定してください。",
              file=sys.stderr)
        return 2

    if args.list:
        return cmd_list(root, stash_dir)
    if args.restore:
        return cmd_restore(root, stash_dir, args.apply)
    return cmd_stash(root, stash_dir, args.apply)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
