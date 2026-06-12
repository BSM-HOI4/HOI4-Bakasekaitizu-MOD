# ai_areas / ai_faction_theaters リファレンス

地理的な兵力・生産の配分を制御する2つのシステム。

## ai_areas

配置: `common/ai_areas/default.txt`

strategic_region をまとめた「エリア」を定義する。エリア名は `ai_strategy` の `area_priority` 等から参照される。

```
areas = {
  scandinavia = {
    strategic_regions = {
      11   # Norway
      191  # Northern Norway
      10   # Southern Sweden
    }
  }
  north_africa = {
    strategic_regions = {
      128  # Egypt
    }
  }
}
```

- 1つの strategic_region を複数エリアに入れてよい(mod内でもsuezとnorth_africaが128を共有)
- エリア追加後は `ai_strategy` 側から使って初めて意味を持つ:

```
ai_strategy = {
  type = area_priority
  id = north_africa
  value = 50
}
```

- strategic_region IDは `bakasekai/map/strategicregions/` を確認。**BSMは独自マップなのでvanillaのID表は使えない**

## ai_faction_theaters

配置: `common/ai_faction_theaters/ai_faction_theaters.txt`

陣営単位の「戦域」を定義し、陣営AIが戦域ごとに戦力を融通する仕組み。
**一次資料**: `bakasekai/common/ai_faction_theaters/_documentation.md` を必ず読む。

```
western_europe = {
  name = theater_western_europe      # locキー
  regions = {                        # strategic_region IDのリスト
    19   # Northern France
    5    # Benelux
  }
  cancel = {                         # 戦域を解散する条件
    OR = {
      AND = {
        original_tag = DEU
        has_war_with = SOV
      }
    }
  }
}
```

- mod内の定義は現在ほぼコメントアウトされている(vanillaマップ前提のIDのため)。**BSMマップ用に有効化する場合はIDを全て張り替える必要がある**
- `cancel` で「この戦域はもう重要でない」条件を書く(例: 史実ドイツは独ソ戦開始で西部戦線の優先を解除)

## 関連: 戦線・守備隊の配分(ai_strategy側)

エリア・戦域と組み合わせて使う代表的な ai_strategy タイプ:

- `front_unit_request_factor` — 戦線への増援要求の倍率
- `theatre_distribution_demand_increase` — 特定戦域への配分増
- `garrison` — 守備隊方針
- `put_unit_buffers` — 予備兵力のプール(vanilla `default.txt` に実例)

これらは型ごとに id/value の意味が異なるため、使用前にvanilla `common/ai_strategy/default.txt` の用例を確認すること。

## mod内実例

- `bakasekai/common/ai_areas/default.txt`
- `bakasekai/common/ai_faction_theaters/_documentation.md` + `ai_faction_theaters.txt`
- `bakasekai/map/strategicregions/` — BSM独自のstrategic_region定義
