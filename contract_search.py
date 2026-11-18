# -*- coding: utf-8 -*-
"""
contract_search.py —— 工程合约条款检索工具 v0.1

功能：读取一份工程合约，按关键词找出相关条款。

用法：
    python contract_search.py

这里是你第一个「项目文件」。和 practice_*.py 的区别：
    练习文件 = 学习用的草稿，可以乱
    项目文件 = 要给别人看的成品，要干净

今天的目标：把练习里的代码重组进这三个函数里。
"""

import os


# ============================================================
# 函数 1：读取文件
# ============================================================
def load_text(path):
    """读取文件，返回全部文字。"""
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(path)
        return "\n".join((page.extract_text() or "") for page in reader.pages)

    with open(path, encoding="utf-8") as f:
        return f.read()


# ============================================================
# 函数 2：把行合并成条款
# ============================================================
def split_clauses(lines):
    """..."""
    
    clauses = []
    current = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        head = line[:6]
        if line.startswith("第") and "条" in head:
            if current:
                clauses.append(current)
            current = line
        else:
            current = current + " " + line
    if current:
        clauses.append(current)
    return clauses


# ============================================================
# 函数 3：检索
# ============================================================
def search(clauses, keyword):
    """找出所有包含关键词的条款。"""
    hits = []
    kw = keyword.replace(" ","")
    for clause in clauses:
        if kw in clause.replace(" ",""):
            hits.append(clause)
    return hits

# ============================================================
# 主流程：把三个函数串起来
# ============================================================
def main():
    # 找到本文件所在的目录，再拼出合约文件的路径
    # 这样不管从哪里运行，都能找对文件
    base = os.path.dirname(os.path.abspath(__file__))
    # 有 PDF 就用 PDF，没有就退回 txt
    pdf_path = os.path.join(base, "sample_contract.pdf")
    txt_path = os.path.join(base, "sample_contract.txt")
    filepath = pdf_path if os.path.exists(pdf_path) else txt_path

    # 检查文件是否存在
    if not os.path.exists(filepath):
        print(f"找不到文件：{filepath}")
        return

    # 第 1 步：读文件
    text = load_text(filepath)
    print(f"已读取文件，共 {len(text)} 个字符。")

    # 第 2 步：切成条款
    clauses = split_clauses(text.splitlines())
    print(f"共切出 {len(clauses)} 条条款。")

    # 第 3、4 步：循环提问
    while True:
        keyword = input("请输入关键词（直接回车退出）：").strip()

        if not keyword:
            print("再见。")
            break

        hits = search(clauses, keyword)
        print()
        print(f"包含「{keyword}」的条款有 {len(hits)} 条：")
        for i, clause in enumerate(hits, start=1):
            print()
            print(f"--- 第 {i} 条命中 ---")
            print(clause)


# 这一行是 Python 的标准写法，意思是：
# 「只有直接运行这个文件时才执行 main()」
# 如果这个文件被别的程序 import，就不会自动跑。
# 现在照抄就行，以后会讲。
if __name__ == "__main__":
    main()
