from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import math
import random

initial_message = "You will take this test"
success_message = "Here is how well you did"
failure_message = "You have failed"
question_limit = 5
program_title = "Permit Test Simulator"
primary_color = "#bf4949"
incorrect_display_duration = 69
four_options_enabled = True
passing_score_threshold = 0.69

question_selector = 1
skipped_questions = []
window_width = 1200
window_height = 782
window_center = int(window_width/2)
dmv_data = open("dmv_data.txt", "r")
dmv_lines = dmv_data.readlines()
correct_data = open("correct_answers.txt", "r")
cl = correct_data.readlines()
correct_lines = []
for sub in cl:
    correct_lines.append(sub.replace("\n", ""))
qs_value = 0
as_value = 1
q = 1
a = 1
correct_counter = 0
wrong_counter = 0
location_list = []

line_count = 0.0
for line in dmv_lines:
    line_count += 1
question_count = line_count / 5
qs_value = 0
q = 1
while q < question_selector:
    qs_value = qs_value + 5
    q = q + 1
as_value = 1
a = 1
while a < question_selector:
    as_value = as_value + 2
    a = a + 1

da = 0
if question_limit > question_count:
    question_limit = int(question_count)

sq = []
while da < question_count:
    sq.append(da)
    da += 1
random.shuffle(sq)

group_dmv_data = []
g = 0
gdd_line_start = 0
gdd_line_end = 5
while g < question_count:
    group_dmv_data.append(dmv_lines[gdd_line_start:gdd_line_end])
    gdd_line_start = gdd_line_start + 5
    gdd_line_end = gdd_line_end + 5
    g += 1

group_answer_data = []
da = 0
gad_line_start = 0
gad_line_end = 2
while da < question_count:
    group_answer_data.append(correct_lines[gad_line_start:gad_line_end])
    gad_line_start = gad_line_start + 2
    gad_line_end = gad_line_end + 2
    da += 1

