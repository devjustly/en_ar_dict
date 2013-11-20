#! -*-  coding: utf-8 -*-

from PySide import QtGui,QtCore
import sys
from PySide import *
import sqlite3

class Dict(QtGui.QWidget):
    def __init__(self):
        super(Dict,self).__init__()

        self.isEN = 1
        self.line = QtGui.QLineEdit()
        #self.line.returnPressed.connect(self.translate)
        self.line.textChanged.connect(self.translate)

        self.button = QtGui.QPushButton("Translate")
        self.button.clicked.connect(self.translate)
        self.trans = QtGui.QPushButton("Ar")
        self.trans.clicked.connect(self.direct)


        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.line)
        hbox.addWidget(self.button)
        hbox.addWidget(self.trans)


        self.table = QtGui.QTableWidget(0,2)
        self.table.setHorizontalHeaderLabels(["English","Arabic"])
        header = self.table.horizontalHeader()
        #header.setStretchLastSection(True)
        header.setResizeMode(QtGui.QHeaderView.Stretch)






        hbox2 = QtGui.QVBoxLayout()
        hbox2.addLayout(hbox)
        hbox2.addWidget(self.table)




        self.setWindowTitle("Dict EN->AR")
        self.setWindowIcon(QtGui.QIcon("dict.png"))
        self.setGeometry(0,20,450,600)
        self.setLayout(hbox2)
        self.show()


    def translate(self):
        print self.line.text()
        con = sqlite3.connect("data.db")
        cur = con.cursor()


        if self.isEN == 1:
            sql = "select count(*) from words_list where en like '%%%s%%'" % self.line.text()
        else:
            sql = "select count(*) from words_list where ar like '%%%s%%'" % self.line.text()

        cur.execute(sql)

        compare = cur.fetchone()[0]
        counts = 0
        x = 0
        if compare >= 50:
            counts = 50
        else:
            counts = compare



        if self.isEN == 1:
            sql = "select * from words_list where en like '%%%s%%' limit 50" % self.line.text()
        else:
            sql = "select * from words_list where ar like '%%%s%%' limit 50" % self.line.text()


        cur.execute(sql)

        self.table.setRowCount(counts)

        rows = cur.fetchall()


        for i in rows:
            print i[2]
            self.en = QtGui.QTableWidgetItem(i[2])
            self.ar = QtGui.QTableWidgetItem(i[3])

            self.table.setItem(x,0,self.en)
            self.table.setItem(x,1,self.ar)
            x += 1
            #self.resize(self.table.sizeHint())
    def direct(self):
        if self.sender().text() == "En->Ar":
            self.isEN = 1
            self.trans.setText("Ar")
            self.setWindowTitle("Dict EN->AR")
            print self.isEN
        else:
            self.isEN = 0
            self.trans.setText("Ar->En")
            self.setWindowTitle("Dict AR->EN")
            print self.isEN

    def keyPressEvent(self,e):
        if e.key() == QtCore.Qt.Key_Escape:
            #self.line.setText("")

            if len(self.line.text()) == 0:
                self.close()
            else:
                self.line.setText("")
def main():

    app = QtGui.QApplication(sys.argv)
    #app.setStyle(QtGui.QStyleFactory.create("plastique"))
    #QtGui.QSystemTrayIcon(QtGui.QIcon("dict.png"),app).show()
    dict = Dict()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
