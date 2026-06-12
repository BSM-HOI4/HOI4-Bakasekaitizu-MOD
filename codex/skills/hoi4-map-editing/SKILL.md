---
name: hoi4-map-editing
description: Safe map editing procedures for the BSM mod - map/ files (definition.csv, provinces.bmp, strategicregions, adjacencies, rivers, supply), state province membership, and the mandatory cache-deletion + 2-launch verification that prevents delayed crashes. Use when (1) Editing anything under bakasekai/map/ ("マップ編集", "戦略地域", "strategic region", "province追加"), (2) Moving provinces between states, (3) Debugging crashes that happen on the SECOND launch or "deleting naval_dist.cache fixes it once", (4) adjacencies/supply/railway/river changes, or (5) Before launching after any map-touching change.
---

# HOI4 Map Editing Safety (マップ編集の安全手順)

BSM modは独自マップ。マップ編集は**1回目の起動では動いて2回目で落ちる**遅延クラッシュを生みやすい。
このスキルは編集そのものの手順と、必須の後処理(キャッシュ削除+2回起動検証)を定める。

## なぜ2回目に落ちるのか(2026-06-02に逆解析で特定)

戦略地域グラフが破損していても、HOI4はキャッシュ**生成**時(初回起動)は警告を出しつつ自己整合的に書き込むため動く。
しかし次回起動の**ロード**経路は `naval_dist.cache` の値を無検証で信用し、再構築した地域indexテーブルとズレて
範囲外参照→SIGSEGV。`naval_dist_checksum.cache` は「メモリ上の派生配列のMD5」であって
マップファイルのハッシュではないため、**ファイルを直しても古いキャッシュが残っていれば一致扱いでロードされ再発する**。
(Rosetta下ではクラッシュレポートも残らない)

## 編集後の必須手順(順番厳守)

```bash
# 1. 整合性チェック(0.5秒で完了。NGなら起動前に修正)
python3 .claude/skills/hoi4-map-editing/scripts/check_map.py

# 2. キャッシュを必ず「両方一緒に」削除
rm -f "$HOME/Documents/Paradox Interactive/Hearts of Iron IV/naval_dist.cache" \
      "$HOME/Documents/Paradox Interactive/Hearts of Iron IV/naval_dist_checksum.cache"
```

3. **2回起動テスト**: 1回目起動(キャッシュ再生成)→終了→**2回目起動**(キャッシュロード。従来落ちる回)→
   メインメニュー到達でOK。1回だけの起動確認では不十分
4. error.log で `strategicregiontemplate.cpp` の `"Couldn't locate a position"` が出ていないこと

## 「マップ編集」に該当する変更(=上記手順が必要)

- `map/definition.csv`(province定義)、`map/provinces.bmp` 等のビットマップ
- `map/strategicregions/*.txt`(戦略地域の id・provinces・naval_terrain)
- `map/adjacencies.csv` / `adjacency_rules.txt`(海峡・接続)
- `map/supply_nodes.txt` / `railways.txt`
- `history/states/*.txt` の **provinces ブロック**(州の領域変更。owner/coreだけなら不要だが、迷ったら削除して損はない)

## 守るべき不変条件(check_map.pyが自動検査)

1. 戦略地域IDの重複ゼロ(過去事例: 偽`245-kagawa.txt`が南極海域id=245を奪い58州が二重所属→クラッシュ)
2. 各provinceは厳密に1つの戦略地域のみに所属
3. `definition.csv` にprovince IDとRGB色の重複なし
4. 各provinceは1つのstateのみに所属
5. state/戦略地域が参照するprovinceは definition.csv に存在する

## 編集作業のガイド

- **編集前**: 対象ファイルをバックアップ(`cp file file.backup` — `rivers.bmp.backup` の前例あり)
- **戦略地域の追加/変更**: 既存ファイルの命名 `<id>-<name>.txt` に従う。idは既存最大値の確認から
  (`grep -rhoE 'id *= *[0-9]+' bakasekai/map/strategicregions/ | grep -oE '[0-9]+' | sort -n | tail -1`)。
  海域は `naval_terrain` を指定する
- **stateへのprovince移動**: 移動元と移動先の両方の `provinces = {}` を更新(片方だけだと二重所属/孤児になる)。
  victory_points・buildings内のprovince位置指定(naval_base等)も移動に追従させる
- **rivers.bmp**: インデックスパレット必須。詳細は `documents/03_map/01_River.md`。
  error.log の `map.cpp:667` がパレット不正の指標
- **ゲーム内Nudge**: コンソール `nudge` でマップエディタが開くが、**ファイルを直接書き換える**ので
  起動前に必ずgitがクリーンな状態で使い、差分をレビューする
- 大規模なprovince再配置・bmp編集は人間の確認を取ってから行う(復旧コストが高い)

## 関連する別系統のクラッシュ(マップと混同しない)

- 起動時ローディング画面で固まる → `settings.txt` のbackground/weight破損(ユーザーデータ側)。マップ無関係
- 世界初期化でSIGFPE → dynamic_tags扱いの国が開始時領土保有(`hoi4-country-setup` 参照)
- 診断の進め方は `debug-trace` スキル + `documents/hoi4_crash_debug_20260604.md`

## 関連ファイル・資料

- `bakasekai/map/` — 実ファイル群(definition.csv, strategicregions/ 283ファイル, adjacencies.csv 等)
- `documents/03_map/01_River.md` — 河川編集
- state所有権・コアの変更(provinces非変更)は `hoi4-country-setup` の領分
