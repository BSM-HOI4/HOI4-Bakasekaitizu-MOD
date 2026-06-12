# HOI4 起動クラッシュ調査記録 2026-06-04

## 現象

- 対象 MOD: `bakasekai`
- 起動環境: macOS / Steam 版 HOI4 / Rosetta x86_64
- 当初の症状:
  - 1回目は起動できることがある
  - 2回目または3回目の起動でクラッシュまたはハングする
  - 停止位置はほぼ同じ
- 最新状態:
  - `career_profile_*.pr`、`naval_dist.cache`、`naval_dist_checksum.cache` などを削除すると起動できる
  - ただし、最新の map 形式修正後は「一回も起動できない」状態になった

## 参照した主なパス

- HOI4 ログ:
  - `/Users/eightman/Documents/Paradox Interactive/Hearts of Iron IV/logs`
- HOI4 実行ファイル:
  - `/Users/eightman/Library/Application Support/Steam/steamapps/common/Hearts of Iron IV/hoi4.app/Contents/MacOS/hoi4`
- 生成ファイル:
  - `/Users/eightman/Documents/Paradox Interactive/Hearts of Iron IV/career_profile_9B21E73601001001_v3.pr`
  - `/Users/eightman/Documents/Paradox Interactive/Hearts of Iron IV/naval_dist.cache`
  - `/Users/eightman/Documents/Paradox Interactive/Hearts of Iron IV/naval_dist_checksum.cache`
- MOD:
  - `/Users/eightman/Desktop/HOI4_modding/bsm_test/bakasekai`

## ログ上の特徴

### error.log

直近では致命的な script error は少ない。

- `Invalid supported_version` 系は外部 `.mod` の警告で、本件の本命ではなさそう
- `loc key collisions` は残るが、停止位置とは直接結びついていない
- 以前出ていた `rivers.bmp` の palette warning は、header 修正後には消えた

### memory.log

停止直前は毎回ほぼ同じ。

```text
InitGame:: CFrontEnd
InitGame()
InitMap:: CGraphicalMap
InitMap:: Init map stuff
frontend.cpp:444: _Super.InitMap
```

重要点:

- `no_game_date` のロードではなく、`1936.01.01.12` に入ったあとで止まる
- つまり main menu 初期化だけではなく、ゲーム開始後の map / frontend / runtime 初期化で止まっている

### system_debug.log

多くの `career_profile` GUI illegal position warning が出る。

ただし、これらは vanilla 側でも出るタイプの警告が多く、単独ではクラッシュ原因と断定できない。

MOD 側で目立ったもの:

```text
interface/replace/frontendmainview.gui(line 196):
Object "sp_tutorial_button" has illegal position with y: 11538
```

これは SSW / EoaNB 方式に寄せていたが、警告自体は残る。

## macOS crash report / live sample から見えたこと

クラッシュレポートでは以下が出ていた。

```text
Exception Type: EXC_CRASH (SIGABRT)
malloc_zone_error
nanov2_guard_corruption_detected
small_free_list_remove_ptr_no_clear
AGXMetal / Metal / Audio thread
```

解釈:

- Paradox script の通常エラーではない
- どこかでヒープ破壊が起きており、Metal / Audio / malloc 側で表面化している
- sample では `career_profile` 名の関数は直接出ていない
- `InitMap` 後に表面化しているため、map asset / map cache / frontend 初期化のいずれかが強い

採取した sample:

- `/tmp/hoi4_sample_58111_after_profile_map.txt`

## career_profile 仮説

根拠:

- `career_profile_9B21E73601001001_v3.pr` がクラッシュ時刻に再生成される
- `strings` で `kaiserreich_career_profile` が見えた
- 2回目/3回目起動で発生するという症状と、生成済み profile 読み込みは噛み合う

弱い点:

- live sample に `career_profile` 関数名は出ていない
- `career_profile_*.pr` だけでなく `naval_dist.cache` も消すと起動できる
- 現時点では profile 単独より、生成キャッシュ全体のうち map 側がより怪しい

実施済み:

- `career_profile_9B21E73601001001_v3.pr` を複数回退避
- 最新退避先:
  - `/tmp/hoi4_profile_map_cache_20260604_1/career_profile_9B21E73601001001_v3.pr`

## map / naval_dist 仮説

根拠:

- ユーザー報告:
  - 以下を削除すると起動できる
    - `launcher-v2.sqlite`
    - `career_profile_9B21E73601001001_v3.pr`
    - `settings.txt`
    - `pdx_settings.txt`
    - `logs`
    - `gameplaysettings.txt`
    - `naval_dist.cache`
    - `naval_dist_checksum.cache`
    - `crashes`
