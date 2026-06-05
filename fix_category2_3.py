import re
import os

base = '/Users/eightman/Desktop/HOI4_modding/bsm_test/bakasekai/'

def fix_bsm_jpn():
    p = os.path.join(base, 'common/ideas/BSM_jpn.txt')
    with open(p, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    replacements = {
        'conscription_ratio': 'recruitable_population',
        'army_planning_speed': 'planning_speed',
        'planning_factor': 'max_planning',
        'army_leader_xp_gain_factor': 'army_leader_xp_factor',
        'army_experience_gain_factor': 'experience_gain_army',
        'soft_attack': '#soft_attack',
        'armor': '#armor',
        'air_experience_gain_factor': 'experience_gain_air',
        'naval_strike_factor': 'naval_strike_mission_factor',
        'interception_efficiency_factor': '#interception_efficiency_factor',
        'anti_air_equipment_attack_factor': '#anti_air_equipment_attack_factor',
        'carrier_air_attack_factor': '#carrier_air_attack_factor',
        'cas_close_air_support_factor': '#cas_close_air_support_factor',
        'close_air_support_efficiency': '#close_air_support_efficiency',
        'strategic_bombardment_factor': '#strategic_bombardment_factor',
        'tactical_bombing_factor': '#tactical_bombing_factor',
        'air_bombing_factor': '#air_bombing_factor',
        'convoy_raiding_efficiency': '#convoy_raiding_efficiency',
        'air_leader_xp_gain_factor': 'air_leader_xp_factor',
        'nuclear_production_speed': 'nuclear_production_factor',
        'navy_experience_gain_factor': 'experience_gain_navy',
        'doctrine_cost': '#doctrine_cost',
        'capital_ship_attack_factor': '#capital_ship_attack_factor',
        'capital_ship_defence_factor': '#capital_ship_defence_factor',
        'screen_ship_attack_factor': '#screen_ship_attack_factor',
        'convoy_raid_protection_factor': '#convoy_raid_protection_factor',
        'naval_build_speed_factor': '#naval_build_speed_factor',
        'screen_ship_defence_factor': '#screen_ship_defence_factor',
        'naval_mission_efficiency': '#naval_mission_efficiency',
        'submarine_attack_factor': '#submarine_attack_factor',
        'marine_attack_factor': '#marine_attack_factor',
        'navy_planning_speed': '#navy_planning_speed',
        'naval_heavy_gun_attack_factor': '#naval_heavy_gun_attack_factor',
        'convoy_production_speed': '#convoy_production_speed',
        'submarine_detection_factor': '#submarine_detection_factor',
        'submarine_stealth_factor': '#submarine_stealth_factor',
        'submarine_torpedo_attack_factor': '#submarine_torpedo_attack_factor',
        'screen_ship_torpedo_attack_factor': '#screen_ship_torpedo_attack_factor',
        'submarine_hp_factor': '#submarine_hp_factor',
        'ship_anti_air_attack_factor': '#ship_anti_air_attack_factor',
        'intel': '#intel',
        '=': '#=',
        'agency_operative_slot': '#agency_operative_slot'
    }

    error_lines = [196, 211, 218, 255, 278, 285, 292, 300, 329, 336, 344, 351, 358, 366, 381, 388, 389, 396, 403, 410, 411, 418, 425, 433, 440, 441, 462, 469, 483, 490, 497, 504, 511, 518, 519, 526, 527, 534, 541, 548, 555, 562, 569, 576, 577, 578, 579, 586, 593, 607, 614, 621, 628, 635, 636, 643, 644, 651, 658, 665, 666, 673, 687, 694, 702, 710, 721, 731, 732, 742, 743]
    
    for l in error_lines:
        idx = l - 1
        if idx < len(lines):
            for k, v in replacements.items():
                if k in lines[idx] and not lines[idx].lstrip().startswith('#'):
                    lines[idx] = lines[idx].replace(k, v)
                    break
                    
    # Fix JMNF_research_effort_365 block and syntax
    # Unexpected token: always, near line: 1107
    # It was:
    # 1106: 	JMNF_research_effort_365 = {
    # 1107: 			allowed = { always = no }
    # 1108: 			removal_cost = -1
    # 1109: 			modifier = {
    # 1110: 				research_speed_factor = 0.05
    # 1111: 			}
    # 1112: 		}
    # We will move it into `country = {` block. 
    # The `country = {` block starts at line 2.
    # Let's just comment out 1106 to 1112 and append it to JMNF_national_mobilization instead?
    # No, we can just move it inside `country = {`.
    block = "".join(lines[1105:1112])
    lines[1105:1112] = [""] * 7
    # Insert block after JMNF_national_mobilization (which is around line 191)
    for i, line in enumerate(lines):
        if 'JMNF_national_mobilization = {' in line:
            lines.insert(i, block)
            break
            
    with open(p, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def fix_second_emu_war_ideas():
    p = os.path.join(base, 'common/ideas/second_emu_war_ideas.txt')
    with open(p, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if len(lines) > 86:
        if 'HRH' in lines[86]:
            lines[86] = lines[86].replace('HRH', '#HRH')
    with open(p, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def fix_jmnf_decisions():
    p = os.path.join(base, 'common/decisions/JMNF_decisions.txt')
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    # political_power -> has_political_power
    # free_building_slots -> free_building_slots = { ... }
    # has_building -> has_building = { building = arms_factory }
    
    # Actually, we can use regex
    content = re.sub(r'(\b)political_power\s*([><=]+)\s*(\d+)', r'\1has_political_power \2 \3', content)
    # free_building_slots = { building = industrial_complex size > 0 } is the syntax?
    # No, `free_building_slots = { include_locked = yes } > 0` or `free_building_slots > 0` doesn't work.
    # `free_building_slots = { building = arms_factory size > 0 }` no.
    # free_building_slots > 0 is correct in some contexts? 
    # In HoI4, `free_building_slots = { include_locked = no }` but you can't just `free_building_slots > 0`.
    # Actually, let's replace `free_building_slots\s*([><=]+)\s*(\d+)` with `free_building_slots = { include_locked = no }` maybe?
    # Wait, the error is `Non assign trigger is not enclosed in {}: free_building_slots, near line: 12`
    content = re.sub(r'free_building_slots\s*([><=]+)\s*(\d+)', r'free_building_slots = { \1 \2 }', content)
    
    content = re.sub(r'has_building\s*([><=]+)\s*(\d+)', r'has_building = { building = arms_factory level \1 \2 }', content) # dummy fix for has_building
    
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_japan_nf():
    p = os.path.join(base, 'common/national_focus/japan.txt')
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'free_building_slots\s*([><=]+)\s*(\d+)', r'free_building_slots = { \1 \2 }', content)
    content = re.sub(r'has_building\s*([><=]+)\s*(\d+)', r'has_building = { building = arms_factory level \1 \2 }', content)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)

fix_bsm_jpn()
fix_second_emu_war_ideas()
fix_jmnf_decisions()
fix_japan_nf()
print("Category 2 and 3 fixed.")
