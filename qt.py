from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QFrame, QPushButton, QMessageBox, QLineEdit, QVBoxLayout, QListWidget,QTableWidget, QTableWidgetItem,QSpinBox,QSlider
from PySide6.QtGui import QFont
import sys

from PySide6.QtCore import Qt

class SeparatorLine(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class BackgroundFrame(QFrame):
    def __init__(self, parent=None, color="#d9d9d9", width=100, height=40):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {color};")
        self.setFixedSize(width, height)


class CenteredLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Установка размеров и цвета фона для главного окна
        self.setGeometry(0, 0, 1920, 1080)
        self.setStyleSheet("background-color: #d9d9d9;")

        # Создание дочернего виджета
        self.child_widget = QWidget(self)
        self.child_widget.setGeometry(1176, 0, 744, 1080)  # Положение справа от главного окна и расширение до края
        self.child_widget.setStyleSheet("background-color: #ffffff;")

        self.sputnik_label = QLabel(
            "Sputnik Panel", self.child_widget
        )
        self.sputnik_label.setGeometry(
            90, -500, 494, 1080
        )  # Координаты и размеры надписи внутри дочернего виджета
        self.sputnik_label.setStyleSheet(
            "background-color: transparent;"
        )  # Прозрачный фон
        self.sputnik_label.setFont(QFont("Arial", 30))

        # Добавление разделительной линии
        self.line = QFrame(self.child_widget)
        self.line.setGeometry(0, 70, 744, 1)
        self.line.setStyleSheet("background-color: black;")

        # Создание списка для спутников
        self.satellite_list = QListWidget(self.child_widget)
        self.satellite_list.setGeometry(500, 130, 200, 700)
        self.satellite_list.setStyleSheet("background-color: #ffffff; border: 1px solid black;")
        self.satellite_list.setFont(QFont("Arial", 14))

        # Создание заднего фона за счетчиком
        self.background_frame = BackgroundFrame(
            self.child_widget, width=40, height=40
        )
        self.background_frame.move(230, 130)

        # Создание надписи "Large semi-axis"
        self.large_semi_axis_label = QLabel(
            "Large semi-axis:", self.child_widget
        )
        self.large_semi_axis_label.setGeometry(
            20, 130, 200, 40
        )  # Координаты и размеры надписи
        self.large_semi_axis_label.setStyleSheet(
            "background-color: transparent;"
        )
        self.large_semi_axis_label.setFont(QFont("Arial", 16))

        # Создание счетчика
        self.counter = 0
        self.saved_counter = 0  # Переменная для хранения первого счетчика
        self.counter_spinbox = QSpinBox(self.child_widget)  # Используем QSpinBox
        self.counter_spinbox.setGeometry(
            230, 130, 40, 40
        )  # Координаты и размеры счетчика
        self.counter_spinbox.setButtonSymbols(QSpinBox.NoButtons)
        self.counter_spinbox.setStyleSheet("background-color: transparent;")
        self.counter_spinbox.setFont(QFont("Arial", 10))
        self.counter_spinbox.setRange(0, 1000)  # Устанавливаем диапазон значений
        self.counter_spinbox.setValue(self.counter)
        self.counter_spinbox.valueChanged.connect(self.update_counter)

        # Создание поля для ввода названия спутника
        self.satellite_name_input = QLineEdit(self.child_widget)
        self.satellite_name_input.setGeometry(20, 80, 350, 35)
        self.satellite_name_input.setPlaceholderText("Введите название спутника")
        

        # Переменная для подсчета номера спутника
        self.counterFor = 0

        # Создание кнопки "+1"
        self.plus_one_button = QPushButton("+1", self.child_widget)
        self.plus_one_button.setGeometry(280, 130, 40, 40)
        self.plus_one_button.setStyleSheet(
            "background-color: #d9d9d9; color: black; border-radius: 5px;"
        )
        self.plus_one_button.setFont(QFont("Arial", 16))
        self.plus_one_button.clicked.connect(self.increment_spinbox_value)
        self.plus_one_button.setFixedSize(40, 40)

        # Создание кнопки "-1"
        self.minus_one_button = QPushButton("-1", self.child_widget)
        self.minus_one_button.setGeometry(330, 130, 40, 40)
        self.minus_one_button.setStyleSheet(
            "background-color: #d9d9d9; color: black; border-radius: 5px;"
        )
        self.minus_one_button.setFont(QFont("Arial", 16))
        self.minus_one_button.clicked.connect(self.decrement_spinbox_value)
        self.minus_one_button.setFixedSize(40, 40)


        # Создание кнопки "Add"
        self.yes_button = QPushButton("Добавить", self.child_widget)
        self.yes_button.setGeometry(80, 870, 300, 40)
        self.yes_button.setStyleSheet(
            "background-color: #4CAF50; color: white; border-radius: 5px;"
        )
        self.yes_button.setFont(QFont("Arial", 16))
        self.yes_button.clicked.connect(self.add_satellite)

        
        
        self.child_widget1 = QWidget(self)
        self.child_widget1.setGeometry(1000, 0, 180, 1080)  # Положение справа от главного окна и расширение до края
        self.child_widget1.setStyleSheet("background-color: #C0C0C0;")
        self.satellite_table = QTableWidget(self.child_widget1)
        self.satellite_table.setStyleSheet("QTableWidget {border: none;}")
        self.satellite_table.setGeometry(30, 10, 180, 1080)  # Положение и размеры таблицы
        self.satellite_table.setColumnCount(1)  # Установка количества столбцов
        self.satellite_table.setHorizontalHeaderLabels(["Name"])
        self.satellite_table.cellDoubleClicked.connect(self.showCellInfo)
        
        
        # Создание надписи "Eccentricity:"
        self.eccentricity_label = QLabel(
            "Eccentricity:", self.child_widget
        )
        self.eccentricity_label.setGeometry(20, 180, 200, 40)  # Координаты и размеры надписи
        self.eccentricity_label.setStyleSheet(
            "background-color: transparent;"
        )
        self.eccentricity_label.setFont(QFont("Arial", 16))

        # Создание поля для отображения значения эксцентриситета
        self.eccentricity_line_edit = QLineEdit(self.child_widget)
        self.eccentricity_line_edit.setGeometry(170, 180, 40, 40)
        self.eccentricity_line_edit.setText("0")
        self.eccentricity_line_edit.setAlignment(Qt.AlignCenter)
        self.eccentricity_line_edit.setReadOnly(False)  # Устанавливаем поле редактируемым
        self.eccentricity_line_edit.setStyleSheet("background-color: #d9d9d9;")  # Установка цвета фона
        self.eccentricity_line_edit.setFont(QFont("Arial", 8))
        self.eccentricity_line_edit.textChanged.connect(self.update_eccentricity_from_line_edit)

        self.eccentricity_value = 0  # Переменная для хранения значения эксцентриситета
        self.eccentricity_counter = 0
                # Создание горизонтального ползунка для эксцентриситета
        self.eccentricity_slider = QSlider(Qt.Horizontal, self.child_widget)
        self.eccentricity_slider.setGeometry(241, 180, 100, 40)
        self.eccentricity_slider.setMinimum(0)
        self.eccentricity_slider.setMaximum(100)
        self.eccentricity_slider.setValue(0)
        self.eccentricity_slider.setTickInterval(1)  # Установка интервала меток
        self.eccentricity_slider.setTickPosition(QSlider.TicksBothSides)  # Установка позиции меток
        self.eccentricity_slider.setStyleSheet(
            "QSlider::groove:horizontal {"
            "    border: none;"
            "    height: 10px;"  # Высота ползунка
            "    background-color: #d9d9d9;"  # Цвет фона
            "}"
            "QSlider::handle:horizontal {"
            "    background-color: #4CAF50;"  # Цвет ползунка
            "    border: 1px solid #4CAF50;"  # Обводка ползунка
            "    width: 18px;"  # Ширина ползунка
            "    margin: -5px 0;"  # Положение ползунка
            "    border-radius: 9px;"  # Скругление углов ползунка
            "}"
)
        
        self.eccentricity_slider.valueChanged.connect(self.update_eccentricity_from_slider)

        # Создание метки для значения 0 слева от ползунка
        self.eccentricity_min_label = QLabel("0", self.child_widget)
        self.eccentricity_min_label.setGeometry(220, 180, 20, 40)
        self.eccentricity_min_label.setAlignment(Qt.AlignCenter)

        # Создание метки для значения 1 справа от ползунка
        self.eccentricity_max_label = QLabel("1", self.child_widget)
        self.eccentricity_max_label.setGeometry(342, 180, 20, 40)
        self.eccentricity_max_label.setAlignment(Qt.AlignCenter)


        self.parameter1_line_edit, self.parameter1_slider = self.create_slider("Inclination:", 20, 230, self.update_parameter1_from_line_edit, self.update_parameter1_from_slider)
        self.parameter2_line_edit, self.parameter2_slider = self.create_slider("Longitude of the ascending node:", 20, 290, self.update_parameter2_from_line_edit, self.update_parameter2_from_slider)
        self.parameter3_line_edit, self.parameter3_slider = self.create_slider("Argument of the pericenter:", 20, 360, self.update_parameter3_from_line_edit, self.update_parameter3_from_slider)
        self.parameter4_line_edit, self.parameter4_slider = self.create_slider("Mean anomaly:", 20, 430, self.update_parameter4_from_line_edit, self.update_parameter4_from_slider)
        
        

    def create_slider(self, label_text, x, y, line_edit_callback, slider_callback):
        label = QLabel(label_text, self.child_widget)
        label.setGeometry(x, y, 185, 50)
        label.setStyleSheet("background-color: transparent;")
        label.setFont(QFont("Arial", 16))
        label.setWordWrap(True) 
        

        line_edit = QLineEdit(self.child_widget)
        line_edit.setGeometry(x + 195, y, 40, 40)
        line_edit.setText("0")
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(False)
        line_edit.setStyleSheet("background-color: #d9d9d9;")
        line_edit.setFont(QFont("Arial", 8))
        line_edit.textChanged.connect(line_edit_callback)

        slider = QSlider(Qt.Horizontal, self.child_widget)
        slider.setGeometry(x + 260, y, 100, 40)
        slider.setMinimum(0)
        slider.setMaximum(360)
        slider.setValue(0)
        slider.setTickInterval(10)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setStyleSheet(
            "QSlider::groove:horizontal {"
            "    border: none;"
            "    height: 10px;"
            "    background-color: #d9d9d9;"
            "}"
            "QSlider::handle:horizontal {"
            "    background-color: #4CAF50;"
            "    border: 1px solid #4CAF50;"
            "    width: 18px;"
            "    margin: -5px 0;"
            "    border-radius: 9px;"
            "}"
        )
        slider.valueChanged.connect(slider_callback)

        min_label = QLabel("0", self.child_widget)
        min_label.setGeometry(x + 235, y, 20, 40)
        min_label.setAlignment(Qt.AlignCenter)

        max_label = QLabel("360", self.child_widget)
        max_label.setGeometry(x + 360, y, 20, 40)
        max_label.setAlignment(Qt.AlignCenter)

        return line_edit, slider

    def update_parameter1_from_line_edit(self, text):
        try:
            value = float(text)
            if 0 <= value <= 360:
                self.parameter1_slider.setValue(int(value))
                self.inclination_value = value
        except ValueError:
            pass

    def update_parameter1_from_slider(self, value):
        self.parameter1_line_edit.setText(str(value))

    def update_parameter2_from_line_edit(self, text):
        try:
            value = float(text)
            if 0 <= value <= 360:
                self.parameter2_slider.setValue(int(value))
                self.ascending_node_value = value
        except ValueError:
            pass

    def update_parameter2_from_slider(self, value):
        self.parameter2_line_edit.setText(str(value))
        
    def update_parameter3_from_line_edit(self, text):
        try:
            value = float(text)
            if 0 <= value <= 360:
                self.parameter3_slider.setValue(int(value))
                self.pericenter_value = value
        except ValueError:
            pass

    def update_parameter3_from_slider(self, value):
        self.parameter3_line_edit.setText(str(value))
    
    def update_parameter4_from_line_edit(self, text):
        try:
            value = float(text)
            if 0 <= value <= 360:
                self.parameter4_slider.setValue(int(value))
                self.anomaly_value = value
        except ValueError:
            pass

    def update_parameter4_from_slider(self, value):
        self.parameter4_line_edit.setText(str(value))
          
    def update_counter(self, value):
        self.counter = value

    def update_eccentricity_from_line_edit(self, text):
        try:
            value = float(text)
            if 0 <= value <= 1:
                self.eccentricity_slider.setValue(int(value * 100))
                self.eccentricity_value = value  # Обновление значения эксцентриситета
        except ValueError:
            pass

    def update_eccentricity_from_slider(self, value):
        self.eccentricity_line_edit.setText(str(value / 100))
        self.eccentricity_value = value / 100  # Обновление значения эксцентриситета     
          
    def add_satellite(self):
        eccentricity_value=self.eccentricity_value
        inclination_value=self.inclination_value
        ascending_node_value=self.ascending_node_value
        anomaly_value=self.anomaly_value
        pericenter_value=self.pericenter_value
        satellite_name = self.satellite_name_input.text().strip()
        if not satellite_name:
            self.counterFor += 1
            satellite_name = f"Sputnik[{self.counterFor}]"
        self.satellite_list.addItem(f"{satellite_name} - {self.counter_spinbox.value()}")  # Добавление спутника в список
        self.satellite_name_input.setText("")  # Обнуление поля ввода названия спутника
        self.saved_counter = self.counter_spinbox.value()
        self.show_message_box(satellite_name, self.saved_counter,eccentricity_value,inclination_value,ascending_node_value,anomaly_value,pericenter_value)  # Показать сообщение о добавлении спутника
        self.insert_row_to_table(satellite_name)  # Добавить строку в таблицу спутников       
        self.counter_spinbox.setValue(0)  # Обнуление счетчика

    def show_message_box(self, satellite_name, saved_counter,eccentricity_value,inclination_value,ascending_node_value,anomaly_value,pericenter_value):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Спутник добавлен")
        msg_box.setText(f"Название спутника: {satellite_name}\nLarge semi-axis: {saved_counter}\nEccentricity: {eccentricity_value}\nInclination: {inclination_value}\nLongitude of the ascending node: {ascending_node_value}\nArgument of the pericenter: {pericenter_value}\nMean anomaly: {anomaly_value}")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setFixedSize(800, 200)  # Установка размеров окна
        msg_box.exec()

    def insert_row_to_table(self, satellite_name):
        row_count = self.satellite_table.rowCount()
        self.satellite_table.insertRow(row_count)
        satellite_name_item = QTableWidgetItem(satellite_name)
        satellite_name_item.setFlags(satellite_name_item.flags() & ~Qt.ItemIsEditable)  # Запретить редактирование ячейки
        self.satellite_table.setItem(row_count, 0, satellite_name_item)  # Название спутника

        
    def update_eccentricity_counter(self, value):
        self.eccentricity_counter = value

    def showCellInfo(self, row, column):
        cell_content = self.satellite_table.item(row, column).text()
        satellite_name_item = self.satellite_table.horizontalHeaderItem(column).text()
        self.popup = DynamicPopupWindow(satellite_name_item, cell_content)
        self.popup.show()

    def increment_spinbox_value(self):
        self.counter += 1
        self.counter_spinbox.setValue(self.counter)

    def decrement_spinbox_value(self):
        self.counter -= 1
        self.counter_spinbox.setValue(self.counter)

class DynamicPopupWindow(QWidget):
    def __init__(self, satellite_name_item, content):
        super().__init__()

        layout = QVBoxLayout()
        self.satellite_label = QLabel(satellite_name_item)
        layout.addWidget(self.satellite_label)

        self.label = QLabel(content)
        layout.addWidget(self.label)

        self.setLayout(layout)
        self.setWindowTitle("Cell Info")
        self.resize(300, 200)

    def set_content(self, content):
        self.label.setText(content)

    def perform_action(self, action):
        # Реализуйте необходимые действия на основе переданного действия
        pass


    def set_content(self, content):
        self.label.setText(content)

    def perform_action(self, action):
        # Реализуйте необходимые действия на основе переданного действия
        pass

    
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
