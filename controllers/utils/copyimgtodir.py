import os
import shutil
class CopyImgToDir(object):
    def __init__(self,fname,des_dir):
        self.fname = fname
        self.des_dir = des_dir

    def copy_img_to_dir(self):
        file = os.path.isfile(self.fname)
        if file:
            self.filepath, self.filename = os.path.split(self.fname)
            destination=self.des_dir+'\\'+self.filename
            if destination not in self.fname :
                shutil.copyfile(self.fname, destination)

# fname = r'C:\Users\MSI-PC\Desktop\1.xls'
# des_dir=r'E:\迅雷下载'
# copy = CopyImgToDir(fname,des_dir)
# copy.copy_img_to_dir()



