import shelve
from typing import Union

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QApplication, \
    QListWidget, QFileDialog
import sys
from PyQt5.QtGui import QPixmap
from Similarity import Similarity


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._init_Sim()

        self.current_show_name=''
        self.current_show_image_path=''

        self.add_person_btn.clicked.connect(self._clilked_add_persion_btn_slot)
        self.find_person_btn.clicked.connect(self._clilked_find_persion_btn_slot)
    def _setup_ui(self):
        self.lefttop=(100,100)
        self.size=(1200,600)
        self.setGeometry(*self.lefttop,*self.size)

        self.add_person_btn=QPushButton('add')
        self.rm_person_btn=QPushButton('rm')
        self.find_person_btn=QPushButton('find')

        self.person_id_lable=QLabel('person_id')
        self.person_image_lable=QLabel('person_image')
        self.person_info_list=QListWidget()

        self.vbox_1L=QVBoxLayout(self)
        self.vbox_2L_btns=QHBoxLayout()
        self.vbox_2L_labels=QHBoxLayout()
        self.vbox_3L_lists=QVBoxLayout()
        self.vbox_1L.addLayout(self.vbox_2L_btns)
        self.vbox_1L.addLayout(self.vbox_2L_labels)
        self.vbox_2L_labels.addLayout(self.vbox_3L_lists,stretch=3)

        self.vbox_2L_btns.addWidget(self.add_person_btn)
        self.vbox_2L_btns.addWidget(self.rm_person_btn)
        self.vbox_2L_btns.addWidget(self.find_person_btn)

        self.vbox_2L_labels.addWidget(self.person_image_lable,stretch=7)

        self.vbox_3L_lists.addWidget(self.person_id_lable)
        self.vbox_3L_lists.addWidget(self.person_info_list)


        self.show()
    def _init_Sim(self):
        self.sim = Similarity()
        self.shelf_db=shelve.open('image_db.dat')
    def __del__(self):
        self.shelf_db.close()
    def add_person(self,image_path:str):
        _,name=self.sim.add_person(image_path)
        self.shelf_db['name']=image_path
    def rm_person(self,person_id:str):
        if person_id in self.shelf_db.keys():
            del self.shelf_db[person_id]
            self.rm_persion(person_id)
    def find_person(self,image_path:str)->Union[str,None]:
        name,score=self.sim.find_person(image_path)
        if score>0.7:
            return name


    def update_image_ui(self):
       if  self.current_show_image_path and self.current_show_name:
           self.person_id_lable.setText(self.current_show_name)
           img=QPixmap(self.current_show_image_path)
           if img.width()>300:
               img=img.scaledToWidth(300)
           self.person_image_lable.setPixmap(img)
       else:
           self.person_id_lable.setText("none")
           self.person_image_lable.setPixmap(QPixmap())
    def update_person_list_ui(self):
        # for k,v in self.shelf_db.items():
        #     item=QListWidgetItem(self.person_info_list)
        pass

    def _clilked_add_persion_btn_slot(self):
        files, _ =QFileDialog.getOpenFileNames(self,'select files',filter='jpg(*.jpg);;png(*.png)')
        for file in files:
            is_unique,name=self.sim.add_person(file)
            if is_unique:
                self.shelf_db[name]=file
    def _clilked_find_persion_btn_slot(self):
        files, _ =QFileDialog.getOpenFileNames(self,'select files',filter='jpg(*.jpg);;png(*.png)')
        if files:
            file=files[0]
            name,score=self.sim.find_person(file)
            if score>0.7:
                self.current_show_name = name
                self.current_show_image_path=self.shelf_db[name]
            else:
                self.current_show_name = ""
                self.current_show_image_path=''
            self.update_image_ui()
if __name__ == '__main__':
    app=QApplication(sys.argv)
    w=MainWidget()
    sys.exit(app.exec_())
