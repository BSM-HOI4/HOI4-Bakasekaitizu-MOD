---
name: hoi4-land-air-oob
description: Create or edit Hearts of Iron IV land and air orders of battle (OOB) in the BSM mod - division_template definitions, starting divisions (units/division blocks), air_wings, instant_effect equipment production, and DLC-conditional OOB wiring (oob=/set_oob/set_air_oob). Use when (1) Adding starting divisions/army to a country ("初期師団", "陸軍OOB", "開始時の軍隊"), (2) Creating/editing division templates ("師団テンプレート"), (3) Adding starting air wings ("航空隊", "air OOB"), or (4) Wiring TAG_1936/_nsb/_air files to history/countries. Naval OOB uses hoi4-naval-oob-editor instead.
---

# HOI4 Land & Air OOB (陸空の初期配備)

`history/units/` の陸軍・空軍OOBの作成・編集。海軍OOBは `hoi4-naval-oob-editor`(NVRW/hidden_slot方式)を使う。
国家側の初期状態(政治・技術・領土)は `hoi4-country-setup`。

## ファイル構成と配線(最重要)

OOBファイルは **history/countries から参照されて初めてロードされる**。置いただけでは死にファイルになる
(実例: `JPN_1936_air_bba.txt` / `_air_legacy.txt` は現在未配線で機能していない)。

```
# history/countries/TAG - Name.txt 側
oob = "TAG_1936"                      # 陸軍(基本)。専用がなければ "Default_oob"

if = {                                # NSB有無で師団構成を分ける場合
  limit = { NOT = { has_dlc = "No Step Back" } }
  set_oob = "TAG_1936"
}
if = {
  limit = { has_dlc = "No Step Back" }
  set_oob = "TAG_1936_nsb"
}

if = {                                # 空軍を別ファイルにする場合(BBA分岐)
  limit = { has_dlc = "By Blood Alone" }
  set_air_oob = "TAG_1936_air_bba"
}
if = {
  limit = { NOT = { has_dlc = "By Blood Alone" } }
  set_air_oob = "TAG_1936_air_legacy"
}
```

- 命名: `TAG_1936.txt` / `TAG_1936_nsb.txt` / `TAG_1936_air_bba.txt` / `TAG_1936_air_legacy.txt` / 内戦用 `TAG_civilwar.txt`
- 小規模国は air_wings を陸軍OOBファイル内に直接書いてよい(MLT_1936.txt方式)。別ファイル化はDLC分岐が要るときだけ

## division_template(CHN_1936実例ベース)

```
division_template = {
  name = "Sanjiao Jun"                # OOB内で一意。divisionから文字列参照される
  division_names_group = CHI_INF_01   # 任意: common/units/names_divisions/ のグループ

  regiments = {                       # 戦闘大隊。x=列(0〜4) y=行(0〜4)
    infantry = { x = 0 y = 0 }
    infantry = { x = 0 y = 1 }
    infantry = { x = 1 y = 0 }
  }
  support = {                         # 支援中隊。x=0固定 y=0〜4
    artillery = { x = 0 y = 0 }
    engineer = { x = 0 y = 1 }
  }
  priority = 1                        # 任意: 装備配分優先度(0=低 1=通常 2=高)
}
```

- 大隊名(infantry, artillery, light_armor, mountaineers, motorized, mot_recon 等)は `common/units/*.txt` の定義名。
  存在確認: `hoi4-searcher` か `grep -rl '^<name> = {' bakasekai/common/units/`
- 格子座標の重複は不可。列を飛ばさない(x=0を埋めてからx=1)
- その大隊の前提技術を国が `set_technology` で持っていないと、師団は装備0で出現する。
  `hoi4-country-setup` の初期技術とセットで設計する

## 開始時師団(units ブロック)

```
units = {
  division = {                        # name か division_names_group のどちらかで命名
    location = 11913                  # province ID(state IDではない)
    division_template = "Sanjiao Jun"
    start_experience_factor = 0.2     # 0〜1
    start_equipment_factor = 0.85     # 1未満=充足率低い状態で開始
  }
}
```

- province IDの調べ方: 対象stateの `history/states/*.txt` の `provinces = { ... }` から選ぶ(VP provinceが無難)。
  ゲーム内では `tdebug` でマウスオーバー表示
- 大量配置は同じ division ブロックをコピーする(1ブロック=1師団)

## 空軍(air_wings)

```
air_wings = {
  282 = {                             # ★state ID(provinceではない)。air_baseがあるstate
    small_plane_airframe_0 = {        # BBA機体型(legacy版は fighter_equipment_0 等)
      owner = "JPN"
      amount = 72
      version_name = "キ-10"          # 任意: create_equipment_variant の name と完全一致
    }
  }
}
```

- BBA airframe型: `small_plane_airframe_X`(戦闘機) / `small_plane_cas_airframe_X` / `medium_plane_airframe_X` 等
- `version_name` を指定する場合、そのバリアントが国の scripted_effect 等で先に作成されていること
  (BSMでは `TAG_air_design = yes` のような設計エフェクトを history/countries 側で呼ぶ)
- 配備先stateに `air_base` が必要(`history/states` の buildings)

## 開始時生産ライン(instant_effect)

```
instant_effect = {
  add_equipment_production = {
    equipment = { type = infantry_equipment_0 creator = "TAG" }
    requested_factories = 1
    progress = 0.87
    efficiency = 50
  }
}
```

## 検証

1. `python3 .claude/skills/hoi4-searcher/scripts/search_defs.py --check history/units/<file>`
2. **配線確認**: `grep -rn "TAG_1936" bakasekai/history/countries/` で参照されているか(未配線が最頻バグ)
3. 起動 → 国家選択画面の師団数表示 → `tag TAG` で配備位置・装備充足を確認
4. error.log に template/equipment/location の警告がないか(`debug-trace`)
