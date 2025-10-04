import os
import re
from collections import defaultdict
from opcode import def_op


def update_loc_list(modid):
    print("Updating Location List...")
    loc_path = f"{modid}/localisation"
    langs = os.path.isdir(loc_path)
    print(langs)




def process_tags_from_directory(tags: list[str], directory_path: str) -> tuple[list, list, list]:
    """
    TAGリストとディレクトリパスを受け取り、統合データ、ファイルごとの不足キー、
    そしてキーの重複情報を返す。
    """
    master_yml_data = {}
    key_locations = defaultdict(list)

    if not os.path.isdir(directory_path):
        print(f"エラー: ディレクトリ '{directory_path}' が見つかりません。")
        return [], [], []

    # --- 1. ディレクトリ内の全ファイルを読み込み、master_yml_data に集約 ---
    for dirpath, _, filenames in os.walk(directory_path):
        for filename in sorted(filenames):
            if not (filename.endswith('.yml') or filename.endswith('.txt')):
                continue

            file_path = os.path.join(dirpath, filename)

            try:
                with open(file_path, 'r', encoding='utf-8-sig') as f:
                    for line in f:
                        line = line.strip()
                        if ':' not in line: continue
                        key, raw_value = line.split(':', 1)
                        key = key.strip()
                        match = re.search(r'"(.*?)"', raw_value)
                        if match:
                            value = match.group(1)
                            # データをマスター辞書に直接追加
                            master_yml_data[key] = value
                            # キーがどのファイルにあったかを記録
                            key_locations[key].append(filename)
            except Exception as e:
                print(f"警告: ファイル '{filename}' の読み込み中にエラーが発生しました: {e}")
                continue

    # --- 2. 全ファイルの集約データから `found_data` と `missing_tags` を作成 ---
    all_found_data = []
    missing_tags = []  # 最終的に不足していると判断された「国タグ」のリスト

    for tag in tags:
        # 国タグに関連する3つのキー (例: USA, USA_DEF, USA_ADJ)
        keys_to_check = [tag, f"{tag}_DEF", f"{tag}_ADJ"]
        tag_values = []
        is_found = False  # この国タグのキーが1つでも見つかったかどうかのフラグ

        for key in keys_to_check:
            if key in master_yml_data:
                is_found = True
                tag_values.append(master_yml_data[key])

        if is_found:
            # 1つでもキーが見つかれば、取得できたデータとして追加
            all_found_data.append([tag, tag_values])
        else:
            # 関連するキーがどのファイルにも一つも見つからなければ、不足タグとして追加
            missing_tags.append(tag)

    # --- 3. キーの重複情報を集計 ---
    duplicate_data = []
    for key, files in key_locations.items():
        if len(files) > 1:
            duplicate_data.append([key, files])

    # 戻り値の2番目を新しい `missing_tags` に変更
    return all_found_data, missing_tags, duplicate_data

def country_counter(file_path):
   return len(country_getter(file_path))

def country_getter(file_path):
    """
    指定されたテキストファイルから、特定のパターンを持つ3文字の
    大文字アルファベットコードを抽出し、リストとして返します。

    パターン：
    - 行の先頭から始まる
    - 3文字の大文字アルファベットである
    - 後ろに'='が続く（スペースはあってもなくても良い）
    - '#'で始まるコメント行や関係のない行は無視する

    Args:
        file_path (str): 処理対象のファイルパス。

    Returns:
        list: 抽出された3文字コードのリスト。
    """
    codes = []

    # 正規表現パターンを定義します。
    # ^       : 行の先頭
    # ([A-Z]{3}) : 3文字の大文字アルファベット。()で囲むことでこの部分だけを抽出対象とします。
    # \s* : 0個以上の空白文字（スペースやタブなど）
    # =       : 等号記号
    pattern = re.compile(r'^([A-Z]{3})\s*=')

    try:
        # ファイルを開いて一行ずつ読み込みます。
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # 行の前後の余分な空白を削除します。
                stripped_line = line.strip()

                # コメント行や空行は処理対象外とします。
                if not stripped_line or stripped_line.startswith('#'):
                    continue

                # 正規表現でパターンに一致するかをチェックします。
                match = pattern.match(stripped_line)
                if match:
                    # パターンに一致した場合、抽出対象のグループ（3文字コード）をリストに追加します。
                    codes.append(match.group(1))

    except FileNotFoundError:
        print(f"エラー: ファイル '{file_path}' が見つかりませんでした。")
    except Exception as e:
        print(f"ファイルの処理中にエラーが発生しました: {e}")

    return codes

def all_country_getter(modid):
    path = f"{modid}/common/country_tags"
    countries = []
    c_c = 0
    for file in os.listdir(path):
        if file.endswith(".txt"):
            countries.extend(country_getter(os.path.join(path, file)))
            c_c = c_c + country_counter(os.path.join(path, file))
    return countries, c_c

def check_loc(lang,modid,countries):
    loc_path = ""
    if lang == "japanese":
        loc_path = f"{modid}/localisation/japanese"
        postfix = "_l_japanese.yml"
    elif lang == "english":
        loc_path =  f"{modid}/localisation/english"
        postfix = "_l_english.yml"

    found, missing, duplicate = process_tags_from_directory(countries, loc_path)
    return found, missing, duplicate

def read_country_name(TAG, modid,lang,TYPE):
    path = f"{modid}/localisation/{lang}"
    found, missing, duplicate = check_loc(lang, modid, path)


if __name__ == '__main__':
    modid = "bakasekai"
    cs,cc = all_country_getter(modid)
    print(cs)
    print(cc)
    found, missing, duplicate = check_loc("japanese", modid, cs)
    print("✅ 取得できたデータ (全ファイル統合):")
    print(found) # 長すぎる場合はコメントアウトしてもOK
    print(f"\n❌ 定義が見つからなかった国タグ ({len(missing)}件):")
    if missing:
        print(missing)
    else:
        print("不足している国タグはありませんでした。")
    print(f"\n⚠️ 重複していたキー ({len(duplicate)}件):")
    for item in duplicate:
        print(f"- '{item[0]}' が次のファイルで重複: {item[1]}")
    update_loc_list(modid)