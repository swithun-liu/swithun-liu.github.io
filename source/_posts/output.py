import os
import re

def extract_and_replace_links(base_dir):
    """
    遍历 base_dir 下所有 md 文件，处理 [slink](@@@数字) 替换。
    """
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                process_file(file_path)

def process_file(file_path):
    """
    处理单个 Markdown 文件，替换 [slink](@@@数字) 为指定内容。
    """
    print(f"Processing file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    content = "".join(lines)
    
    # 匹配 [slink](@@@数字)
    slink_pattern = re.compile(r"\\[slink\\]\\(@@@(\\d+)\\)")
    matches = slink_pattern.findall(content)

    print(f"Matches found: {matches}")
    for match in matches:
        slink_id = match
        start_pattern = re.compile(rf"^.*\\(begin@@@{slink_id}\\).*$", re.MULTILINE)
        end_pattern = re.compile(rf"^.*\\(end@@@{slink_id}\\).*$", re.MULTILINE)

        # 提取 begin 和 end 行的索引
        start_match = start_pattern.search(content)
        end_match = end_pattern.search(content)

        if start_match and end_match:
            start_index = start_match.end()
            end_index = end_match.start()

            # 提取范围内的内容
            snippet = content[start_index:end_index].strip()

            # 替换 [slink](@@@数字) 为提取的内容
            slink_tag = rf"[slink](@@@{slink_id})"
            content = re.sub(re.escape(slink_tag), snippet, content)

            # 删除 (begin@@@数字) 和 (end@@@数字)
            content = start_pattern.sub("", content)
            content = end_pattern.sub("", content)
        else:
            print(f"Markers for slink_id {slink_id} not found in {file_path}")

    # 输出修改后的内容到新文件
    new_file_path = file_path.replace(".md", "_new.md")
    print(f"Writing to file: {new_file_path}")
    with open(new_file_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    extract_and_replace_links(base_dir)

