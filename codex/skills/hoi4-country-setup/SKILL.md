---
name: hoi4-country-setup
description: Create new countries or edit starting conditions in the BSM mod - country tags, common/countries color/gfx, history/countries (capital, politics, popularities, technology, ideas, characters), state ownership/cores, flags, names, and localisation. Use when (1) Adding a brand-new country tag ("新しい国家を追加", "国を作って"), (2) Editing a country's 1936 start (政治体制・人気度・初期技術・国民精神・首都), (3) Changing state ownership/cores ("この州を〜領に"), (4) Wiring characters/flags/names for a country, or (5) Fixing startup issues caused by tag definitions.
---

# HOI4 Country Setup (国家の初期状態)

新規国家の追加と、既存国家の開始時状態(1936)の編集。BSM modの実規約に準拠。
陸空OOBの中身は `hoi4-land-air-oob`、海軍は `hoi4-naval-oob-editor`、AI挙動は `hoi4-ai-modding` を使う。

## 新規国家追加チェックリスト(全7点セット)

| # | ファイル | 内容 |
|---|---|---|
| 1 | `common/country_tags/bsm_default_countries.txt` | TAG定義(地域コメント節に追記) |
| 2 | `common/countries/<region>.txt` | 既存地域ファイルを指すだけなら不要。色は `common/countries/colors.txt` |
| 3 | `history/countries/TAG - Name.txt` | 開始時状態(下記テンプレート) |
| 4 | `history/states/*.txt` | 領土(owner / add_core_of) |
| 5 | `gfx/flags/TAG.tga` (+ small/, medium/) | 国旗(hoi4-image-asset-creatorで作成可) |
| 6 | `common/characters/TAG.txt` | 指導者・閣僚(なければ汎用) |
| 7 | `localisation/japanese/` | TAG名キー |

検索は `hoi4-searcher` を使う(例: 既存characterの確認 `--type character --name '^TAG'`)。

## 1. country_tags

```
TAG	= "countries/Asia.txt"	#日本語コメント
```

- TAGは3文字大文字・既存と重複禁止(確認: `grep -rh '^TAG' common/country_tags/`)
- **重大な罠**: `dynamic_tags = yes` を含むファイルより**辞書順で後**のファイルに静的国家を置かない。
  dynamic_tags指定は後続ファイルへ引き継がれ、動的タグ扱いの国が開始時に領土を持つと起動時SIGFPEでクラッシュする
  (`zzz_dynamic_countries.txt` が最後尾にあるのはこのため。静的国家は `bsm_default_countries.txt` へ)

## 2. history/countries テンプレート(WES実例ベース)

ファイル名は `TAG - 英語名.txt` 形式。

```
capital = 271                       # state ID

oob = "Default_oob"                 # 専用OOBを作るまでは Default_oob(240カ国が使用)

# 初期技術: 個別指定 or BSMのtech_levelエフェクト
set_technology = {
  infantry_weapons = 1
  tech_support = 1
}
# set_tech_level_2 = yes            # まとめて指定(scripted_effects参照)

add_ideas = TAG_some_spirit         # 国民精神(hoi4-idea-creatorで作成)
set_convoys = 20

# 政治: BSMは political_set_* scripted effect を使う(直接set_politicsを書かない)
# 定義: common/scripted_effects/_bsm_set_politics.txt
# n=中道(選挙なし) N=中道(選挙あり) d=民主 s=共産 f等は定義ファイル参照
political_set_n = yes

set_popularities = {                # 合計100。イデオロギー名は改名済みトークン
  democratic_ideology = 25
  fascism_ideology = 20
  communism_ideology = 5
  neutrality_ideology = 50
}

recruit_character = TAG_leader_name # common/characters/TAG.txt に定義
```

- イデオロギーは必ず `*_ideology` トークン(communism_ideology 等)。素の `communism` はBSMでは存在しない
- DLC分岐が必要な要素は `if = { limit = { has_dlc = "..." } ... }` で囲む(OOB分岐の例は hoi4-land-air-oob 参照)

## 3. 領土(history/states)

既存stateの `history` ブロックを編集する:

```
history = {
  owner = TAG
  add_core_of = TAG                 # コア(既存ownerのコアを残すか判断)
  victory_points = { 3838 1 }
  buildings = { infrastructure = 2 industrial_complex = 1 }
}
```

- state IDの特定: `grep -rn 'owner = XXX' history/states/` や state名で検索
- **stateの新設・province変更はマップ編集**(別作業)。province構成を触ったら `naval_dist.cache` 等のキャッシュ削除が必要になるので安易にやらない
- capital に指定した state は必ず自国 owner であること

## 4. 国旗

- `gfx/flags/TAG.tga`(82x52)、`gfx/flags/small/TAG.tga`(10x7)、`gfx/flags/medium/TAG.tga`(41x26)
- イデオロギー別: `TAG_fascism_ideology.tga` 等(改名済みトークン名で。無ければデフォルトにフォールバック)
- 素材はリポジトリの `flags/00〜03/` に保管されている。生成・変換は `hoi4-image-asset-creator` + `mcp__hoi4__hoi4_convert_images`

## 5. characters / names / localisation

- `common/characters/TAG.txt`: 指導者(country_leader)を最低1人。`recruit_character` を忘れると指導者不在
- 未定義キャラを `recruit_character` するとerror.log行き。先に `hoi4-searcher --type character --name '^TAG'` で確認
- `common/names/` (汎用人名) と `common/units/names_divisions/TAG_names_divisions.txt`(師団名、任意)
- localisation 最低限:

```yaml
l_japanese:
 TAG:0 "国名"
 TAG_DEF:0 "国名"
 TAG_ADJ:0 "形容詞形"
 # 政体別: TAG_neutrality_ideology:0 等(任意)
```

## 検証

1. `python3 .claude/skills/hoi4-searcher/scripts/search_defs.py --check <変更ファイル>`
2. loc: `mcp__hoi4__hoi4_find_missing_keys`
3. 起動して国家選択画面で確認 → `tag TAG` で政治・閣僚・領土を目視
4. error.log に `recruit_character`/idea/flag の欠落警告がないか(`debug-trace` スキル)
