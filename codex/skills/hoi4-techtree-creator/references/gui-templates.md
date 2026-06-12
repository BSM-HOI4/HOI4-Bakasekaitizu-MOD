# GUI テンプレート集

> **重要:** キャンバスサイズ・ピクセル間隔はmod・ツリー種類ごとに異なる。
> 必ず参照フォルダ（ユーザーが指定したもの）を Read して実測値を確認してから使用すること。
> 以下の数値はあくまでデフォルト例（engnavalfolder 実測値ベース）。

各テンプレートの `[FOLDERNAME]` / `[TAG]` / `[TITLE_KEY]` を実際の値に置換して使用する。

---

## [VERTICAL_FOLDER] 縦型フォルダ本体

`countrytechtreeview.gui` の `countrytechtreeview` containerWindowType の中（他フォルダの直後）に追記。

`[CANVAS_W]` = カテゴリ数 × 280 + 余白 (例: 6カテゴリ → 3300)
`[CANVAS_H]` = 年代スパン × 140 + 余白 (例: 1925-1975 → 2800)
年ラベルのy座標 = (年変数値) × 70 (例: @1925=0→y=0, @1930=2→y=140, @1935=4→y=280...)
カテゴリヘッダーのx座標 = 120 + (カテゴリy変数値) × 70 (例: @CAT_A=0→x=120, @CAT_B=4→x=400...)

```gui
		containerWindowType = {
			name = "[FOLDERNAME]"
			position = { x=0 y=47 }
			size = { width = 100%% height = 100%% }
			margin = { top = 13 left = 13 bottom = 24 right = 25}
			drag_scroll = { left middle }
			verticalScrollbar = "right_vertical_slider"
			horizontalScrollbar = "bottom_horizontal_slider"

			background = {
				name = "Background"
				quadTextureSprite = "GFX_tiled_window_2b_border"
			}

			containerWindowType = {
				name = "[TAG]_[FOLDERNAME]_techtree_stripes"
				position = { x= 0 y= 0 }
				size = {
					width = [CANVAS_W] height = [CANVAS_H]
					min = { width = 100%% height = 100%% }
				}
				clipping = no

				background = {
					name = "Background"
					quadTextureSprite = "GFX_techtree_stripes"
				}

				iconType = {
					name = "[TAG]_[FOLDERNAME]_techtree_bg"
					spriteType = "GFX_naval_techtree_bg"
					position = { x=0 y=0 }
					alwaystransparent = yes
				}

				instantTextBoxType = {
					name = "[TAG]_[FOLDERNAME]_title"
					position = { x = 100 y = 20 }
					textureFile = ""
					font = "hoi_36header"
					borderSize = { x = 0 y = 0}
					text = "[TITLE_KEY]"
					maxWidth = 600
					maxHeight = 62
					format = left
					Orientation = "UPPER_LEFT"
				}

				# 左側年ラベル列
				containerWindowType = {
					name = "[TAG]_[FOLDERNAME]_year_left"
					position = { x=10 y=120 }
					size = { width = 80 height = 100% }
					orientation = upper_left

					# 年ラベルを繰り返す（y = 年x変数値 × 70）
					instantTextBoxType = {
						name = "[TAG]_year_1930"
						position = { x = 40 y = 0 }
						textureFile = ""
						font = "hoi_24"
						borderSize = {x = 0 y = 4}
						text = "1930"
						maxWidth = 80
						maxHeight = 32
						format = center
						Orientation = "UPPER_CENTER"
					}
					instantTextBoxType = {
						name = "[TAG]_year_1935"
						position = { x = 40 y = 140 }
						textureFile = ""
						font = "hoi_24"
						borderSize = {x = 0 y = 4}
						text = "1935"
						maxWidth = 80
						maxHeight = 32
						format = center
						Orientation = "UPPER_CENTER"
					}
					instantTextBoxType = {
						name = "[TAG]_year_1940"
						position = { x = 40 y = 280 }
						textureFile = ""
						font = "hoi_24"
						borderSize = {x = 0 y = 4}
						text = "1940"
						maxWidth = 80
						maxHeight = 32
						format = center
						Orientation = "UPPER_CENTER"
					}
					instantTextBoxType = {
						name = "[TAG]_year_1945"
						position = { x = 40 y = 420 }
						textureFile = ""
						font = "hoi_24"
						borderSize = {x = 0 y = 4}
						text = "1945"
						maxWidth = 80
						maxHeight = 32
						format = center
						Orientation = "UPPER_CENTER"
					}
					# 必要に応じて年ラベルを追加...
				}

				# カテゴリヘッダー（x = 120 + カテゴリy変数値 × 70）
				containerWindowType = {
					name = "[TAG]_[FOLDERNAME]_cat_a"
					position = { x = 120 y = 60 }
					size = { width = 300 height = 100%% }

					instantTextBoxType = {
						name = "[TAG]_cat_a_label"
						position = { x = 75 y = 0 }
						textureFile = ""
						font = "hoi_30header"
						borderSize = { x = 0 y = 0}
						text = "[CAT_A_LABEL_KEY]"
						maxWidth = 250
						maxHeight = 32
						format = left
						Orientation = "UPPER_LEFT"
					}
				}
				# カテゴリBヘッダー（x = 120 + @CAT_B×70）
				containerWindowType = {
					name = "[TAG]_[FOLDERNAME]_cat_b"
					position = { x = 400 y = 60 }
					size = { width = 300 height = 100%% }

					instantTextBoxType = {
						name = "[TAG]_cat_b_label"
						position = { x = 75 y = 0 }
						textureFile = ""
						font = "hoi_30header"
						borderSize = { x = 0 y = 0}
						text = "[CAT_B_LABEL_KEY]"
						maxWidth = 250
						maxHeight = 32
						format = left
						Orientation = "UPPER_LEFT"
					}
				}
				# 必要に応じてカテゴリを追加...

			}
		}
```

