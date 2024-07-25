from docx import Document

# path = r'D:\aData\SFT\sft数据整理0722\YonBIP理念、价值和体系学习考试题库V3.0.docx'

def docx2list(path):
    doc = Document(path)
    list = []
    # 输出的是列表，列表中一共有4份内容
    # [<docx.text.paragraph.Paragraph object at 0x7fca95f0aba8>,
    # <docx.text.paragraph.Paragraph object at 0x7fca95f0abe0>,
    # <docx.text.paragraph.Paragraph object at 0x7fca95f0ab70>,
    #<docx.text.paragraph.Paragraph object at 0x7fca95f0ac50>,]

    for paragraph in doc.paragraphs:
        print(paragraph.text)
        list.append(paragraph.text)
    return list