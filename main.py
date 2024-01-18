from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon, QFont, QCursor
from PyQt5.QtCore import QRect, QSize, QTimer, Qt
import math
import random

initial_message = "You will take this test"
success_message = "Here is how well you did"
failure_message = "You have failed"
question_limit = 10
passing_score_threshold = 0.69
incorrect_display_duration = 69
program_title = "Permit Test Simulator"
primary_color = "#2c4391"
text_color = "#ffffff"
four_options_enabled = False

question_selector = 1
skipped_questions = []
window_width = 1200
window_height = 782
window_center = int(window_width / 2)

dmv_data = open("data/question_data.txt", "r")
dmv_lines = dmv_data.readlines()
dmv_data.close()

correct_data = open("data/correct_answers.txt", "r")
cl = correct_data.readlines()
correct_data.close()

correct_lines = [sub.strip() for sub in cl]

correct_counter = 0
wrong_counter = 0
location_list = []

question_count = len(dmv_lines) / 5
if question_limit > question_count:
    question_limit = int(question_count)

shuffle_question = list(range(int(question_count)))
random.shuffle(shuffle_question)

group_dmv_data = [dmv_lines[i:i + 5] for i in range(0, len(dmv_lines), 5)]
group_answer_data = [correct_lines[i:i + 2] for i in range(0, len(correct_lines), 2)]