- 特に `naval_dist.cache` / `naval_dist_checksum.cache` は map 由来
- 停止位置が `InitMap` 後
- macOS 側では Metal / malloc のヒープ破壊として表面化

見つかった map 不整合:

- `default.map` は `tree_definition = "trees.bmp"` を要求している
- しかし `bakasekai/map/trees.bmp` が存在していなかった
- `world_normal.bmp` が vanilla と異なり 32bit BMP だった
- `terrain.bmp` が vanilla と異なり Windows 98/2000 BMP header だった

実施済み map 変更:

- `bakasekai/map/trees.bmp`
  - 新規追加
  - 5120 x 2560 x 8bit BMP
- `bakasekai/map/world_normal.bmp`
  - 32bit BMP から 24bit BMP3 に変換
  - 元ファイル退避:
    - `/tmp/hoi4_profile_map_cache_20260604_1/world_normal.bmp.backup_32bit`
- `bakasekai/map/terrain.bmp`
  - DIB header 124 byte から BMP3 40 byte に正規化
  - 元ファイル退避:
    - `/tmp/hoi4_profile_map_cache_20260604_1/terrain.bmp.backup_v5`
- `bakasekai/map/rivers.bmp`
  - 以前、BMP header の `biClrUsed` / `biClrImportant` を正規化

最新の map file 状態:

```text
terrain.bmp      Windows 3.x BMP, 5120 x 2560 x 8
trees.bmp        Windows 3.x BMP, 5120 x 2560 x 8
world_normal.bmp Windows 3.x BMP, 2560 x 1280 x 24
rivers.bmp       Windows 3.x BMP, 5120 x 2560 x 8
```

重要な注意:

- この map 形式修正後、ユーザー報告では「一回も起動できない」
- したがって `trees.bmp` 追加、`world_normal.bmp` 変換、`terrain.bmp` 正規化のいずれかが悪化要因になった可能性がある
- 特に `trees.bmp` を全黒で生成したこと、または `terrain.bmp` の 255 色 palette 処理が HOI4 側の期待とずれている可能性がある

## GUI 仮説

ユーザーは GUI 系を疑っていた。

実施済み:

- 一度、古い full replace GUI を外した
- その後、SSW / EoaNB / vanilla 1.18.2 に寄せて復帰
- 対象:
  - `bakasekai/interface/replace/frontendmainview.gui`
  - `bakasekai/interface/replace/frontendgamesetupview.gui`
  - `bakasekai/interface/replace/core.gui`
  - `bakasekai/interface/replace/subscription_message_view.gui`
  - `bakasekai/interface/replace/_bsm_load_screen_font.gfx`

主な変更:

- `_bsm_load_screen_font.gfx`
  - `loadscreen_tips` を `loadscreen_tip` に修正
- `core.gui`
  - vanilla ベースへ寄せた
  - `right_cabinet_vertical_slider` を復旧
- `frontendmainview.gui`
  - `career_profile_button` 周辺を復旧
  - `sp_tutorial_button` を EoaNB 方式に寄せた

評価:

- GUI 修正後も停止位置は大きく変わらなかった
- GUI 警告は残るが、現在の本命は GUI 単独ではない
- ただし frontend 初期化で止まるため、GUI を完全除外はできない

## medals / unit_medals / career profile 定義

実施済み:

- `bakasekai/common/medals/00_medals.txt`
  - 1.18.2 vanilla に近い定義へ更新
  - `experimental_science_mastery` など新しい career profile medals を追加
- `bakasekai/common/unit_medals/00_default.txt`
  - vanilla ベースに寄せた
  - MOD の ideology key に合わせて修正
    - `communism_ideology`
    - `democratic_ideology`
    - `fascism_ideology`
    - `neutrality_ideology`
- `bakasekai/common/scripted_triggers/unit_medals_scripted_triggers.txt`
  - retag に合わせた
    - `GER -> DEU`
    - `ENG -> GBR`
    - `JAP -> JPN`
    - `KOR` 復帰

評価:

- これらの修正後もクラッシュは継続
- medals 単体の可能性は下がった
- ただし `career_profile` と unit leader / medal 系はまだ関連候補

## character / leader 不整合

`history/countries` の `recruit_character` を検査した。

見つかった未定義参照:

