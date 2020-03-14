import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from sqlalchemy.orm import sessionmaker

from controllers.utils.loginutil import CommonUtil
from PyQt5.QtWidgets import QWidget, QFileDialog, QTreeWidgetItem, QTableWidgetItem

from model.createdb import engine
from views.chujuan import  Ui_Dialog
from controllers.utils.modeutil import ModelUtil
from controllers.utils.exporttoword import ExportToWord, RandExportToWord


class chujuanform(QWidget,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(CommonUtil.APP_ICON))
        self.pushButton.clicked.connect(self.exportpaper)
        self.inittree()
        self.treeWidget_2.itemClicked.connect(self.zhuanye_kemu_clicked)
        self.treeWidget_3.itemClicked.connect(self.zhuanye_dengji_clicked)
        self.pushButton.clicked.connect(self.chujuan)
    def chujuan(self):
        pass
    def kemu_tishu_init(self):
        self.tableWidget.clear()
        selecteditems = self.get_kemu_zhuaye_selected()
        rows=0
        for (k,v) in selecteditems.items():
            newitem = QTableWidgetItem(k)
            self.tableWidget.setItem(rows,0,newitem)
            rows+=1


    def zhuanye_dengji_clicked(self, item, column):
        self.item_autoselected(item)
    def zhuanye_kemu_clicked(self, item, column):
        self.item_autoselected(item)
        self.dengji_clicked()
        self.kemu_tishu_init()

    def item_autoselected(self,item):
        num = item.childCount()
        # 选中专业也选择科目
        try:
            if item.checkState(0):
                for i in range(num):
                    item.child(i).setCheckState(0, Qt.Checked)
            else:
                for i in range(num):
                    item.child(i).setCheckState(0, not Qt.CheckState)
        except:
            pass




    # def getTreeWidgetRootItem(self, Item=None,treeWidget=None):
    #     """
    #     根据给定节点 Item 递归查找对应的根节点索引号
    #     如果 Item 为空，则获取当前选中节点索引号，并上推根节点的索引号
    #     :param index:
    #     :return:
    #     """
    #     if Item == None:
    #         currentItem = treeWidget.currentItem()
    #         parentItem = currentItem.parent()
    #     else:
    #         currentItem = Item
    #         parentItem = currentItem.parent()
    #     # 如果不是ROOT节点，则继续
    #     if parentItem != None:
    #         rootItem = self.getTreeWidgetRootItem(parentItem)
    #     else:
    #         rootItem = currentItem
    #     return rootItem

    def dengji_clicked(self):
        self.deleteItem(self.treeWidget_3)

        selecteditems = self.get_kemu_zhuaye_selected()
        modelutil =  ModelUtil()
        zhunayedengjilist = modelutil.get_zhuaye_kemu_dengji(selecteditems)
        self.filldata_tree(zhunayedengjilist,self.treeWidget_3)

    def get_kemu_zhuaye_selected(self):
        selecteditems = {}
        numzhuanye = self.treeWidget_2.topLevelItemCount()
        for i in range(numzhuanye):
            if self.treeWidget_2.topLevelItem(i).checkState(0):
                zhuanyename = self.treeWidget_2.topLevelItem(i).text(0)
                selecteditems[zhuanyename] = []
                kemunum = self.treeWidget_2.topLevelItem(i).childCount()
                for j in range(kemunum):
                    if self.treeWidget_2.topLevelItem(i).child(j).checkState(0):
                        kemuname = self.treeWidget_2.topLevelItem(i).child(j).text(0)
                        selecteditems[zhuanyename].append(kemuname)
        return selecteditems






    def filldata_tree(self,dict,tree):

        for (k, v) in dict.items():
            shaixuanroot = QTreeWidgetItem(tree)
            shaixuanroot.setText(0, k)
            shaixuanroot.setCheckState(0, not Qt.CheckState)
            for i in range(len(v)):
                child2 = QTreeWidgetItem(shaixuanroot)
                child2.setText(0, v[i])
                child2.setCheckState(0, not Qt.CheckState)
        tree.expandAll()
    # 删除控件树子节点/根节点
    def deleteItem(self,tree):
        try:
            self.treeWidget_3.clear()
        except Exception:
            pass
    def exportpaper(self):

        try:
             papernum=int(self.lineEdit.text())
             fileName, ok2 = QFileDialog.getSaveFileName(self,
                                                         "文件保存",
                                                         "./",
                                                         "All Files (*);;Text Files (*.docx)")
             self.filepath, self.filename = os.path.split(fileName)
             self.coursename = '数学'
             for i in range(1, papernum + 1):

                 from controllers.utils.createpaper import random_createpaper
                 zhuanyedict = {'数学': ['第一章', '第二章'], '英语': ['第三章','第四章']}
                 dengjilist = ['五级', '四级']
                 zhuanyetishudict = {'数学': {'xz':1,'mxz':1,'pd':1,'tk':1,'jd':1}, '英语': {'xz':1,'mxz':1,'pd':1,'tk':0,'jd':0}}
                 timuleixingshudict = {'单选题': 20, '多选题': 20, '判断题': 20, '填空题': 20, '简答题': 20}
                 rand = random_createpaper(zhuanyedict, dengjilist, zhuanyetishudict, timuleixingshudict)
                 questionidlist=rand.create_random_paper()
                 if not questionidlist:
                     QtWidgets.QMessageBox.information(self, '出卷', '出卷失败')
                 else:
                     # paper = createpaper(self.coursename)
                     # questionidlist = paper.createpaper()
                     # questionidlist.pop()
                     try:
                         exporttoword = RandExportToWord(self.filepath, self.filename)
                         exporttoword.exportpaper(str(i), questionidlist)
                     except:
                         QtWidgets.QMessageBox.information(self, '出卷', '出卷失败')
                     # exporttoword = ExportToWord(self.filepath, self.filename, self.coursename)
                     # exporttoword.exportpaper(str(i), questionidlist)

        except:
            QtWidgets.QMessageBox.information(self, '出卷', '请输入正确数字')
    def inittree(self):
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()
        self.treeWidget_2.setColumnCount(1)
        modelutil =  ModelUtil()
        zhuanye_kemudict = modelutil.get_zhuaye_kemu()
        self.filldata_tree(zhuanye_kemudict, self.treeWidget_2)


        session.close()
