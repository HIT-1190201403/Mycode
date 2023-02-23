import pymysql
import sys
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
import numpy as np
from PySide2.QtCore import *


class Menu:

    def __init__(self):
        self.ui = QUiLoader().load("menu.ui")
        self.ui.pushButton.clicked.connect(self.query1)
        self.ui.pushButton_2.clicked.connect(self.delete1)
        self.ui.pushButton_3.clicked.connect(self.insert1)
        self.ui.show()

    def query1(self):
        self.ui = QUiLoader().load("query1.ui")
        self.ui.pushButton.clicked.connect(self.queryButton)
        self.ui.show()

    def insert1(self):
        self.ui = QUiLoader().load("table.ui")
        self.ui.pushButton.clicked.connect(self.insertButton)
        self.ui.show()

    def delete1(self):
        self.ui = QUiLoader().load("table.ui")
        self.ui.pushButton.clicked.connect(self.deleteButton)
        self.ui.show()

    def queryButton(self):
        sql = "SELECT "
        t = []
        field = []
        for i in range(28):
            s = "checkBox_" + str(i + 1)
            temp = getattr(self.ui, s)
            if temp.isChecked():
                t1 = temp.parent().title()
                sql = sql + t1 + "." + temp.text() + ","
                field.append(t1 + "." + temp.text())
                if not (t1 in t):
                    t.append(temp.parent().title())
        sql = sql[:-1] + " FROM "
        for i in t:
            sql = sql + i + ","
        sql = sql[:-1]
        self.ui = QUiLoader().load("empty.ui")
        self.ui.table = QTableWidget(self.ui)
        self.ui.table.setColumnCount(3)
        self.ui.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.table.setGeometry(0, 100, self.ui.width(), self.ui.height() - 300)
        self.ui.table.setHorizontalHeaderLabels(['字段', '条件', '数值'])
        self.ui.addCondition = QPushButton(self.ui.centralwidget)
        self.ui.addCondition.setGeometry(400, 670, 150, 50)
        self.ui.addCondition.setText("增加条件")
        self.ui.runButton = QPushButton(self.ui.centralwidget)
        self.ui.runButton.setGeometry(600, 670, 150, 50)
        self.ui.runButton.setText("查询")
        self.group = ""
        self.ui.groupButton = QPushButton(self.ui.centralwidget)
        self.ui.groupButton.setGeometry(800, 670, 150, 50)
        self.ui.groupButton.setText("分组")
        self.ui.runButton.clicked.connect(lambda: self.queryButton2(sql, field))
        self.ui.addCondition.clicked.connect(lambda: self.conditionButton(field))
        self.ui.groupButton.clicked.connect(lambda: self.groupButton(field))
        self.ui.show()

    def groupButton(self, field):
        a, b = QInputDialog.getItem(self.ui, "分组", "选择分组属性", field, 0, False)
        if b:
            self.group = "GROUP BY " + str(a)

    def conditionButton(self, field):
        self.ui.table.insertRow(self.ui.table.rowCount())
        combo = QComboBox()
        combo.addItems(field)
        self.ui.table.setCellWidget(self.ui.table.rowCount() - 1, 0, combo)

    def insertButton(self):
        b = 0
        for i in range(8):
            s = "radioButton_" + str(i + 1)
            if getattr(self.ui, s).isChecked():
                b = 1
                self.name = getattr(self.ui, s).text()
        if b == 1:
            self.ui = QUiLoader().load("empty.ui")
            self.drawTable_2()
            self.ui.commit.setText("插入")
            self.ui.commit.clicked.connect(self.insertButton2)
            self.ui.show()
        else:
            msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '请选择要插入的表！')
            msg_box.exec_()

    def deleteButton(self):
        b = 0
        for i in range(8):
            s = "radioButton_" + str(i + 1)
            if getattr(self.ui, s).isChecked():
                b = 1
                self.name = getattr(self.ui, s).text()
        if b == 1:
            self.ui = QUiLoader().load("empty.ui")
            self.drawTable()
            self.ui.commit.setText("删除")
            self.ui.commit.clicked.connect(self.deleteButton2)
            self.ui.show()
        else:
            msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '请选择要删除的表！')
            msg_box.exec_()

    def drawTable(self):
        sql = "SELECT * FROM " + self.name
        self.r1 = cursor.execute(sql)
        self.r2 = cursor.fetchall()
        sql = "SELECT * FROM information_schema.columns WHERE table_schema= 'school' AND table_name = '" + self.name + "'"
        cursor.execute(sql)
        mes = cursor.fetchall()
        self.des = [[] for i in range(len(mes))]
        for i in range(len(mes)):
            self.des[i].append(mes[i][7])
            self.des[i].append(mes[i][3])
        self.ui.table = QTableWidget(self.ui)
        self.ui.label = QLabel(self.ui.centralwidget)
        self.ui.label.setText("请选择要删除第几条数据")
        name = [0 for i in range(len(self.des))]
        for i in range(len(self.des)):
            name[i] = self.des[i][1]
        self.ui.table.setRowCount(self.r1)
        self.ui.table.setColumnCount(name.__len__())
        self.ui.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.table.setGeometry(0, 100, self.ui.width(), self.ui.height() - 300)
        self.ui.table.setHorizontalHeaderLabels(name)
        for i in range(self.r1):
            for j in range(len(name)):
                self.ui.table.setItem(i, j, QTableWidgetItem(str(self.r2[i][j])))
        self.ui.commit = QPushButton(self.ui.centralwidget)
        self.ui.commit.setGeometry(400, 670, 75, 50)
        self.ui.t = QTextEdit(self.ui.centralwidget)
        self.ui.t.setGeometry(500, 675, 75, 40)

    def drawTable_2(self):
        self.drawTable()
        self.ui.t.close()
        self.ui.label.setText("请在表格最后一行输入数据")
        self.ui.commit.setGeometry(500, 670, 75, 50)
        self.ui.table.insertRow(self.r1)

    def queryButton2(self, sql, field):
        n = self.ui.table.rowCount()
        if n > 0:
            sql = sql + " WHERE "
        for i in range(n):
            sql = sql + str(self.ui.table.cellWidget(i, 0).currentText()) + str(self.ui.table.item(i, 1).text()) + str(
                self.ui.table.item(i, 2).text()) + " AND "
        if n > 0:
            sql = sql[:-4] + self.group
        else:
            sql = sql + " " + self.group
        print(sql)
        self.ui = QUiLoader().load("empty.ui")
        try:
            r1 = cursor.execute(sql)
            r2 = cursor.fetchall()
            self.ui.table = QTableWidget(self.ui)
            self.ui.table.setRowCount(r1)
            self.ui.table.setColumnCount(len(field))
            self.ui.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.ui.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.ui.table.setGeometry(0, 100, self.ui.width(), self.ui.height() - 300)
            self.ui.table.setHorizontalHeaderLabels(field)
            for i in range(r1):
                for j in range(len(field)):
                    self.ui.table.setItem(i, j, QTableWidgetItem(str(r2[i][j])))
            self.ui.quitButton = QPushButton(self.ui.centralwidget)
            self.ui.quitButton.setText("确定")
            self.ui.quitButton.clicked.connect(self.quitButton)
            self.ui.quitButton.setGeometry(500, 670, 75, 50)
            self.ui.show()
        except Exception:
            msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '请选择正确的查询条件！')
            msg_box.exec_()
            self.__init__()

    def quitButton(self):
        self.__init__()

    def deleteButton2(self):
        text = self.ui.t.toPlainText()
        l = [str(i + 1) for i in range(self.r1)]
        if text in l:
            text = int(text)
            sql = "DELETE FROM " + str(self.name) + " WHERE "
            for i in range(len(self.des)):
                if self.des[i][0] == "varchar" or self.des[i][0] == "char":
                    sql = sql + self.des[i][1] + " = \"" + str(self.r2[text - 1][i]) + "\" and " \
                                                                                       "zzzzz"
                else:
                    sql = sql + self.des[i][1] + " = " + str(self.r2[text - 1][i]) + " and "
            sql = sql[:-5]
            print(sql)
            try:
                cursor.execute(sql)
                connect.commit()
            except:
                msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '存在外键约束，不能删除该数据！')
                msg_box.exec_()
            finally:
                self.__init__()
        else:
            msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '请输入有效数字！')
            msg_box.exec_()

    def insertButton2(self):
        sql = "INSERT INTO " + str(self.name) + " VALUES("
        for i in range(len(self.des)):
            if self.ui.table.item(self.r1, i) is None:
                sql = sql + "NULL,"
            else:
                if self.des[i][0] == "varchar" or self.des[i][0] == "char":
                    sql = sql + "'" + str(self.ui.table.item(self.r1, i).text()) + "',"
                else:
                    sql = sql + str(self.ui.table.item(self.r1, i).text()) + ","
        sql = sql[:-1] + ")"
        print(sql)
        try:
            cursor.execute(sql)
            connect.commit()
            self.__init__()
        except pymysql.err.IntegrityError as a:
            print(a.args)
            if a.args[0] == 1048:
                msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '主键不能为空！')
                msg_box.exec_()
            if a.args[0] == 1062:
                msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '主键不能重复！')
                msg_box.exec_()
            if a.args[0] == 1452:
                msg_box = QMessageBox(QMessageBox.Warning, 'Warning', '存在外键约束！')
                msg_box.exec_()


connect = pymysql.connect(host="localhost", user="root", password="1234", charset="utf8", database="school")
cursor = connect.cursor()
app = QApplication()
stats = Menu()
sys.exit(app.exec_())