correct_answer = ""
correct_bool = False
answer_string = ""
wrong_pixmap_width = 6969
wrong_pixmap_height = 0
right_pixmap_width = 6969
right_pixmap_height = 6969
is_clickable = True
is_submittable = False

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(program_title)
        MainWindow.setFixedSize(window_width, window_height)
        wrong_pixmap = QPixmap('images/wrong.png')
        wrong_pixmap = wrong_pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        right_pixmap = QPixmap('images/right.png')
        right_pixmap = right_pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.border = self.create_bar_ui(self.centralwidget, QtCore.QRect(100, 6969, 1001, 451), f"border :10px solid {primary_color};", "border")
        self.topbar = self.create_bar_ui(self.centralwidget, QtCore.QRect(0, 0, 1201, 71), f"border :100px solid {primary_color};", "topbar")
        self.top_label = self.create_label("top_label", self.centralwidget, QtCore.QRect(0, 5, 1201, 61), 40, False, True, 50, "text-align: center;", QtCore.Qt.AlignCenter)
        self.initial_label = self.create_label("question_label", self.centralwidget, QtCore.QRect(140, 6969, 1000, 200), 42, True, False, 75, "", QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.start_button = self.create_start_button("start_button", QtCore.QRect(430, 600, 341, 71), self.add_questionui, self.centralwidget, primary_color)
        self.question_label = self.create_label("question_label", self.centralwidget, QtCore.QRect(140, 6969, 1000, 200), 22, True, False, 75, "", QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.button_A = self.create_button("button_A", lambda: self.select_answer('A'), self.centralwidget, QtCore.QRect(160, 6969, 800, 21), QtCore.QSize(0, 0), 18, "width: 55px;\nheight: 55px;", QtCore.QSize(100, 100), False)
        self.button_B = self.create_button("button_B", lambda: self.select_answer('B'), self.centralwidget, QtCore.QRect(160, 6969, 800, 21), QtCore.QSize(0, 0), 18, "width: 55px;\nheight: 55px;", QtCore.QSize(100, 100), False)
        self.button_C = self.create_button("button_C", lambda: self.select_answer('C'), self.centralwidget, QtCore.QRect(160, 6969, 800, 21), QtCore.QSize(0, 0), 18, "width: 55px;\nheight: 55px;", QtCore.QSize(100, 100), False)
        if four_options_enabled == True:
            self.button_D = self.create_button("button_D", lambda: self.select_answer('D'), self.centralwidget, QtCore.QRect(160, 6969, 800, 21), QtCore.QSize(0, 0), 18, "width: 55px;\nheight: 55px;", QtCore.QSize(100, 100), False)
        self.button_noinput = self.create_button("no_input", None, self.centralwidget, QtCore.QRect(160, 6969, 361, 21), QtCore.QSize(100, 100), 17, "width: 55px;\nheight: 55px;", QtCore.QSize(100, 100), True)
        self.right_img = self.create_img_label('images/right.png', "right_img", right_pixmap_width, right_pixmap_height)
        self.wrong_img = self.create_img_label('images/wrong.png', "wrong_img", wrong_pixmap_width, wrong_pixmap_height)
        self.submit_button = self.create_submit_button("submit_button", QtCore.QRect(430, 6969, 341, 71), self.submit_click, self.centralwidget, primary_color)
        self.submit_button_2 = self.create_submit_button("submit_button_2", QtCore.QRect(50, 6969, 341, 71), self.skip_click, self.centralwidget, primary_color)
        self.submit_button_3 = self.create_submit_button("submit_button_3", QtCore.QRect(810, 6969, 341, 71), self.quit_program, self.centralwidget, primary_color)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.hide()
        self.counter = self.create_label("counter", self.centralwidget, QtCore.QRect(145, 650, 921, 101), 22, True, False, 75, "", QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.initial_layout()

    def create_bar_ui(self, widget, geometry, style, object_name):
        border = QtWidgets.QLabel(widget)
        border.setGeometry(geometry)
        border.setStyleSheet(style)
        border.setText("")
        border.setObjectName(object_name)
        return border

    def create_img_label(self, img_file, object_name, pixmap_width, pixmap_height):
        img_label = QtWidgets.QLabel(self.centralwidget)
        pixmap = QPixmap(img_file)
        img_label.setPixmap(pixmap)
        img_label.setGeometry(QtCore.QRect(pixmap_width, pixmap_height, 100, 100))
        img_label.setPixmap(pixmap)
        img_label.resize(pixmap.width(), pixmap.height())
        img_label.setObjectName(object_name)
        return img_label

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
        if select_method is not None:
            button.clicked.connect(select_method)
        return button

    def create_start_button(self, name, geometry, click_action, centralwidget, primary_color):
        button = QtWidgets.QPushButton(centralwidget)
        button.setGeometry(geometry)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        button.setFont(font)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(f"background-color: {primary_color}; color:{text_color}; border-radius: 7px;")
        button.setObjectName(name)
        button.clicked.connect(click_action)
        return button

    def create_submit_button(self, name, geometry, click_action, centralwidget, primary_color):
        button = QtWidgets.QPushButton(centralwidget)
        button.setGeometry(geometry)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        button.setFont(font)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(f"background-color: {primary_color}; color:{text_color}; border-radius: 7px;")
        button.setObjectName(name)
        button.clicked.connect(click_action)
        return button

    def quit_program(self):
        if is_clickable == True:
            self.close()

    def select_answer(self, selected_option):
        global is_clickable, correct_bool, wrong_pixmap_height, is_submittable, correct_answer
        if is_clickable:
            wrong_pixmap_height = location_list[ord(selected_option) - ord('A')] - 40
            self.wrong_img.setGeometry(QtCore.QRect(wrong_pixmap_width, wrong_pixmap_height, 100, 100))
            correct_answer = selected_option
            correct_bool = (correct_answer == group_answer_data[shuffle_question[question_selector - 1]][1])
            is_submittable = True

    def submit_click(self):
        global is_clickable
        global is_submittable
        if is_clickable == True and is_submittable == True:
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
                    self.question_label.setText(f"    {group_dmv_data[shuffle_question[question_selector - 1]][0]}")
                    self.button_A.setText(f"    {group_dmv_data[shuffle_question[question_selector - 1]][1]}")
                    self.button_B.setText(f"    {group_dmv_data[shuffle_question[question_selector - 1]][2]}")
                    self.button_C.setText(f"    {group_dmv_data[shuffle_question[question_selector - 1]][3]}")
                    if four_options_enabled == True:
                        self.button_D.setText(f"    {group_dmv_data[shuffle_question[question_selector - 1]][4]}")
                    self.button_noinput.setChecked(True)
                    correct_bool = False
                    is_submittable = False
                else:
                    self.remove_questionui()
                    self.initial_label.setText(f"<html><head/><body><p align=\"center\">{success_message}: {correct_counter}/{question_limit}</p></body></html>")
                    self.end_ui()
            else:
                self.counter.setText(f"<html><head/><body><p align=\"center\">{answer_string}</p></body></html>")
                is_clickable = False
                self.button_noinput.setChecked(True)
                self.wrong_img.setGeometry(QtCore.QRect(134, wrong_pixmap_height, 100, 100))
                if group_answer_data[shuffle_question[question_selector - 1]][1] == "A":
                    right_pixmap_width = 134
                    right_pixmap_height = location_list[0] - 40
                    self.right_img.setGeometry(QtCore.QRect(right_pixmap_width, right_pixmap_height, 100, 100))

                elif group_answer_data[shuffle_question[question_selector - 1]][1] == "B":
                    right_pixmap_width = 134
                    right_pixmap_height = location_list[1] - 40
                    self.right_img.setGeometry(QtCore.QRect(right_pixmap_width, right_pixmap_height, 100, 100))

                elif group_answer_data[shuffle_question[question_selector - 1]][1] == "C":
                    right_pixmap_width = 134
                    right_pixmap_height = location_list[2] - 40
                    self.right_img.setGeometry(QtCore.QRect(right_pixmap_width, right_pixmap_height, 100, 100))
                if four_options_enabled == True:
                    if group_answer_data[shuffle_question[question_selector - 1]][1] == "D":
                        right_pixmap_width = 134
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
            global is_clickable
            global wrong_counter
            global is_submittable
            self.wrong_img.setGeometry(QtCore.QRect(6969, 6969, 100, 100))
            self.right_img.setGeometry(QtCore.QRect(6969, 6969, 100, 100))
            wrong_counter = wrong_counter + 1
            performance_ratio = float(wrong_counter) / float(math.ceil(question_limit))
            if question_selector != question_limit and performance_ratio < passing_score_threshold:
                question_selector = question_selector + 1
                self.randomize_choice_location()
                self.question_label.setText(f"    {group_dmv_data[shuffle_question[question_selector - 1]][0]}")
                self.button_A.setText(f"    {group_dmv_data[shuffle_question[question_selector - 1]][1]}")
                self.button_B.setText(f"    {group_dmv_data[shuffle_question[question_selector - 1]][2]}")
                self.button_C.setText(f"    {group_dmv_data[shuffle_question[question_selector - 1]][3]}")
                if four_options_enabled == True:
                    self.button_D.setText(f"    {group_dmv_data[shuffle_question[question_selector - 1]][4]}")
                self.button_noinput.setChecked(True)
                is_clickable = True
                is_submittable = False
            elif performance_ratio > passing_score_threshold:
                self.remove_questionui()
                self.initial_label.setText(f"<html><head/><body><p align=\"center\">{failure_message}</p></body></html>")
                self.end_ui()
                is_clickable = True
            else:
                self.remove_questionui()
                self.initial_label.setText(f"<html><head/><body><p align=\"center\">"
                                           f"{success_message}: {correct_counter}/{question_limit}</p></body></html>")
                self.end_ui()
                is_clickable = True

    def skip_click(self):
        global question_selector
        if is_clickable:
            self.counter.setText(f"<html><head/><body><p align=\"center\">{answer_string}</p></body></html>")
            skipped_questions.append(question_selector)
            question_selector = question_selector + 1
            self.question_label.setText(f"    {group_dmv_data[shuffle_question[question_selector - 1]][0]}")
            self.button_A.setText(f"    {group_dmv_data[shuffle_question[question_selector - 1]][1]}")
            self.button_B.setText(f"    {group_dmv_data[shuffle_question[question_selector - 1]][2]}")
            self.button_C.setText(f"    {group_dmv_data[shuffle_question[question_selector - 1]][3]}")
            if four_options_enabled == True:
                self.button_D.setText(f"    {group_dmv_data[shuffle_question[question_selector - 1]][4]}")
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
                                                        f"color:{text_color};"f"\">{program_title}</span></p></body></html>"))
        self.question_label.setText(_translate("MainWindow", f"{group_dmv_data[shuffle_question[question_selector - 1]][0]}"))
        self.initial_label.setText(_translate("MainWindow", f"<html><head/><body><p align=\"center\">"
                                                            f"{initial_message}</p></body></html>"))
        self.counter.setText(_translate("MainWindow", f"<html><head/><body><p align=\"center\">"
                                                      f"{answer_string}</p></body></html>"))
        self.button_A.setText(_translate("MainWindow", f"    {group_dmv_data[shuffle_question[question_selector - 1]][1]}"))
        self.button_B.setText(_translate("MainWindow", f"    {group_dmv_data[shuffle_question[question_selector - 1]][2]}"))
        self.button_C.setText(_translate("MainWindow", f"    {group_dmv_data[shuffle_question[question_selector - 1]][3]}"))
        if four_options_enabled == True:
            self.button_D.setText(_translate("MainWindow", f"    {group_dmv_data[shuffle_question[question_selector - 1]][4]}"))
        self.submit_button.setText(_translate("MainWindow", "Submit"))
        self.submit_button_2.setText(_translate("MainWindow", "Skip Question"))
        self.submit_button_3.setText(_translate("MainWindow", "Quit Test"))
        self.start_button.setText(_translate("MainWindow", "Start Test"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    app.setWindowIcon(QIcon('images/permittest_logo.png'))
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
