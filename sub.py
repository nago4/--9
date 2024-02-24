import os
import pickle
import sys
import random as r
import datetime as dt
import PySide6.QtWidgets as Qw
import PySide6.QtCore as Qc
import PySide6.QtTest as Qt

#手持ちのキャラ
have_list = {'鉛筆':{'攻撃力':50,'hp':200,'Lv':1,'報酬':100,'詳細':'みんなが一度は使ったことのある筆記用具の一つ。黒鉛と粘土で作った芯を入れたもの。'},
             '消しゴム':{'攻撃力':25,'hp':100,'Lv':1,'報酬':50,'詳細':'主に鉛筆などで書かれたものを消去するために使う文房具。'},
             'シャー芯':{'攻撃力':25,'hp':100,'Lv':1,'報酬':50,'詳細':'シャープペンシルを使うには必要不可欠なもの。これを購入するときは、太さをちゃんと見なければならない。'},
             '消しカス':{'攻撃力':25,'hp':100,'Lv':1,'報酬':50,'詳細':'消しゴムを使うと出てくるもの。基本はゴミ箱に捨てられるが、練けしとして遊ばれることも多い。'},
             'ノート':{'攻撃力':50,'hp':200,'Lv':1,'報酬':100,'詳細':'文章などを書く紙。'},
             'ハサミ':{'攻撃力':50,'hp':200,'Lv':1,'報酬':100,'詳細':'紙を切るための道具。'},
             '定規':{'攻撃力':50,'hp':200,'Lv':1,'報酬':100,'詳細':'線や角を書いたりものを裁ったりするときに充てる道具。'},
             '成績表':{'攻撃力':100,'hp':300,'Lv':1,'報酬':200,'詳細':'学生が恐れているであろう毎学期の最後に担任の先生から渡される表。'},
             'チョーク':{'攻撃力':100,'hp':300,'Lv':1,'報酬':200,'詳細':'黒板に何かを書くための道具。炭酸カルシウムからできている。'},
             '教科書':{'攻撃力':100,'hp':300,'Lv':1,'報酬':200,'詳細':'人々に知識を与える。この冊子を好んで読む人もいれば恐怖を感じる人もいる。'}}



#戦闘するキャラ
easy_list = {'シャー芯':{'攻撃力':25,'hp':100,'Lv':1,'報酬':50,'詳細':'シャープペンシルを使うには必要不可欠なもの。これを購入するときは、太さをちゃんと見なければならない。'},
             '消しゴム':{'攻撃力':25,'hp':100,'Lv':1,'報酬':50,'詳細':'主に鉛筆などで書かれたものを消去するために使う文房具。'},
             '消しカス':{'攻撃力':25,'hp':100,'Lv':1,'報酬':50,'詳細':'消しゴムを使うと出てくるもの。基本はゴミ箱に捨てられるが、練けしとして遊ばれることも多い。'}}
nomal_list = {'ノート':{'攻撃力':50,'hp':200,'Lv':1,'報酬':100,'詳細':'文章などを書く紙。'},
             'ハサミ':{'攻撃力':50,'hp':200,'Lv':1,'報酬':100,'詳細':'紙を切るための道具。'},
             '定規':{'攻撃力':50,'hp':200,'Lv':1,'報酬':100,'詳細':'線や角を書いたりものを裁ったりするときに充てる道具。'},
             '鉛筆':{'攻撃力':50,'hp':200,'Lv':1,'報酬':100,'詳細':'みんなが一度は使ったことのある筆記用具の一つ。黒鉛と粘土で作った芯を入れたもの。'}}
hard_list = {'成績表':{'攻撃力':100,'hp':300,'Lv':1,'報酬':200,'詳細':'学生が恐れているであろう毎学期の最後に担任の先生から渡される表。'},
             'チョーク':{'攻撃力':100,'hp':300,'Lv':1,'報酬':200,'詳細':'黒板に何かを書くための道具。炭酸カルシウムからできている。'},
             '教科書':{'攻撃力':100,'hp':300,'Lv':1,'報酬':200,'詳細':'人々に知識を与える。この冊子を好んで読む人もいれば恐怖を感じる人もいる。'}}

btn_type = Qw.QMessageBox.StandardButton

