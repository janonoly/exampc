import re
# regex=r'([^\\/:*?"<>|\r\n]+$)'
regex=r'([a-zA-D]:.*\.\S*)\''
# patt=r"C语言发明<img src='D:\PythonWorkspace\exam\resources\logo.jpgs' width='60' height='60' />者是谁？"
patt1='C语言发明<img src=\'D:\\PythonWorkspace\\exam\\resources\\logo.jpg\' width=\'60\' height=\'60\' />者是谁？'
mst=re.search(regex,patt1)
if mst:
    print(mst)
    print(mst.group(1))
