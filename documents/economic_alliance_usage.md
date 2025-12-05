# 経済同盟システム使用方法

このドキュメントでは、経済同盟（Economic Alliance）システムのスクリプト使用方法について説明します。

## 概要

経済同盟は、軍事同盟（陣営）とは独立した経済的な協力関係を表すシステムです。
国は複数の経済同盟に加盟することが可能です。

## 定義済み経済同盟

以下のIDが定義されています：

*   **1**: EU (欧州連合)
*   **2**: Allies (連合国経済同盟)
*   **3**: GEACPS (大東亜共栄圏)

## スクリプト効果の使用方法

引数（`ALLIANCE = EU`など）は使用せず、事前に変数 `temp_alliance_id` を設定してから効果を呼び出します。

### 1. 経済同盟への加盟 / 追加

対象の国スコープで以下のスクリプトを実行します。

```txt
# 例: EU (ID: 1) に加盟させる場合
set_temp_variable = { temp_alliance_id = 1 }
add_to_economic_alliance = yes

# 例: Allies (ID: 2) に加盟させる場合
set_temp_variable = { temp_alliance_id = 2 }
add_to_economic_alliance = yes
```

この効果は以下の処理を自動的に行います：
*   対象の同盟がアクティブでない場合、アクティブ化フラグを立てる。
*   グローバルなメンバー配列 (`global.economic_alliance_EU_members` 等) に国を追加する。
*   国フラグ (`in_economic_alliance_EU` 等) を設定する。
*   経済同盟カウント (`economic_alliance_count`) を増加させる。
*   重複加盟チェック（すでに加盟している場合は二重に追加されない）。

### 2. 経済同盟からの脱退 / 削除

対象の国スコープで以下のスクリプトを実行します。

```txt
# 例: GEACPS (ID: 3) から脱退させる場合
set_temp_variable = { temp_alliance_id = 3 }
remove_from_economic_alliance = yes
```

この効果は以下の処理を行います：
*   グローバルなメンバー配列から国を削除する。
*   国フラグを削除する。
*   経済同盟カウントを減少させる。

### 3. 汎用経済同盟 (Generic Economic Alliance)

定義済みの同盟以外に、ディシジョンを通じて動的に形成される汎用的な経済同盟もあります。

*   **結成**: ディシジョン `bsm_form_economic_alliance` を使用。
*   **加盟**: ディシジョン `bsm_join_economic_alliance` を使用。

これらはスクリプト効果 `bsm_form_economic_alliance_effect` および `bsm_join_economic_alliance_effect` によって処理され、リーダーとメンバーの関係が構築されます。
汎用同盟の場合、IDによる管理ではなく、リーダー国とメンバー国の直接的なリンク（配列 `economic_alliance_joined_leaders` 等）によって管理されます。

## 経済力の統合計算

統一通貨システム (`_bsm_Unified_Currency.txt`) 内で、加盟している経済同盟の総経済力を計算し、ボーナスを付与する処理が行われています。
これも `temp_alliance_id` を使用して各同盟の計算を行っています。

```txt
# 例: EUの経済力を計算
set_temp_variable = { temp_alliance_id = 1 }
ucs_accumulate_alliance_power = yes
```