money = 0
# MainWindowクラス定義 ####
class MainWindow(Qw.QMainWindow):
  
  def __init__(self):
    super().__init__()
    self.money = 0  
    self.setWindowTitle('MainWindow') 
    self.setGeometry(200, 100, 640, 475) 
    

    #「難しさ選択」ボタン＆テキストの生成と設定
    self.lv = Qw.QLabel(self)
    self.lv.setGeometry(15,3,300,25)
    self.lv.setText('戦闘の難易度')

    self.btn_easy = Qw.QPushButton('簡単',self)
    self.btn_easy.setGeometry(10,25,100,30)
    self.btn_easy.clicked.connect(self.btn_easy_clicked)

    self.btn_nomal = Qw.QPushButton('普通',self)
    self.btn_nomal.setGeometry(130,25,100,30)
    self.btn_nomal.clicked.connect(self.btn_nomal_clicked)

    self.btn_hard = Qw.QPushButton('難しい',self)
    self.btn_hard.setGeometry(250,25,100,30)
    self.btn_hard.clicked.connect(self.btn_hard_clicked)

    #「ガチャ系」ボタン＆テキストの生成と設定
    self.lv = Qw.QLabel(self)
    self.lv.setGeometry(15,55,300,25)
    self.lv.setText('ガチャ')

    self.btn_gatya1 = Qw.QPushButton('ガチャ1',self)
    self.btn_gatya1.setGeometry(15,75,100,30)
    self.btn_gatya1.clicked.connect(self.btn_gatya1_clicked)

    self.btn_gatya2 = Qw.QPushButton('ガチャ2',self)
    self.btn_gatya2.setGeometry(135,75,100,30)
    self.btn_gatya2.clicked.connect(self.btn_gatya2_clicked)

    #「キャラ」ボタン＆テキストの生成と設定
    self.lv = Qw.QLabel(self)
    self.lv.setGeometry(255,55,300,25)
    self.lv.setText('キャラ')

    self.btn_chara = Qw.QPushButton('選択キャラの確認',self)
    self.btn_chara.setGeometry(255,75,100,30)
    self.btn_chara.clicked.connect(self.btn_chara_clicked)

    # テキストボックス
    self.tb_log = Qw.QTextEdit('',self)
    self.tb_log.setGeometry(10,110,620,250)
    self.tb_log.setReadOnly(True)
    self.tb_log.setPlaceholderText('(ここに実行ログを表示します)')

    # 出動キャラ選択の見出し
    self.a_select = Qw.QLabel(self)
    self.a_select.setGeometry(15,390,300,25)
    self.a_select.setText('攻撃を行うキャラ')
    # 出動キャラ選択の本体
    self.at_select = Qw.QComboBox(self)
    self.at_select.setGeometry(15,415,80,25)
    self.at_select.setEditable(False)
    for p in have_list:
      self.at_select.addItem(p)
    # pref_list の末尾の「空白」を初期値にセットする。
    self.at_select.setCurrentIndex(len(have_list)-1)

    # キャラ詳細選択の見出し
    self.b_select = Qw.QLabel(self)
    self.b_select.setGeometry(150,390,300,25)
    self.b_select.setText('詳細を確認するキャラ')
    # キャラ詳細選択の本体
    self.bt_select = Qw.QComboBox(self)
    self.bt_select.setGeometry(150,415,80,25)
    self.bt_select.setEditable(False)
    for p in have_list:
      self.bt_select.addItem(p)
    # pref_list の末尾の「空白」を初期値にセットする。
    self.bt_select.setCurrentIndex(len(have_list)-1)

    # 所持金
    self.sb_status = Qw.QStatusBar()
    self.setStatusBar(self.sb_status)
    self.sb_status.setSizeGripEnabled(False)
    self.sb_status.showMessage(f'所持金:{money}円')

  def btn_easy_clicked(self):
    for ea in easy_list:
        easy_list[ea]['hp']=100
    msg = ''
    selected0_index = self.at_select.currentIndex()
    selected0_chara = self.at_select.itemText(selected0_index)
    my_hp = have_list[selected0_chara]['hp']
    self.tb_log.setPlainText('')
    easy_villan = r.choice(list(easy_list))
    msg += f'{easy_villan}が現れた！\n\n'
    while my_hp > 0 and easy_list[easy_villan]['hp'] > 0:
      att0 = r.choice([0.2,1,2])
      att1 = r.choice([0.2,1,2])
      atta0 = have_list[selected0_chara]['攻撃力']*att0
      atta1 = easy_list[easy_villan]['攻撃力']*att1
      easy_list[easy_villan]['hp']-=atta0
      msg += f'{selected0_chara}の攻撃。敵に{atta0}のダメージ。\n'
      vhp=easy_list[easy_villan]['hp']
      if vhp >= 0:
         msg += f'現在の敵のhp:{vhp}、味方のhp:{my_hp}\n\n'
      else:
         msg += f'現在の敵のhp:0、味方のhp:{my_hp}\n\n'
      if my_hp <= 0 or vhp <= 0:
            break
      msg += f'{easy_villan}の攻撃。{selected0_chara}に{atta1}のダメージ。\n'
      my_hp-=atta1
      if my_hp >= 0:
         msg += f'現在の敵のhp:{vhp}、味方のhp:{my_hp}\n\n'
      else:
         msg += f'現在の敵のhp:0、味方のhp:0\n\n'
      if my_hp <= 0 or vhp <= 0:
            break

    # ループを抜けた後の処理（敵または味方が倒れた場合など）
    if my_hp <= 0 :
        msg += "味方が倒れました。"
        self.tb_log.setPlainText(msg)
    else :
        msg += "敵が倒れました。"
        self.tb_log.setPlainText(msg)
        self.money += 50
        self.sb_status.showMessage(f'所持金:{self.money}円')

  def btn_nomal_clicked(self):
    for no in nomal_list:
        nomal_list[no]['hp']=200
    msg = ''
    selected0_index = self.at_select.currentIndex()
    selected0_chara = self.at_select.itemText(selected0_index)
    my_hp = have_list[selected0_chara]['hp']
    self.tb_log.setPlainText('')
    nomal_villan = r.choice(list(nomal_list))
    msg += f'{nomal_villan}が現れた！\n\n'
    while my_hp > 0 and nomal_list[nomal_villan]['hp'] > 0:
      att0 = r.choice([0.2,1,2])
      att1 = r.choice([0.5,1,2])
      atta0 = have_list[selected0_chara]['攻撃力']*att0
      atta1 = nomal_list[nomal_villan]['攻撃力']*att1

      nomal_list[nomal_villan]['hp']-=atta0
      msg += f'{selected0_chara}の攻撃。敵に{atta0}のダメージ。\n'
      vhp=nomal_list[nomal_villan]['hp']
      if vhp >= 0:
         msg += f'現在の敵のhp:{vhp}、味方のhp:{my_hp}\n\n'
      else:
         msg += f'現在の敵のhp:0、味方のhp:{my_hp}\n\n'
      if my_hp <= 0 or vhp <= 0:
            break
      
      msg += f'{nomal_villan}の攻撃。{selected0_chara}に{atta1}のダメージ。\n'
      my_hp-=atta1
      if my_hp >= 0:
         msg += f'現在の敵のhp:{vhp}、味方のhp:{my_hp}\n\n'
      else:
         msg += f'現在の敵のhp:0、味方のhp:0\n\n'
      if my_hp <= 0 or vhp <= 0:
            break

    # ループを抜けた後の処理（敵または味方が倒れた場合など）
    if my_hp <= 0 :
        msg += "味方が倒れました。"
        self.tb_log.setPlainText(msg)
    else :
        msg += "敵が倒れました。"
        self.tb_log.setPlainText(msg)
        self.money += 100
        self.sb_status.showMessage(f'所持金:{self.money}円')

  def btn_hard_clicked(self):
        for ha in hard_list:
            hard_list[ha]['hp']=300
        msg = ''
        selected0_index = self.at_select.currentIndex()
        selected0_chara = self.at_select.itemText(selected0_index)
        my_hp = have_list[selected0_chara]['hp']
        self.tb_log.setPlainText('')
        hard_villan = r.choice(list(hard_list))
        msg += f'{hard_villan}が現れた！\n\n'
        while my_hp > 0 and hard_list[hard_villan]['hp'] > 0:
            att0 = r.choice([0.2,1,2])
            att1 = r.choice([0.5,1,2])
            atta0 = have_list[selected0_chara]['攻撃力']*att0
            atta1 = hard_list[hard_villan]['攻撃力']*att1

            hard_list[hard_villan]['hp']-=atta0
            msg += f'{selected0_chara}の攻撃。敵に{atta0}のダメージ。\n'
            vhp=hard_list[hard_villan]['hp']
            if vhp >= 0:
                msg += f'現在の敵のhp:{vhp}、味方のhp:{my_hp}\n\n'
            else:
                msg += f'現在の敵のhp:0、味方のhp:{my_hp}\n\n'
            if my_hp <= 0 or vhp <= 0:
                    break
            
            msg += f'{hard_villan}の攻撃。{selected0_chara}に{atta1}のダメージ。\n'
            my_hp-=atta1
            if my_hp >= 0:
                msg += f'現在の敵のhp:{vhp}、味方のhp:{my_hp}\n\n'
            else:
                msg += f'現在の敵のhp:0、味方のhp:0\n\n'
            if my_hp <= 0 or vhp <= 0:
                    break

        # ループを抜けた後の処理（敵または味方が倒れた場合など）
        if my_hp <= 0 :
            msg += "味方が倒れました。"
            self.tb_log.setPlainText(msg)
        else :
            msg += "敵が倒れました。"
            self.tb_log.setPlainText(msg)
            self.money += 200
            self.sb_status.showMessage(f'所持金:{self.money}円')


  def btn_gatya1_clicked(self):
      easy = r.choice(list(easy_list))
      nomal = r.choice(list(nomal_list))
      self.tb_log.setPlainText('')
      noha = r.choice([easy,nomal])
      lack_money = 500-self.money
      msg = ''
      if self.money >= 500:
          if noha in have_list :
              have_list[noha]['Lv'] += 1
              enLv =have_list[noha]['Lv']
              have_list[noha]['攻撃力'] += 5
              enat =have_list[noha]['攻撃力']
              have_list[noha]['hp'] += 25
              enhp =have_list[noha]['hp']
              msg +=f'{noha}をgetした!\n\n{noha}の以下の能力がアップした。\n'
              msg += f'Lv:{enLv}\n攻撃力:{enat}\nhp:{enhp}'
               # ガチャを引いたらお金を減らす
              self.money -= 500
              self.sb_status.showMessage(f'所持金:{self.money}円')
          else:
              msg +=f'{noha}をgetした!'
              self.money -= 500
              self.sb_status.showMessage(f'所持金:{self.money}円')
              
      elif self.money < 500:
          msgbox_title = 'ガチャ'
          msgbox_text = f'{lack_money}円不足しているため\nガチャを引くことができません。\n'
          msgbox_text += '[ESC]キーを押すと [Ok] 押下と同等の挙動をします。'
          ret = Qw.QMessageBox.information(
            self,          # 親ウィンドウ
            msgbox_title,  # タイトル
            msgbox_text,   # メッセージ本体
            btn_type.Ok    # デフォルトボタン
          )

          if ret == btn_type.Ok:
            msg = ''
          else :
            msg = '予期せぬ応答が返ってきました。'
      self.tb_log.setText(msg)
          

  def btn_gatya2_clicked(self):
      nomal = r.choice(list(nomal_list))
      hard = r.choice(list(hard_list))
      self.tb_log.setPlainText('')
      noha = r.choice([nomal,hard])
      lack_money = 1000-self.money
      msg = ''
      if self.money >= 1000:
          if noha in have_list :
              have_list[noha]['Lv'] += 1
              enLv =have_list[noha]['Lv']
              have_list[noha]['攻撃力'] += 10
              enat =have_list[noha]['攻撃力']
              have_list[noha]['hp'] += 40
              enhp =have_list[noha]['hp']
              msg +=f'{noha}をgetした!\n\n{noha}の以下の能力がアップした。\n'
              msg += f'Lv:{enLv}\n攻撃力:{enat}\nhp:{enhp}'
               # ガチャを引いたらお金を減らす
              self.money -= 1000
              self.sb_status.showMessage(f'所持金:{self.money}円')
          else:
              msg +=f'{noha}をgetした!'
              self.money -= 1000
              self.sb_status.showMessage(f'所持金:{self.money}円')
              
      elif self.money < 1000:
          msgbox_title = 'ガチャ'
          msgbox_text = f'{lack_money}円不足しているため\nガチャを引くことができません。\n'
          msgbox_text += '[ESC]キーを押すと [Ok] 押下と同等の挙動をします。'
          ret = Qw.QMessageBox.information(
            self,          # 親ウィンドウ
            msgbox_title,  # タイトル
            msgbox_text,   # メッセージ本体
            btn_type.Ok    # デフォルトボタン
          )

          if ret == btn_type.Ok:
            msg = ''
          else :
            msg = '予期せぬ応答が返ってきました。'
      self.tb_log.setText(msg)

  def btn_chara_clicked(self):
      selected_index = self.bt_select.currentIndex()
      selected_chara = self.bt_select.itemText(selected_index)
      self.tb_log.setPlainText('')
      selected_chara1 = have_list[selected_chara]['攻撃力']
      selected_chara2 = have_list[selected_chara]['hp']
      selected_chara3 = have_list[selected_chara]['Lv']
      selected_chara4 = have_list[selected_chara]['詳細']
      self.tb_log.setPlainText(f'名前：{selected_chara}\n攻撃力:{selected_chara1}\nhp:{selected_chara2}\nLv:{selected_chara3}\n詳細:{selected_chara4}')


# 本体
if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  main_window = MainWindow()
  main_window.show()
  sys.exit(app.exec())
  