- `JPN - Japan.txt`
  - `JAP_kanin_kotohito`
  - 実体は `JAP_Kanin_Kotohito`
- `WES - Western Sahara.txt`
  - `WES_El_Ouali_Mustapha_Sayed`
  - 実体は `WES_el_ouali_mustapha_sayed`

修正済み:

- `bakasekai/history/countries/JPN - Japan.txt`
- `bakasekai/history/countries/WES - Western Sahara.txt`

修正後:

- `history/countries` 全体の未定義 `recruit_character` は 0 件

評価:

- `CUnitLeader::GetName()` っぽい経路の疑いがあったため修正した
- ただし修正後もクラッシュ継続
- 現時点では主因ではなさそう

## 外部生成物の退避履歴

最新の退避先:

```text
/tmp/hoi4_profile_map_cache_20260604_1/
```

中身:

```text
career_profile_9B21E73601001001_v3.pr
naval_dist.cache
naval_dist_checksum.cache
world_normal.bmp.backup_32bit
terrain.bmp.backup_v5
```

注意:

- 退避後にユーザーが再起動したため、Documents 側には新しい以下が再生成されている
  - `career_profile_9B21E73601001001_v3.pr`
  - `naval_dist.cache`
  - `naval_dist_checksum.cache`

## 現在の git status 上の関連変更

主な関連ファイル:

```text
M  bakasekai/common/medals/00_medals.txt
M  bakasekai/common/scripted_triggers/unit_medals_scripted_triggers.txt
M  bakasekai/common/unit_medals/00_default.txt
M  bakasekai/history/countries/JPN - Japan.txt
M  bakasekai/history/countries/WES - Western Sahara.txt
M  bakasekai/interface/replace/_bsm_load_screen_font.gfx
M  bakasekai/interface/replace/core.gui
M  bakasekai/interface/replace/frontendgamesetupview.gui
M  bakasekai/interface/replace/frontendmainview.gui
M  bakasekai/interface/replace/subscription_message_view.gui
M  bakasekai/map/rivers.bmp
M  bakasekai/map/rivers.bmp.backup
M  bakasekai/map/terrain.bmp
M  bakasekai/map/world_normal.bmp
?? bakasekai/map/trees.bmp
```

他にも既存作業由来と思われる変更がある:

```text
M  bakasekai/common/on_actions/_bsm_system.txt
M  bakasekai/common/scripted_effects/_bsm_anomaly_system.txt
M  bakasekai/common/scripted_effects/bsm_economic_alliance_gui_effects.txt
M  bakasekai/common/units/equipment/nsi_equipment.txt
M  bakasekai/map/definition.csv
D  bakasekai/map/strategicregions/245-kagawa.txt
M  bakasekai/map/strategicregions/246-ehime.txt
?? bakasekai/gfx/loadingscreens/*.dds
```

## 現時点の判断

優先度順:

1. map / naval_dist cache 系
2. career_profile と unit leader / medal 系
3. frontend GUI 系

理由:

- `naval_dist.cache` を消すと起動できるという報告が強い
- 停止位置が `InitMap` 後
- `default.map` と map asset の不整合が実際にあった
- sample は script error ではなく malloc heap corruption

ただし、最新の map 修正で「一回も起動できない」状態になったため、直近変更のうち map 画像変更は戻して再検証すべき。

## 次にやるべき切り分け

最優先:

1. `terrain.bmp` と `world_normal.bmp` を退避元へ戻す
   - `/tmp/hoi4_profile_map_cache_20260604_1/terrain.bmp.backup_v5`
   - `/tmp/hoi4_profile_map_cache_20260604_1/world_normal.bmp.backup_32bit`
2. `trees.bmp` を一旦外す、または vanilla の `trees.bmp` をサイズ変換して使う
3. `career_profile_*.pr` と `naval_dist*.cache` を削除/退避
4. 1回目起動できるか確認

その後:

- 起動できた場合:
  - `trees.bmp`
  - `world_normal.bmp`
  - `terrain.bmp`
  を1つずつ戻して、どれで壊れるか確認する
- 起動できない場合:
  - map画像以外の直近変更、特に GUI / medals / unit_medals を順に戻す
  - ただし unrelated な既存変更は触らない

## 未解決

- 2回目/3回目で落ちる根本原因はまだ確定していない
- 最新状態では一回も起動できないため、直近の map asset 修正が悪化要因になった可能性が高い
- `naval_dist.cache` 再生成が壊れる理由は未確定
- `career_profile` に `kaiserreich_career_profile` 文字列が残る理由は未確定

