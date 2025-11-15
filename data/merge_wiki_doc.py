# merge_wiki_doc.py
import os
from pathlib import Path

def merge_wiki_doc_to_txt(input_dir, output_file):
    input_path = Path(input_dir)
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    article_count = 0
    with open(output_file, "w", encoding="utf-8") as out_f:
        for subdir in input_path.iterdir():
            if not subdir.is_dir():
                continue
            for file_path in sorted(subdir.iterdir()):
                if not file_path.name.startswith("wiki_"):
                    continue
                with open(file_path, "r", encoding="utf-8") as in_f:
                    lines = in_f.readlines()

                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    if line.startswith("<doc "):
                        i += 2  # 跳过 <doc> 行 和 标题行（如“数学”）
                        content_lines = []
                        while i < len(lines) and not lines[i].strip().startswith("</doc>"):
                            raw_line = lines[i]
                            stripped = raw_line.rstrip('\n\r')  # 保留左侧空格（如有），但去掉换行符
                            # 仅当该行有非空白字符时才保留
                            if stripped.strip():  # 如果去除前后空白后不为空
                                content_lines.append(stripped)
                            # 如果是空行，直接跳过（不 append）
                            i += 1
                        # 跳过 </doc>
                        i += 1

                        # 合并有效内容（用单个换行连接，文章之间用双换行分隔）
                        if content_lines:
                            content = "\n".join(content_lines).strip()
                            if content:
                                out_f.write(content + "\n\n")
                                article_count += 1
                                if article_count % 100000 == 0:
                                    print(f"✅ 已合并 {article_count} 篇文章")
                    else:
                        i += 1

    print(f"🎉 合并完成！共 {article_count} 篇文章，保存至: {output_file}")

if __name__ == "__main__":
    merge_wiki_doc_to_txt(
        input_dir="/home/kevin/trainData/wiki_text",
        output_file="/home/kevin/trainData/wiki_corpus/train.txt"
    )