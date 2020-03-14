import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QEvent
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
        self.tableWidget.itemChanged.connect(self.inittable2)

        # self.tableWidget.installEventFilter(self)
    # def eventFilter(self, widget, event):
    #     if widget == self.tableWidget:
    #         if event.type() == QEvent.MouseButtonRelease:
    #             self.inittable2()

    # def eventFilter(self, watched, event):
    #     if watched == self.tableWidget:  # 只对label1的点击事件进行过滤，重写其行为，其他的事件会被忽略
    #         if event.type() == QEvent.ActivationChange:  # 这里对鼠标按下事件进行过滤，重写其行为
    #             self.inittable2()
    #     return QWidget.eventFilter(self, watched, event)
    def inittable2(self):
        try:
             zhongtishu=self.gettimuzhongshu()
             rows=self.tableWidget_2.rowCount()
             meihangtishu=int(zhongtishu/rows)
             meihangtishu=str(meihangtishu)
             for i in range(rows):
                 self.tableWidget_2.item(i, 1).setText(meihangtishu)
                 self.tableWidget_2.item(i, 2).setText('1')
        except:
            pass

    def gettimuzhongshu(self):
        tishu = self.get_data_from_table_tishu(self.tableWidget)
        zhongtishu = 0
        for (k, v) in tishu.items():
            tishu = int(v[1])
            zhongtishu += tishu
        return zhongtishu
    def gettimuleixingzhongshu(self):
        tishu = self.get_data_from_table_tishu(self.tableWidget_2)
        zhongtishu = 0
        for (k, v) in tishu.items():
            tishu = int(v[1])
            zhongtishu += tishu
        return zhongtishu
    def kemu_tishu_init(self):
        self.tableWidget.clear()
        selecteditems = self.get_data_from_tree_selected(self.treeWidget_2)
        rows=0
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(len(selecteditems.items()))  # 行数
        self.tableWidget.setHorizontalHeaderLabels(['专业名称', '出题数量'])

        for (k,v) in selecteditems.items():
            newitem = QTableWidgetItem(k)
            self.tableWidget.setItem(rows,0,newitem)
            rows+=1

    def get_data_from_table_tishu(self,table):
        row = table.rowCount()
        column = table.columnCount()
        zhuanyetishudict={}
        for i in range(row):
                zhuanyename=table.item(i,0).text()
                rowdata=[]
                for j in range(column):
                    shuliang=table.item(i,j).text()
                    rowdata.append(shuliang)
                zhuanyetishudict[zhuanyename]=rowdata
        return zhuanyetishudict


    def zhuanye_dengji_clicked(self, item, column):
        self.item_autoselected(item)
    def zhuanye_kemu_clicked(self, item, column):
        self.item_autoselected(item)
        self.dengji_clicked()
        self.leixingtable_init()
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

    def leixingtable_init(self):
        self.tableWidget_2.clear()
        selecteditems = self.get_data_from_tree_selected(self.treeWidget_2)
        modelutoil=ModelUtil()
        timuleixing=modelutoil.get_timuleixing(selecteditems)

        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setRowCount(len(timuleixing))  # 行数
        self.tableWidget_2.setHorizontalHeaderLabels(['题目类型', '出题数', '分值'])
        rows = 0
        for i in range(len(timuleixing)):
            newitem = QTableWidgetItem(timuleixing[i])
            self.tableWidget_2.setItem(rows, 0, newitem)
            newitem1 = QTableWidgetItem("1")
            self.tableWidget_2.setItem(rows, 1, newitem1)
            newitem2 = QTableWidgetItem("1")
            self.tableWidget_2.setItem(rows, 2, newitem2)
            rows += 1

    def dengji_clicked(self):
        self.deleteItem(self.treeWidget_3)

        selecteditems = self.get_data_from_tree_selected(self.treeWidget_2)
        modelutil =  ModelUtil()
        zhunayedengjilist = modelutil.get_zhuaye_kemu_dengji(selecteditems)
        self.filldata_tree(zhunayedengjilist,self.treeWidget_3)

    def get_data_from_tree_selected(self,tree):
        selecteditems = {}
        numzhuanye = tree.topLevelItemCount()
        for i in range(numzhuanye):
            if tree.topLevelItem(i).checkState(0):
                zhuanyename = tree.topLevelItem(i).text(0)
                selecteditems[zhuanyename] = []
                kemunum = tree.topLevelItem(i).childCount()
                for j in range(kemunum):
                    if tree.topLevelItem(i).child(j).checkState(0):
                        kemuname = tree.topLevelItem(i).child(j).text(0)
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
            zhongtishu = self.gettimuzhongshu()
            timuleixingzhongtishu=self.gettimuleixingzhongshu()
            if zhongtishu==timuleixingzhongtishu:
                pass
            else:
                QtWidgets.QMessageBox.information(self, '出卷', '专业出题数与题目类型出题数不相等')
                return
        except:
            return
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
                 zhuanyetishu_dict = self.get_data_from_table_tishu(self.tableWidget)
                 zhuanye_kemu_dict = self.get_data_from_tree_selected(self.treeWidget_2)
                 dengjidict = self.get_data_from_tree_selected(self.treeWidget_3)
                 timuleixingtishu_dict = self.get_data_from_table_tishu(self.tableWidget_2)
                 shijuanname = ''

                 for (k,v) in zhuanye_kemu_dict.items():
                     shijuanname+=k


                 fenzhi = {}
                 timuleixingshudict = {}
                 for (k, v) in timuleixingtishu_dict.items():
                     fenzhi[k]=(v[2])
                     timuleixingshudict[k] = int(v[1])
                 fenzhi['时间']=(self.lineEdit_2.text())

                 # # zhuanyedict = {'数学': ['第一章', '第二章', '第三章'], '英语': ['第三章', '第四章', '第五章']}
                 # dsaf = {'单选题': ['单选题', '0', '0'], '多选题': ['多选题', '0', '0'], '判断题': ['判断题', '0', '0'], '填空题': ['填空题', '0', '0'], '简答题': ['简答题', '0', '0']}
                 #
                 # er={'数学': ['数学', '5'], '英语': ['英语', '5']}
                 # eqrw={'数学': ['四级', '五级'], '英语': ['三级', '四级', '五级']}


                 # dengjilist = ['五级', '四级']
                 # zhuanyetishudict = {'战伤救护': {'xz':1,'mxz':1,'pd':1,'tk':1,'jd':1}, '英语': {'xz':1,'mxz':1,'pd':1,'tk':0,'jd':0}}
                 # timuleixingshudict = {'单选题': 20, '多选题':20, '判断题': 20, '填空题': 20, '简答题': 20}

                 rand = random_createpaper(zhuanye_kemu_dict, dengjidict, zhuanyetishu_dict, timuleixingshudict)
                 # rand = random_createpaper(zhuanye_kemu_dict, dengjilist, zhuanyetishudict, timuleixingshudict)
                 questionidlist=rand.create_random_paper()

                 if  type(questionidlist) is str:
                     QtWidgets.QMessageBox.information(self, '出卷', questionidlist)
                 else:
                     # paper = createpaper(self.coursename)
                     # questionidlist = paper.createpaper()
                     # questionidlist.pop()
                     try:
                         exporttoword = RandExportToWord(self.filepath, self.filename,fenzhi)
                         exporttoword.exportpaper(str(i), questionidlist,shijuanname)
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