---

## [HORIZONTAL_FOLDER] 横型フォルダ本体

年ラベルが上部に横並び。vanilla naval_folder スタイル。

`[CANVAS_W]` = 年代スパン × ~350 (例: 7年代 → 2700)
`[CANVAS_H]` = カテゴリ数 × ~200 + 余白 (例: 5カテゴリ → 1200)

```gui
		containerWindowType = {
			name = "[FOLDERNAME]"
			position = { x=0 y=47 }
			size = { width = 100%% height = 100%% }
			margin = { top = 13 left = 13 bottom = 24 right = 25}
			drag_scroll = { left middle }
			verticalScrollbar = "right_vertical_slider"
			horizontalScrollbar = "bottom_horizontal_slider"

			background = {
				name = "Background"
				quadTextureSprite ="GFX_tiled_window_2b_border"
			}

			containerWindowType = {
				name = "size_filler"
				position = { x=0 y=0 }
				size = { width = [CANVAS_W] height = [CANVAS_H] }
			}

			iconType = {
				name ="[TAG]_[FOLDERNAME]_techtree_bg"
				spriteType = "GFX_naval_techtree_bg"
				position = { x=0 y=0 }
			}

			# 上部年ラベル（x = 300 + ステップ×350、y = 20固定）
			instantTextBoxType = {
				name = "[TAG]_year1"
				position = { x = 300 y = 20 }
				textureFile = ""
				font = "hoi_36header"
				borderSize = {x = 0 y = 4}
				text = "1936"
				maxWidth = 170
				maxHeight = 32
				format = left
				Orientation = "UPPER_LEFT"
			}
			instantTextBoxType = {
				name = "[TAG]_year2"
				position = { x = 650 y = 20 }
				textureFile = ""
				font = "hoi_36header"
				borderSize = {x = 0 y = 4}
				text = "1939"
				maxWidth = 170
				maxHeight = 32
				format = left
				Orientation = "UPPER_LEFT"
			}
			# 必要に応じて年ラベルを追加...
		}
```

---

## [ITEM_DEFS] アイテム定義テンプレート

ファイル末尾付近（既存 item/small_item 定義の後）に追記。
`[FOLDERNAME]` を実際のフォルダ名に置換。

### small_item（72×72 小アイコン）

```gui
	containerWindowType = {
		name = "techtree_[FOLDERNAME]_small_item"
		position = { x=0 y=0 }
		size = { width = 72 height = 72 }
		clipping = no

		background = {
			name = "Background"
			quadTextureSprite ="GFX_technology_unavailable_item_bg"
		}
		gridboxtype = {
			name = "special_project_specialization_list"
		}
		iconType = {
			name = "Icon"
			position = { x=3 y=3 }
			spriteType = "GFX_technology_medium"
			alwaystransparent = yes
		}
		iconType = {
			name = "bonus_icon"
			position = { x=3 y=-22 }
			spriteType = "GFX_tech_bonus"
		}
		instantTextBoxType = {
			name = "bonus"
			position = { x = 17 y = -22 }
			textureFile = ""
			font = "hoi_16mbs"
			borderSize = {x = 4 y = 4}
			text = ""
			maxWidth = 50
			maxHeight = 20
			format = right
		}
		iconType = {
			name = "can_assign_design_team_icon"
			position = { x=0 y=42 }
			spriteType = "GFX_design_team_icon"
		}
	}
```

