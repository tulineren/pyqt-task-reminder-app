import sys
from PyQt5 import QtWidgets, QtCore


# 1. Ana Pencere
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle(f"Hoş Geldin, {username}")
        self.resize(600, 400)
        self.setCentralWidget(QtWidgets.QWidget())
        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("Burada Görevler ve Hatırlatmalar Görüntülenecek", self)
        layout.addWidget(self.label)

        self.task_list = QtWidgets.QListWidget(self)
        self.task_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.task_list.customContextMenuRequested.connect(self.show_task_context_menu)
        layout.addWidget(self.task_list)

        self.reminder_list = QtWidgets.QListWidget(self)
        self.reminder_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.reminder_list.customContextMenuRequested.connect(self.show_reminder_context_menu)
        layout.addWidget(self.reminder_list)

        self.open_task_button = QtWidgets.QPushButton("Yeni Görev Ekle", self)
        self.open_task_button.clicked.connect(self.openNewTaskWindow)
        layout.addWidget(self.open_task_button)

        self.open_reminder_button = QtWidgets.QPushButton("Yeni Hatırlatıcı Ekle", self)
        self.open_reminder_button.clicked.connect(self.openNewReminderWindow)
        layout.addWidget(self.open_reminder_button)

        self.open_task_status_button = QtWidgets.QPushButton("Görev Durumunu Görüntüle", self)
        self.open_task_status_button.clicked.connect(self.openTaskStatusWindow)
        layout.addWidget(self.open_task_status_button)

        self.open_user_settings_button = QtWidgets.QPushButton("Kullanıcı Ayarları", self)
        self.open_user_settings_button.clicked.connect(self.openUserSettingsWindow)
        layout.addWidget(self.open_user_settings_button)

        self.centralWidget().setLayout(layout)
        self.reminders = []

    def openNewTaskWindow(self):
        self.new_task_window = TaskWindow(self)
        self.new_task_window.show()

    def openNewReminderWindow(self):
        self.new_reminder_window = ReminderWindow(self)
        self.new_reminder_window.show()

    def openTaskStatusWindow(self):
        self.task_status_window = TaskStatusWindow(self)
        self.task_status_window.show()

    def openUserSettingsWindow(self):
        self.user_settings_window = UserSettingsWindow(self)
        self.user_settings_window.show()

    def addTaskToList(self, task):
        task_item = QtWidgets.QListWidgetItem(task)
        checkbox = QtWidgets.QCheckBox("Tamamlandı", self)
        self.task_list.setItemWidget(task_item, checkbox)
        task_item.setFlags(task_item.flags() | QtCore.Qt.ItemIsEditable)
        self.task_list.addItem(task_item)

    def addReminderToList(self, reminder, reminder_date):
        reminder_item = QtWidgets.QListWidgetItem(f"{reminder} - {reminder_date}")
        self.reminder_list.addItem(reminder_item)
        self.reminders.append(reminder)

    def show_task_context_menu(self, pos):
        menu = QtWidgets.QMenu(self)
        delete_action = menu.addAction("Sil")
        delete_action.triggered.connect(self.deleteTask)
        menu.exec_(self.task_list.mapToGlobal(pos))

    def show_reminder_context_menu(self, pos):
        menu = QtWidgets.QMenu(self)
        delete_action = menu.addAction("Sil")
        delete_action.triggered.connect(self.deleteReminder)
        menu.exec_(self.reminder_list.mapToGlobal(pos))

    def deleteTask(self):
        item = self.task_list.currentItem()
        if item:
            self.task_list.takeItem(self.task_list.row(item))

    def deleteReminder(self):
        item = self.reminder_list.currentItem()
        if item:
            self.reminder_list.takeItem(self.reminder_list.row(item))


class TaskWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Yeni Görev Ekle")
        self.resize(400, 300)
        self.setCentralWidget(QtWidgets.QWidget())
        layout = QtWidgets.QVBoxLayout()

        self.task_input = QtWidgets.QLineEdit(self)
        self.task_input.setPlaceholderText("Yeni görev adı")
        layout.addWidget(self.task_input)

        self.add_button = QtWidgets.QPushButton("Görevi Ekle", self)
        self.add_button.clicked.connect(self.addTask)
        layout.addWidget(self.add_button)

        self.cancel_button = QtWidgets.QPushButton("İptal", self)
        self.cancel_button.clicked.connect(self.close)
        layout.addWidget(self.cancel_button)

        self.centralWidget().setLayout(layout)

    def addTask(self):
        task = self.task_input.text()
        if task:
            self.parent.addTaskToList(task)
        self.close()


class ReminderWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Hatırlatıcılar")
        self.resize(400, 300)
        self.setCentralWidget(QtWidgets.QWidget())
        layout = QtWidgets.QVBoxLayout()

        self.reminder_input = QtWidgets.QLineEdit(self)
        self.reminder_input.setPlaceholderText("Hatırlatıcı metni girin")
        layout.addWidget(self.reminder_input)

        self.reminder_date_input = QtWidgets.QDateTimeEdit(self)
        layout.addWidget(self.reminder_date_input)

        self.add_button = QtWidgets.QPushButton("Hatırlatıcıyı Ekle", self)
        self.add_button.clicked.connect(self.addReminder)
        layout.addWidget(self.add_button)

        self.cancel_button = QtWidgets.QPushButton("İptal", self)
        self.cancel_button.clicked.connect(self.close)
        layout.addWidget(self.cancel_button)

        self.centralWidget().setLayout(layout)

    def addReminder(self):
        reminder = self.reminder_input.text()
        reminder_date = self.reminder_date_input.dateTime().toString()
        if reminder:
            self.parent.addReminderToList(reminder, reminder_date)
        self.close()


class TaskStatusWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Görev Durumu")
        self.resize(400, 300)

        self.setCentralWidget(QtWidgets.QWidget())
        layout = QtWidgets.QVBoxLayout()

        self.task_status_list = QtWidgets.QListWidget(self)
        layout.addWidget(self.task_status_list)

        self.update_button = QtWidgets.QPushButton("Durumları Güncelle", self)
        self.update_button.clicked.connect(self.updateTaskStatus)
        layout.addWidget(self.update_button)

        self.close_button = QtWidgets.QPushButton("Kapat", self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.centralWidget().setLayout(layout)

    def updateTaskStatus(self):
        self.task_status_list.clear()
        for row in range(self.parent.task_list.count()):
            item = self.parent.task_list.item(row)
            checkbox = self.parent.task_list.itemWidget(item)
            status = "Tamamlandı" if checkbox.isChecked() else "Tamamlanmadı"
            self.task_status_list.addItem(f"{item.text()} - {status}")


class UserSettingsWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Kullanıcı Ayarları")
        self.resize(400, 300)

        self.setCentralWidget(QtWidgets.QWidget())
        layout = QtWidgets.QVBoxLayout()

        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.setPlaceholderText("Kullanıcı Adı")
        layout.addWidget(self.username_input)

        self.theme_combo = QtWidgets.QComboBox(self)
        self.theme_combo.addItem("Koyu Tema")
        self.theme_combo.addItem("Açık Tema")
        layout.addWidget(self.theme_combo)

        self.notification_checkbox = QtWidgets.QCheckBox("Bildirimleri Aç", self)
        layout.addWidget(self.notification_checkbox)

        self.save_button = QtWidgets.QPushButton("Ayarları Kaydet", self)
        self.save_button.clicked.connect(self.saveSettings)
        layout.addWidget(self.save_button)

        self.cancel_button = QtWidgets.QPushButton("İptal", self)
        self.cancel_button.clicked.connect(self.close)
        layout.addWidget(self.cancel_button)

        self.centralWidget().setLayout(layout)

    def saveSettings(self):
        username = self.username_input.text()
        theme = self.theme_combo.currentText()
        notifications = self.notification_checkbox.isChecked()

        print(f"Kullanıcı Adı: {username}")
        print(f"Tema: {theme}")
        print(f"Bildirimler: {'Açık' if notifications else 'Kapalı'}")
        self.close()


class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Yap")
        self.resize(300, 150)
        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("Lütfen kullanıcı adınızı girin:")
        layout.addWidget(self.label)

        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı adı")
        layout.addWidget(self.username_input)

        self.login_button = QtWidgets.QPushButton("Giriş Yap")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text().strip()
        if username:
            self.main_window = MainWindow(username)
            self.main_window.show()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Kullanıcı adı boş olamaz!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