correct_answer = ""
correct_bool = False
answer_string = ""
wrong_pixmap_width = 6969
wrong_pixmap_height = 0
right_pixmap_width = 6969
right_pixmap_height = 6969
clickable_butt = True
submittable = False


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(program_title)
        MainWindow.setFixedSize(window_width, window_height)
        wrong_pixmap = QPixmap('wrong.png')
        wrong_pixmap = wrong_pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        right_pixmap = QPixmap('right.png')
        right_pixmap = right_pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.border = QtWidgets.QLabel(self.centralwidget)
        self.border.setGeometry(QtCore.QRect(100, 6969, 1001, 451))
        self.border.setStyleSheet(f"border :10px solid {primary_color};")
        self.border.setText("")
        self.border.setObjectName("border")
        self.topbar = QtWidgets.QLabel(self.centralwidget)
        self.topbar.setGeometry(QtCore.QRect(0, 0, 1201, 71))
        self.topbar.setStyleSheet(f"border :100px solid {primary_color};")
        self.topbar.setText("")
        self.topbar.setObjectName("topbar")
        self.top_label = self.create_label("top_label", self.centralwidget, QtCore.QRect(0, 5, 1201, 61), 40, False, True, 50, "text-align: center;", QtCore.Qt.AlignCenter)
        self.initial_label = self.create_label("question_label", self.centralwidget, QtCore.QRect(140, 6969, 1000, 200), 42, True, False, 75, "", QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(430, 600, 341, 71))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.start_button.setFont(font)
        self.start_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.start_button.setStyleSheet(f"background-color: {primary_color}; color:white; border-radius: 7px;")
        self.start_button.setObjectName("start_button")
        self.start_button.clicked.connect(self.add_questionui)
        self.question_label = self.create_label("question_label", self.centralwidget, QtCore.QRect(140, 6969, 1000, 200), 22, True, False, 75, "", QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.button_A = self.create_button("button_A", lambda: self.select_answer('A'), self.centralwidget, QtCore.QRect(160, 6969, 800, 21), QtCore.QSize(0, 0), 18, "width: 55px;\nheight: 55px;", QtCore.QSize(100, 100), False)
        self.button_B = self.create_button("button_B", lambda: self.select_answer('B'), self.centralwidget, QtCore.QRect(160, 6969, 800, 21), QtCore.QSize(0, 0), 18, "width: 55px;\nheight: 55px;", QtCore.QSize(100, 100), False)
        self.button_C = self.create_button("button_C", lambda: self.select_answer('C'), self.centralwidget, QtCore.QRect(160, 6969, 800, 21), QtCore.QSize(0, 0), 18, "width: 55px;\nheight: 55px;", QtCore.QSize(100, 100), False)
        if four_options_enabled == True:
            self.button_D = self.create_button("button_D", lambda: self.select_answer('D'), self.centralwidget, QtCore.QRect(160, 6969, 800, 21), QtCore.QSize(0, 0), 18, "width: 55px;\nheight: 55px;", QtCore.QSize(100, 100), False)
        self.button_noinput = QtWidgets.QRadioButton(self.centralwidget)
        self.button_noinput.setGeometry(QtCore.QRect(160, 6969, 361, 21))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.button_noinput.setFont(font)
        self.button_noinput.setStyleSheet("width: 55px;\n"
                                    "height: 55px;")
        self.button_noinput.setIconSize(QtCore.QSize(100, 100))
        self.button_noinput.setChecked(True)
        self.button_noinput.setObjectName("no_input")

        self.right_img = QtWidgets.QLabel(self.centralwidget)
        self.right_pixmap = QPixmap('right.png')
        self.right_img.setPixmap(self.right_pixmap)
        self.right_img.setGeometry(QtCore.QRect(right_pixmap_width, right_pixmap_height, 100, 100))
        self.right_img.setPixmap(right_pixmap)
        self.right_img.resize(right_pixmap.width(), right_pixmap.height())
        self.right_img.setObjectName("right_img")

        self.wrong_img = QtWidgets.QLabel(self.centralwidget)
        self.wrong_pixmap = QPixmap('wrong.png')
        self.wrong_img.setPixmap(self.wrong_pixmap)
        self.wrong_img.setGeometry(QtCore.QRect(wrong_pixmap_width, wrong_pixmap_height, 100, 100))
        self.wrong_img.setPixmap(wrong_pixmap)
        self.wrong_img.resize(wrong_pixmap.width(), wrong_pixmap.height())
        self.wrong_img.setObjectName("wrong_img")
        self.submit_button = self.create_submit_button("submit_button", QtCore.QRect(430, 6969, 341, 71), self.submit_click, self.centralwidget, primary_color)
        self.submit_button_2 = self.create_submit_button("submit_button_2", QtCore.QRect(50, 6969, 341, 71), self.skip_click, self.centralwidget, primary_color)
        self.submit_button_3 = self.create_submit_button("submit_button_3", QtCore.QRect(810, 6969, 341, 71), self.quitlmao, self.centralwidget, primary_color)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.hide()
        self.counter = QtWidgets.QLabel(self.centralwidget)
        self.counter.setGeometry(QtCore.QRect(145, 650, 921, 101))
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.counter.setFont(font)
        self.counter.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.counter.setObjectName("counter")
        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.initial_layout()

    def create_button(self, name, select_method, widget, rect, size, font_size, style, icon_size, checked):
        button = QtWidgets.QRadioButton(widget)
        button.setGeometry(rect)
        button.setSizeIncrement(size)
        font = QtGui.QFont()
        font.setPointSize(font_size)
        button.setFont(font)
        button.setLayoutDirection(QtCore.Qt.LeftToRight)
        button.setStyleSheet(style)
        button.setIconSize(icon_size)
        button.setChecked(checked)
        button.setObjectName(name)
        button.clicked.connect(select_method)
        return button

    def create_label(self, name, widget, rect, font_size, bold, italic, weight, style, alignment):
        label = QtWidgets.QLabel(widget)
        label.setGeometry(rect)
        font = QtGui.QFont()
        font.setPointSize(font_size)
        font.setBold(bold)
        font.setItalic(italic)
        font.setWeight(weight)
        label.setFont(font)
        label.setStyleSheet(style)
        label.setAlignment(alignment)
        label.setObjectName(name)
        return label

    def create_submit_button(self, name, geometry, click_action, centralwidget, primary_color):
        button = QtWidgets.QPushButton(centralwidget)
        button.setGeometry(geometry)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        button.setFont(font)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(f"background-color: {primary_color}; color:white; border-radius: 7px;")
        button.setObjectName(name)
        button.clicked.connect(click_action)
        return button

    def quitlmao(self):
        if clickable_butt == True:
            self.close()

    def select_answer(self, selected_option):
        global clickable_butt, correct_bool, wrong_pixmap_height, submittable, correct_answer
        if clickable_butt:
            wrong_pixmap_height = location_list[ord(selected_option) - ord('A')] - 40
            self.wrong_img.setGeometry(QtCore.QRect(wrong_pixmap_width, wrong_pixmap_height, 100, 100))
            correct_answer = selected_option
            correct_bool = (correct_answer == group_answer_data[sq[question_selector - 1]][1])
            submittable = True

    def submit_click(self):
        global clickable_butt
        global submittable
        if clickable_butt == True and submittable == True:
            global answer_string
            global question_selector
            global correct_bool
            global correct_counter
            global performance_ratio
            if correct_bool == True:
                self.counter.setText(f"<html><head/><body><p align=\"center\">{answer_string}</p></body></html>")
                correct_counter = correct_counter + 1
                performance_ratio = float(correct_counter) / float(question_selector)
                if question_selector != question_limit:
                    question_selector = question_selector + 1
                    self.randomize_choice_location()
                    self.question_label.setText(f"    {group_dmv_data[sq[question_selector - 1]][0]}")
                    self.button_A.setText(f"    {group_dmv_data[sq[question_selector - 1]][1]}")
                    self.button_B.setText(f"    {group_dmv_data[sq[question_selector - 1]][2]}")
                    self.button_C.setText(f"    {group_dmv_data[sq[question_selector - 1]][3]}")
                    if four_options_enabled == True:
                        self.button_D.setText(f"    {group_dmv_data[sq[question_selector - 1]][4]}")
                    self.button_noinput.setChecked(True)
                    correct_bool = False
                    submittable = False
                else:
                    self.remove_questionui()
                    self.initial_label.setText(f"<html><head/><body><p align=\"center\">{success_message}: {correct_counter}/{question_limit}</p></body></html>")
                    self.end_ui()
            else:
                self.counter.setText(f"<html><head/><body><p align=\"center\">{answer_string}</p></body></html>")
                clickable_butt = False
                self.button_noinput.setChecked(True)
                self.wrong_img.setGeometry(QtCore.QRect(144, wrong_pixmap_height, 100, 100))
                if group_answer_data[sq[question_selector - 1]][1] == "A":
                    right_pixmap_width = 144
                    right_pixmap_height = location_list[0] - 40
                    self.right_img.setGeometry(QtCore.QRect(right_pixmap_width, right_pixmap_height, 100, 100))

                elif group_answer_data[sq[question_selector - 1]][1] == "B":
                    right_pixmap_width = 144
                    right_pixmap_height = location_list[1] - 40
                    self.right_img.setGeometry(QtCore.QRect(right_pixmap_width, right_pixmap_height, 100, 100))

                elif group_answer_data[sq[question_selector - 1]][1] == "C":
                    right_pixmap_width = 144
                    right_pixmap_height = location_list[2] - 40
                    self.right_img.setGeometry(QtCore.QRect(right_pixmap_width, right_pixmap_height, 100, 100))
                if four_options_enabled == True:
                    if group_answer_data[sq[question_selector - 1]][1] == "D":
                        right_pixmap_width = 144
                        right_pixmap_height = location_list[3] - 40
                        self.right_img.setGeometry(QtCore.QRect(right_pixmap_width, right_pixmap_height, 100, 100))
                self.timer=QTimer()
                self.timer.setInterval(100)
                self.timer.timeout.connect(self.timercounter)
                self.timer.start()
                self.timecount_value = 0

    def randomize_choice_location(self):
        global location_list
        location_list = [220, 270, 320]
        if four_options_enabled == True:
            location_list.append(370)
        random.shuffle(location_list)
        self.button_A.setGeometry(QtCore.QRect(160, location_list[0], 800, 21))
        self.button_B.setGeometry(QtCore.QRect(160, location_list[1], 800, 21))
        self.button_C.setGeometry(QtCore.QRect(160, location_list[2], 800, 21))
        if four_options_enabled == True:
            self.button_D.setGeometry(QtCore.QRect(160, location_list[3], 800, 21))

    def timercounter(self):
        self.timecount_value = self.timecount_value + 1
        self.button_noinput.setChecked(True)
        if self.timecount_value == incorrect_display_duration:
            self.timer.stop()
            global question_selector
            global clickable_butt
            global wrong_counter
            global submittable
            self.wrong_img.setGeometry(QtCore.QRect(6969, 6969, 100, 100))
            self.right_img.setGeometry(QtCore.QRect(6969, 6969, 100, 100))
            wrong_counter = wrong_counter + 1
            performance_ratio = float(wrong_counter) / float(math.ceil(question_limit))
            if question_selector != question_limit and performance_ratio < passing_score_threshold:
                question_selector = question_selector + 1
                self.randomize_choice_location()
                self.question_label.setText(f"    {group_dmv_data[sq[question_selector - 1]][0]}")
                self.button_A.setText(f"    {group_dmv_data[sq[question_selector - 1]][1]}")
                self.button_B.setText(f"    {group_dmv_data[sq[question_selector - 1]][2]}")
                self.button_C.setText(f"    {group_dmv_data[sq[question_selector - 1]][3]}")
                if four_options_enabled == True:
                    self.button_D.setText(f"    {group_dmv_data[sq[question_selector - 1]][4]}")
                self.button_noinput.setChecked(True)
                clickable_butt = True
                submittable = False
            elif performance_ratio > passing_score_threshold:
                self.remove_questionui()
                self.initial_label.setText(f"<html><head/><body><p align=\"center\">{failure_message}</p></body></html>")
                self.end_ui()
                clickable_butt = True
            else:
                self.remove_questionui()
                self.initial_label.setText(f"<html><head/><body><p align=\"center\">"
                                           f"{success_message}: {correct_counter}/{question_limit}</p></body></html>")
                self.end_ui()
                clickable_butt = True

    def skip_click(self):
        global question_selector
        if clickable_butt:
            self.counter.setText(f"<html><head/><body><p align=\"center\">{answer_string}</p></body></html>")
            skipped_questions.append(question_selector)
            question_selector = question_selector + 1
            self.question_label.setText(f"    {group_dmv_data[sq[question_selector - 1]][0]}")
            self.button_A.setText(f"    {group_dmv_data[sq[question_selector - 1]][1]}")
            self.button_B.setText(f"    {group_dmv_data[sq[question_selector - 1]][2]}")
            self.button_C.setText(f"    {group_dmv_data[sq[question_selector - 1]][3]}")
            if four_options_enabled == True:
                self.button_D.setText(f"    {group_dmv_data[sq[question_selector - 1]][4]}")
            self.button_noinput.setChecked(True)

    def initial_layout(self):
        self.initial_label.setGeometry(QtCore.QRect(140, 200, 921, 101))

    def add_questionui(self):
        global location_list
        self.randomize_choice_location()
        self.counter.setGeometry(QtCore.QRect(145, 650, 921, 101))
        self.border.setGeometry(QtCore.QRect(100, 110, 1001, 451))
        self.question_label.setGeometry(QtCore.QRect(140, 150, 921, 101))
        self.submit_button.setGeometry(QtCore.QRect(430, 440, 341, 71))
        self.submit_button_2.setGeometry(QtCore.QRect(6969, 610, 341, 71))
        self.submit_button_3.setGeometry(QtCore.QRect(810, 610, 341, 71))
        self.initial_label.setGeometry(QtCore.QRect(420, 6969, 341, 71))
        self.start_button.setGeometry(QtCore.QRect(420, 6969, 341, 71))

    def remove_questionui(self):
        self.button_A.setGeometry(QtCore.QRect(160, 6969, 361, 21))
        self.button_B.setGeometry(QtCore.QRect(160, 6969, 361, 21))
        self.button_C.setGeometry(QtCore.QRect(160, 6969, 361, 21))
        if four_options_enabled == True:
            self.button_D.setGeometry(QtCore.QRect(160, 6969, 361, 21))
        self.counter.setGeometry(QtCore.QRect(145, 6969, 921, 101))
        self.border.setGeometry(QtCore.QRect(100, 6969, 1001, 451))
        self.question_label.setGeometry(QtCore.QRect(140, 6969, 921, 101))
        self.submit_button.setGeometry(QtCore.QRect(430, 6969, 341, 71))
        self.submit_button_2.setGeometry(QtCore.QRect(50, 6969, 341, 71))

    def end_ui(self):
        self.initial_label.setGeometry(QtCore.QRect(130, 200, 921, 101))
        self.submit_button_3.setGeometry(QtCore.QRect(430, 610, 341, 71))

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", program_title))
        self.top_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" "
                                                        "color:#ffffff;"f"\">{program_title}</span></p></body></html>"))
        self.question_label.setText(_translate("MainWindow", f"{group_dmv_data[sq[question_selector - 1]][0]}"))
        self.initial_label.setText(_translate("MainWindow", f"<html><head/><body><p align=\"center\">"
                                                            f"{initial_message}</p></body></html>"))
        self.counter.setText(_translate("MainWindow", f"<html><head/><body><p align=\"center\">"
                                                      f"{answer_string}</p></body></html>"))
        self.button_A.setText(_translate("MainWindow", f"    {group_dmv_data[sq[question_selector - 1]][1]}"))
        self.button_B.setText(_translate("MainWindow", f"    {group_dmv_data[sq[question_selector - 1]][2]}"))
        self.button_C.setText(_translate("MainWindow", f"    {group_dmv_data[sq[question_selector - 1]][3]}"))
        if four_options_enabled == True:
            self.button_D.setText(_translate("MainWindow", f"    {group_dmv_data[sq[question_selector - 1]][4]}"))
        self.submit_button.setText(_translate("MainWindow", "Submit"))
        self.submit_button_2.setText(_translate("MainWindow", "Skip Question"))
        self.submit_button_3.setText(_translate("MainWindow", "Quit Test"))
        self.start_button.setText(_translate("MainWindow", "Start Test"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    app.setWindowIcon(QIcon('permittest_logo.png'))
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
