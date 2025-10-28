# 4. Full Example
# HOI4 キャラクター定義サンプル

## common/characters/*.txt

```plaintext
characters = {
    UKR_nestor_makhno = {
        name = UKR_nestor_makhno
        portraits = {
            civilian = {
                large = "GFX_portrait_UKR_nestor_makhno"
            }
        }
        country_leader = {
            ideology = anarchist_communism
            traits = { agrarian_activist }
            desc = UKR_nestor_makhno_desc
        }
    }

    SOV_georgy_zhukov = {
        name = SOV_georgy_zhukov
        portraits = {
            army = {
                small = "GFX_idea_georgy_zhukov"
                large = "GFX_portrait_SOV_georgy_zhukov"
            }
        }
        corps_commander = {
            traits = {
                media_personality
                armor_officer
                war_hero
                winter_specialist
            }
            skill = 5
            attack_skill = 5
            defense_skill = 2
            planning_skill = 4
            logistics_skill = 5
            legacy_id = 410
            visible = {
                NOT = { has_character_flag = SOV_exiled_flag }
            }
        }
        advisor = {
            slot = theorist
            idea_token = georgy_zhukov
            ledger = army
            allowed = { original_tag = SOV }  # 任意（実質効果なし）
            available = {
                has_completed_focus = SOV_positive_heroism
            }
            traits = { mass_assault_expert }
        }
    }
}
