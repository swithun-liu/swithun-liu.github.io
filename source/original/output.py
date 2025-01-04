import os
import re

def extract_and_replace_links(base_dir):
    """
    遍历 base_dir 下所有 md 文件，处理 [slink](@@@数字) 替换，并将输出文件存入 shadow 目录。
    """
    # 预加载所有文件内容供后续查找 begin 和 end 标记
    file_contents = load_all_files(base_dir)

    shadow_dir = os.path.join(base_dir, "../_posts")
    if not os.path.exists(shadow_dir):
        os.makedirs(shadow_dir)

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, base_dir)
                shadow_file_path = os.path.join(shadow_dir, relative_path.replace(".md", ".md"))

                shadow_file_dir = os.path.dirname(shadow_file_path)
                if not os.path.exists(shadow_file_dir):
                    os.makedirs(shadow_file_dir)

                process_file(file_path, shadow_file_path, file_contents)

def load_all_files(base_dir):
    """
    加载 base_dir 下所有 md 文件的内容，返回 {文件路径: 内容} 的字典。
    """
    file_contents = {}
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    file_contents[file_path] = f.read()
    return file_contents

def find_markers_in_files(slink_id, file_contents):
    """
    在所有文件中查找指定 slink_id 的 begin 和 end 标记。
    """
    start_marker = f"(begin@@@{slink_id})"
    end_marker = f"(end@@@{slink_id})"

    start_match, end_match = None, None
    for file_path, content in file_contents.items():
        if not start_match:
            start_index = content.find(start_marker)
            if start_index != -1:
                start_match = (file_path, start_index + len(start_marker))
        if not end_match:
            end_index = content.find(end_marker)
            if end_index != -1:
                end_match = (file_path, end_index)
        if start_match and end_match:
            break

    return start_match, end_match

def process_file(file_path, shadow_file_path, file_contents):
    """
    处理单个 Markdown 文件，替换 [slink](@@@数字) 为指定内容，并将结果写入 shadow 文件。
    """
    print(f"Processing file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    content = "".join(lines)

    # 匹配 [slink](@@@数字)
    slink_pattern = re.compile(r"\[slink\]\(@@@(\d+)\)")
    matches = slink_pattern.findall(content)

    print(f"Matches found: {matches}")
    for match in matches:
        slink_id = match

        # 在所有文件中查找 begin 和 end 标记
        start_match, end_match = find_markers_in_files(slink_id, file_contents)

        if start_match and end_match:
            start_file, start_index = start_match
            end_file, end_index = end_match

            if start_file == end_file:
                # 提取范围内的内容
                snippet = file_contents[start_file][start_index:end_index].strip()

                print(f"Snippet for slink_id {slink_id}: {snippet}")

                # 替换 [slink](@@@数字) 为提取的内容
                slink_tag = rf"[slink](@@@{slink_id})"
                content = content.replace(slink_tag, snippet)

                # 从源文件内容中删除标记（可选，根据需求）
                file_contents[start_file] = file_contents[start_file].replace(f"(begin@@@{slink_id})", "")
                file_contents[start_file] = file_contents[start_file].replace(f"(end@@@{slink_id})", "")
            else:
                print(f"Markers for slink_id {slink_id} span multiple files, skipping.")
        else:
            print(f"Markers for slink_id {slink_id} not found in any file.")

    # 输出修改后的内容到 shadow 文件
    print(f"Writing to file: {shadow_file_path}")
    with open(shadow_file_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    extract_and_replace_links(base_dir)

