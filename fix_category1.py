import os

def fix_bom_and_loc():
    base = '/Users/eightman/Desktop/HOI4_modding/bsm_test/bakasekai/localisation/japanese'
    
    # 1. bsm_ea_news_l_japanese.yml - add BOM
    p1 = os.path.join(base, 'bsm_ea_news_l_japanese.yml')
    with open(p1, 'rb') as f:
        content = f.read()
    if not content.startswith(b'\xef\xbb\xbf'):
        with open(p1, 'wb') as f:
            f.write(b'\xef\xbb\xbf' + content)
            
    # 2. JMNF_l_japanese.yml - fix BOM (it has double BOM right now)
    p2 = os.path.join(base, 'JMNF_l_japanese.yml')
    with open(p2, 'rb') as f:
        content = f.read()
    while content.startswith(b'\xef\xbb\xbf\xef\xbb\xbf'):
        content = content[3:]
    # Check if 'l_japanese:' is present at the start
    text = content.decode('utf-8-sig')
    if not text.lstrip().startswith('l_japanese:'):
        text = 'l_japanese:\n' + text
    with open(p2, 'w', encoding='utf-8-sig') as f:
        f.write(text)
        
    # 3. BKK_l_japanese.yml - fix colon
    p3 = os.path.join(base, 'BKK_l_japanese.yml')
    with open(p3, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if 'SJK_air_force?:0' in line:
            lines[i] = line.replace('SJK_air_force?:0', 'SJK_air_force:0')
        if 'SJK_air_force?_desc:0' in line:
            lines[i] = line.replace('SJK_air_force?_desc:0', 'SJK_air_force_desc:0')
    with open(p3, 'w', encoding='utf-8-sig') as f:
        f.writelines(lines)
        
    # 4. PRU_l_japanese.yml - fix colon
    p4 = os.path.join(base, 'PRU_l_japanese.yml')
    with open(p4, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if 'PRU_Sacred...?:0' in line:
            lines[i] = line.replace('PRU_Sacred...?:0', 'PRU_Sacred:0')
        if 'PRU_Sacred...?_desc:0' in line:
            lines[i] = line.replace('PRU_Sacred...?_desc:0', 'PRU_Sacred_desc:0')
    with open(p4, 'w', encoding='utf-8-sig') as f:
        f.writelines(lines)

fix_bom_and_loc()
print("Category 1 fixed.")
