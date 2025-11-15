这是一个fork自 https://github.com/karpathy/nanoGPT 的项目，我想基于这个项目来学习语言模型的训练。

我的设备信息：

- 一台 HP ZBook G11 笔记本电脑；

- CPU架构：x86_64的Intel(R) Core(TM) Ultra 7 155H (1.40 GHz)；
- 内存：64G；
- 显卡：RTX4060（8G显存）；
- 操作系统：Windows11，安装了 Nvidia 显卡 581.29版本驱动；
- 通过wsl2部署了Ubuntu24.04；

硬件限制：

- 你必须注意的是，我只有1台笔记本电脑，绝对不要尝试使用什么分布式训练的技术，包括但不限于多台机器、多卡训练等。

软件信息：

- wls2 的 Ubuntu 中的用户名为 kevin，home目录为：/home/kevin；

- 安装了 /home/kevin/miniconda3，创建了 nanogpt 虚拟环境，并且安装了需要的依赖包；

- 项目目录：/home/kevin/nanoGPT；

- 数据路径：/home/kevin/trainData，存放了从 https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2 下载的维基百科中文语料（使用命令 `wikiextractor -o wiki_text zhwiki-latest-pages-articles.xml` 提取了 zhwiki-latest-pages-articles.xml，存放到 /home/kevin/trainData/wiki_text 目录中），其内存放了1497915篇文章。使用如下merge_wiki_doc.py 脚本将其数据提取到 /home/kevin/trainData/wiki_corpus/train.txt 文件中：

  ```python
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
  ```

- llama.cpp：位置在 /home/kevin/llama.cpp，并通过 `make clean && LLAMA_CUDA=1 make` 完成了编译。

你的目标：

1. 首先用 nanoGPT 自带的“莎士比亚”数据集，完成模型训练，并转换成HuggingFace格式（GGUF）使用 llama.cpp 装载模型并完成问答测试；
2. 然后将这个模型装载到 ollama 中并完成问答测试；
3. 完成训练过程中详细的指导文档；
4. 最后再开始使用 /home/kevin/trainData 下的数据集训练中文语言模型。

限制条线：

- 所有的训练，包括小规模数据训练测试模型，都必须使用cuda来加速训练；
- 你需要使用 `conda activate nanogpt` 来激活这个虚拟环境；
- 在训练中文模型时必须注意分词问题，必须和 ollama、llama.cpp 加载模型兼容分词器。