# Real BSM GUI Examples

This file contains actual working examples from the BSM/SSW mods for reference.

## Table of Contents
- [Topbar Resource Display](#topbar-resource-display)
- [Toggle Window](#toggle-window)
- [Dynamic List with Log Entries](#dynamic-list-with-log-entries)
- [Country Selection GUI](#country-selection-gui)

## Topbar Resource Display

Example from `bsm_topbar` showing resource displays in the top bar.

### Scripted GUI
```
scripted_gui = {
    bsm_topbar = {
        window_name = "bsm_topbar"
        context_type = player_context

        effects = {
            bsm_OE_GUI_open_button_click = {
                if = {
                    limit = { has_variable = OE_page }
                    clear_variable = OE_page
                }
                else = {
                    set_variable = { OE_page = 1 }
                }
            }

            anomaries_button_click = {
                if = {
                    limit = { has_variable = bsm_anomaly_tab }
                    clear_variable = bsm_anomaly_tab
                }
                else = {
                    set_variable = { bsm_anomaly_tab = 1 }
                }
            }
        }
    }
}
```

### GUI File (Snippet)
```
guiTypes = {
    containerWindowType = {
        name = "bsm_topbar"
        position = { x=0 y=0 }
        size = { width=100%% height=100%% }

        # Resource display container
        containerWindowType = {
            name = "popular_opinion"
            position = { x= 705 y = 8}
            size = { width=56 height=30 }
            orientation = UPPER_LEFT

            background = {
                position = { x = 2 y = 1 }
                name = "po_bg"
                quadTextureSprite ="GFX_bg_mini_tooltip"
                pdx_tooltip = "popular_opinion_title"
                pdx_tooltip_delayed = "popular_opinion_desc"
            }

            iconType = {
                name ="po"
                spriteType = "GFX_text_resource_unity"
                position = { x= 4 y = 2 }
                orientation = "UPPER_LEFT"
                alwaystransparent = yes
                pdx_tooltip = "popular_opinion_title"
                pdx_tooltip_delayed = "popular_opinion_desc"
            }

            instantTextBoxType = {
                name ="COUNTRY_PO"
                position = { x= 19 y = 5 }
                font = "vanilla_hoi_18mbs"
                text = "COUNTRY_PO"
                format = left
                maxWidth = 50
                maxHeight = 24
                fixedsize = yes
                alwaystransparent = yes
                pdx_tooltip = "popular_opinion_title"
                pdx_tooltip_delayed = "popular_opinion_desc"
            }
        }

        # Energy currency display
        containerWindowType = {
            name = "Energie_currencies"
            position = { x= 850 y = 8}
            size = { width=56 height=30 }
            orientation = UPPER_LEFT

            background = {
                position = { x = 2 y = 1 }
                name = "cd_bg"
                quadTextureSprite ="GFX_bg_mini_tooltip"
                pdx_tooltip = "Unified_Currency_title_txt"
                pdx_tooltip_delayed = "Unified_Currency_desc_2"
            }

            iconType = {
                name ="ec"
                spriteType = "GFX_resource_energy_large"
                position = { x= -2 y = -4 }
                orientation = "UPPER_LEFT"
                alwaystransparent = yes
                pdx_tooltip = "Unified_Currency_title_txt"
                pdx_tooltip_delayed = "Unified_Currency_desc_2"
                scale = 0.8
            }

            instantTextBoxType = {
                name ="COUNTRY_ec"
                position = { x= 19 y = 5 }
                font = "vanilla_hoi_18mbs"
                text = Unified_Currency
                format = left
                maxWidth = 50
                maxHeight = 24
                fixedsize = yes
                alwaystransparent = yes
                pdx_tooltip = "Unified_Currency_title_txt"
                pdx_tooltip_delayed = "Unified_Currency_desc_2"
            }
        }

        # Toggle button for opening event GUI
        containerWindowType = {
            name = "bsm_OE_GUI_open"
            position = { x= -400 y = 4}
            size = { width=40 height=40 }
            orientation = UPPER_RIGHT

            buttonType = {
                name = "bsm_OE_GUI_open_button"
                position = { x = 0 y = 0 }
                quadTextureSprite ="GFX_bsm_icon"
                orientation = "UPPER_right"
                clicksound = click_close
                oversound = ui_menu_over
                scale = 1
            }
        }
    }
}
```

**Key Patterns:**
- Resource displays use background + icon + text combination
- All three elements share same tooltips for consistency
- `alwaystransparent = yes` on icon and text allows clicks to pass through to background
- Negative x positioning with `UPPER_RIGHT` orientation for right-aligned elements

## Toggle Window

Example from `ssw_economic_sphere_gui` showing selection and toggle pattern.

### Scripted GUI
```
scripted_gui = {
    ssw_economic_sphere_gui = {
        context_type = selected_country_context
        parent_window_token = selected_country_view_diplomacy
        window_name = "economic_sphere_button_container"

        ai_enabled = { always = no }
        visible = { always = yes }

        triggers = {
            economic_sphere_open_button_visible = {
                FROM = { has_variable = es_economic_sphere }
            }
        }

        effects = {
            economic_sphere_open_button_click = {
                if = {
                    limit = {
                        check_variable = { ROOT.selected_policy_button_diplomancy = 2 }
                        check_variable = { FROM.es_economic_sphere = ROOT.ptsd_select_economic_sphere }
                    }
                    clear_variable = ROOT.selected_policy_button_diplomancy
                }
                else = {
                    set_variable = { ROOT.selected_policy_button_diplomancy = 2 }
                    set_temp_variable = { sphere_token = FROM.es_economic_sphere }
                    es_select_ptsd_sphere_btn = yes
                    if = {
                        limit = { NOT = { has_country_flag = ptsd_already_opened } }
                        set_global_flag = ptsd_already_opened
                    }
                }
            }
        }

        properties = {
            economic_sphere_open_button = {
                image = "GFX_[?FROM.es_economic_sphere.GetTokenKey]"
            }
        }
    }
}
```

**Key Patterns:**
- Toggle logic: check if already selected with same value, clear if yes, set if no
- Dynamic image using properties: `image = "GFX_[?variable.GetTokenKey]"`
- Global flag to track first-time opening
- Temp variable for immediate processing

## Dynamic List with Log Entries

Example from `bsm_mine_GUI` showing dynamic list for displaying logs.

### Scripted GUI
```
scripted_gui = {
    bsm_mine_GUI = {
        window_name = bsm_mine_GUI
        context_type = decision_category

        visible = { }
        effects = { }
        triggers = { }
        properties = { }

        dynamic_lists = {
            mine_log_gridbox = {
                array = bsm_mine_log_id
                change_scope = no
                entry_container = "bsm_mine_log_container"
                value = log_id
                index = log_index
            }
        }
    }
}
```

### GUI File
```
guiTypes = {
    containerWindowType = {
        name = "bsm_mine_GUI"
        size = { width = 500 height = 218 }

        containerWindowType = {
            name = "bsm_mine_GUI"
            size = { width = 516 height = 250 }
            position = { x = -8 y = -27 }

            background = {
                name = "Background"
                spriteType ="GFX_bsm_mineview_bg"
            }

            # Static info displays
            instantTextboxType = {
                name = "MD_mine_size_title"
                position = { x = 43 y = 30 }
                font = "bsm_16_black"
                text = "MD_mine_size_title"
                maxWidth = 110
                maxHeight = 23
                format = centre
                fixedsize = yes
                pdx_tooltip = MD_mine_size_tooltip
                pdx_tooltip_delayed = MD_mine_size_tooltip_delay
            }

            instantTextboxType = {
                name = "MD_mine_size"
                position = { x = 43 y = 56 }
                font = "bsm_16_black"
                text = "MD_mine_size"
                maxWidth = 110
                maxHeight = 23
                format = centre
                fixedsize = yes
                pdx_tooltip = MD_mine_size_tooltip
                pdx_tooltip_delayed = MD_mine_size_tooltip_delay
            }

            # Log section with scrollbar
            containerWindowType = {
                name = "bsm_mine_log"
                size = { width = 310 height = 210 }
                position = { x = 203 y = 35 }

                background = {
                    name = "Background"
                    spriteType ="GFX_tiled_empty"
                }

                verticalScrollbar = "win95_right_vertical_slider"
                margin = {top=0 left=0 bottom=0 right= 0}

                gridboxtype = {
                    name = "mine_log_gridbox"
                    position = { x=10 y=0 }
                    size = { width = 100%% height = 10%% }
                    slotsize = { width=285 height= 50 }
                    max_slots_horizontal = 1
                    add_horizontal = no
                }
            }
        }
    }

    # Log entry template (dynamically instantiated)
    containerWindowType = {
        name = "bsm_mine_log_container"
        size = { width = 100%% height = 100%% }
        position = { x = 0 y = 0 }

        background = {
            name = "Background"
            spriteType ="GFX_bsm_btm_bar"
        }

        instantTextboxType = {
            name = "MD_log_name"
            position = { x = 3 y = 8 }
            font = "bsm_16_black"
            text = "MD_log_name"
            maxWidth = 260
            maxHeight = 40
            format = left
            fixedsize = yes
            pdx_tooltip = MD_log_name_tooptip
        }
    }
}
```

**Key Patterns:**
- Split container (left side: static info, right side: dynamic log list)
- Scrollable grid using `gridboxtype` with `verticalScrollbar`
- Separate container definition for log entry template
- Entry template defined outside main container at root level
- `slotsize` determines height of each entry
- `max_slots_horizontal = 1` for vertical list

## Country Selection GUI

Example from `ssw_GER_reichstag_GUI` showing dynamic lists with properties.

### Scripted GUI
```
scripted_gui = {
    ssw_GER_reichstag_GUI = {
        context_type = decision_category
        window_name = "ssw_GER_reichstag_GUI"

        visible = {
            tag = GER
        }

        effects = {
            grg_debug_btn_1_click = {
                grg_set_reichstag = yes
            }
        }

        triggers = {
            grg_debug_btn_1_visible = {
                is_debug = yes
            }
        }

        properties = {
            iss_half_piechart_item = {
                frame = gps_faction_color_list^v
            }

            grs_party_icon = {
                image = "[?gps_faction_icon_list^v.GetTokenKey]"
            }
        }

        dynamic_lists = {
            grg_half_piechart_gridbox = {
                array = grg_reichstag_array
                change_scope = no
                entry_container = "iss_half_piechart_entry_[?i]"
            }

            grg_ruling_parties_list = {
                array = gps_ruling_party_list
                change_scope = no
                entry_container = "grg_party_container"
            }

            grg_non_ruling_parties_list = {
                array = gps_non_ruling_party_list
                change_scope = no
                entry_container = "grg_party_container"
            }
        }
    }
}
```

**Key Patterns:**
- Multiple dynamic lists in one GUI
- Dynamic entry container name using index: `entry_container = "iss_half_piechart_entry_[?i]"`
- Array value access in properties: `frame = array_name^v`
- Shared entry container for multiple lists (`grg_party_container`)
- Debug-only buttons using `is_debug` trigger
- Tag-specific GUI visibility