### item（フル表示）

縦型ツリー用（テック名を上部テキストで表示、アイコンは中央）:

```gui
	containerWindowType = {
		name = "techtree_[FOLDERNAME]_item"
		position = { x=-60 y=0 }
		size = { width = 320 height = c }
		clipping = no

		background = {
			name = "Background"
			quadTextureSprite ="GFX_technology_engnavalsupportfolder_small_unavailable_item_bg"
		}
		gridboxtype = {
			name = "special_project_specialization_list"
		}
		instantTextBoxType = {
			name = "Name"
			position = { x = 3 y = -1 }
			textureFile = ""
			font = "ssw_harenosora_20"
			borderSize = {x = 4 y = 4}
			text = ""
			maxWidth = 320
			maxHeight = 20
			fixedsize = yes
			format = left
		}
		iconType = {
			name = "Icon"
			position = { x=167 y=34 }
			spriteType = "GFX_technology_medium"
			centerposition = yes
			alwaystransparent = yes
		}
		iconType = {
			name = "bonus_icon"
			position = { x=111 y=-22 }
			spriteType = "GFX_tech_bonus"
		}
		instantTextBoxType = {
			name = "bonus"
			position = { x = 111 y = -22 }
			textureFile = ""
			font = "hoi_16mbs"
			borderSize = {x = 4 y = 4}
			text = ""
			maxWidth = 80
			maxHeight = 20
			format = center
		}
		containerWindowType = {
			name = "sub_technology_slot_0"
			position = { x=285 y=5 }
			size = { width = 35 height = 26 }
			clipping = no
			background = {
				name = "Background"
				spriteType ="GFX_subtechnology_unavailable_item_bg"
			}
			iconType = {
				name = "picture"
				position = { x=2 y=2 }
				spriteType = "GFX_subtech_heavy_battleship"
				alwaystransparent = yes
			}
		}
		containerWindowType = {
			name = "sub_technology_slot_1"
			position = { x=285 y=31 }
			size = { width = 35 height = 26 }
			clipping = no
			background = {
				name = "Background"
				spriteType ="GFX_subtechnology_unavailable_item_bg"
			}
			iconType = {
				name = "picture"
				position = { x=2 y=2 }
				spriteType = "GFX_subtech_heavy_battleship"
				alwaystransparent = yes
			}
		}
		iconType = {
			name = "can_assign_design_team_icon"
			position = { x=0 y=42 }
			spriteType = "GFX_design_team_icon"
		}
	}
```

横型ツリー用（右側テキスト + 左アイコン、naval_folder_item スタイル）:

```gui
	containerWindowType = {
		name = "techtree_[FOLDERNAME]_item"
		position = { x=-131 y=1 }
		size = { width = 204 height = 72 }
		clipping = no

		background = {
			name = "Background"
			quadTextureSprite ="GFX_technology_unavailable_item_bg"
		}
		gridboxtype = {
			name = "special_project_specialization_list"
		}
		iconType = {
			name = "Icon"
			position = { x=167 y=34 }
			spriteType = "GFX_technology_medium"
			centerposition = yes
			alwaystransparent = yes
		}
		instantTextBoxType = {
			name = "Name"
			position = { x = 3 y = -1 }
			textureFile = ""
			font = "ssw_harenosora_20"
			borderSize = {x = 4 y = 4}
			text = ""
			maxWidth = 290
			maxHeight = 20
			fixedsize = yes
			format = left
		}
		iconType = {
			name = "bonus_icon"
			position = { x=257 y=-18 }
			spriteType = "GFX_tech_bonus"
		}
		instantTextBoxType = {
			name = "bonus"
			position = { x = 257 y = -19 }
			textureFile = ""
			font = "hoi_16mbs"
			borderSize = {x = 4 y = 4}
			text = ""
			maxWidth = 80
			maxHeight = 20
			format = center
		}
		containerWindowType = {
			name = "sub_technology_slot_0"
			position = { x=285 y=5 }
			size = { width = 35 height = 26 }
			clipping = no
			background = {
				name = "Background"
				spriteType ="GFX_subtechnology_unavailable_item_bg"
			}
			iconType = {
				name = "picture"
				position = { x=2 y=2 }
				spriteType = "GFX_subtech_heavy_battleship"
				alwaystransparent = yes
			}
		}
		iconType = {
			name = "can_assign_design_team_icon"
			position = { x=0 y=42 }
			spriteType = "GFX_design_team_icon"
		}
	}
```
