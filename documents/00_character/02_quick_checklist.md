# キャラクター作成クイックチェックリスト

## 重要な注意事項

- **スパイの追加**には `create_operative_leader` を使用（キャラクターではない）
- **キャラクターシステム**はパッチ 1.11 で追加されたシステム
- 同じキャラクターを複数の役割（顧問、国家指導者、部隊指揮官）で使用可能
- スパイはキャラクターとは別扱い



## ファイル配置

- **キャラクター定義**: `/common/characters/*.txt`
- **キャラクター募集**: `/history/countries/TAG*.txt`
- **ファイル名**: 国家タグと同じ名前が一般的だが、必須ではない
- **汎用キャラクター**: `/history/general/*.txt` で `generate_character` エフェクトを使用

## 基本構造

キャラクターは `characters = { ... }` ブロック内で定義される。

```
characters = {
    my_character_1 = {
        # キャラクター1の定義
    }
    my_character_2 = {
        # キャラクター2の定義
    }
}
```
## キャラクター募集の重要ルール

- **必須**: すべてのキャラクターは `/history/countries/` で `recruit_character = my_character` で募集が必要
- **募集なしでは登場しない**: 募集されないキャラクターはゲームに登場しない
- **ファイルの最終行には置かない**: 募集コマンドの後に少なくとも1行必要

## クイックチェックリスト

### 1. キャラクター作成
- `/common/characters/*.txt` でキャラクターを定義
- `name = TAG_loc_key` - `/localisation/english/*_l_english.yml` で定義されたローカライゼーションキーを使用
- `portraits = { ... }` - `/interface/*.gfx` で定義された spriteType を使用

### 2. 画像ファイルの配置
- **国家/部隊指導者**: `/gfx/leaders/` に配置が一般的
- **顧問**: `/gfx/interface/ideas/` に配置が一般的
- **柔軟性**: スプライトの texturefile はモッド内の任意のフォルダを指定可能

### 3. 国家への割り当て
- `/history/countries/` で `recruit_character` を使用
- **注意**: ファイルの最終行には配置不可

### 4. 後から役割を追加する場合
ゲーム開始時に役割がないキャラクターには、後から以下のエフェクトで役割を追加:
- `add_country_leader_role` - 国家指導者役割
- `add_corps_commander_role` - 軍団指揮官役割
- `add_field_marshal_role` - 元帥役割
- `add_naval_commander_role` - 海軍指揮官役割
- `add_advisor_role` - 顧問役割（制限あり）

**顧問の代替手段**: `visible = { ... }` とフラグを使用した条件付き表示
