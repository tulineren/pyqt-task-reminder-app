import sys
from PyQt5 import QtWidgets, QtCore


# 1. Ana Pencere
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ana Pencere - Görevler")
        self.resize(600, 400)
        self.setCentralWidget(QtWidgets.QWidget())
        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("Burada Görevler ve Hatırlatmalar Görüntülenecek", self)
        layout.addWidget(self.label)

        # Görevler için liste
        self.task_list = QtWidgets.QListWidget(self)
        self.task_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.task_list.customContextMenuRequested.connect(self.show_task_context_menu)
        layout.addWidget(self.task_list)

        # Hatırlatıcılar için liste
        self.reminder_list = QtWidgets.QListWidget(self)
        self.reminder_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.reminder_list.customContextMenuRequested.connect(self.show_reminder_context_menu)
        layout.addWidget(self.reminder_list)

        # 5 QMainWindow'dan birini açacak butonlar
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

        self.reminders = []  # Hatırlatıcıları tutacak liste

    def openNewTaskWindow(self):
        self.new_task_window = TaskWindow(self)  # Ana pencereye yeni görev ekle
        self.new_task_window.show()

    def openNewReminderWindow(self):
        self.new_reminder_window = ReminderWindow(self)  # Ana pencereye yeni hatırlatıcı ekle
        self.new_reminder_window.show()

    def openTaskStatusWindow(self):
        self.task_status_window = TaskStatusWindow(self)  # Görev durumu penceresini aç
        self.task_status_window.show()

    def openUserSettingsWindow(self):
        self.user_settings_window = UserSettingsWindow(self)  # Kullanıcı ayarları penceresini aç
        self.user_settings_window.show()

    def addTaskToList(self, task):
        task_item = QtWidgets.QListWidgetItem(task)
        checkbox = QtWidgets.QCheckBox("Tamamlandı", self)
        self.task_list.setItemWidget(task_item, checkbox)  # Görev item'ına checkbox ekliyoruz
        task_item.setFlags(task_item.flags() | QtCore.Qt.ItemIsEditable)  # Düzenlenebilir yapıyoruz
        self.task_list.addItem(task_item)

    def addReminderToList(self, reminder, reminder_date):
        reminder_item = QtWidgets.QListWidgetItem(reminder)
        reminder_item.setText(f"{reminder} - {reminder_date}")  # Hatırlatıcıya tarih ekliyoruz
        self.reminder_list.addItem(reminder_item)
        self.reminders.append(reminder)  # Hatırlatıcıları listeye ekle

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
            self.task_list.takeItem(self.task_list.row(item))  # Seçili öğeyi sil

    def deleteReminder(self):
        item = self.reminder_list.currentItem()
        if item:
            self.reminder_list.takeItem(self.reminder_list.row(item))  # Seçili öğeyi sil


# 2. Görev Ekleme Penceresi
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
            self.parent.addTaskToList(task)  # Görevi ana pencereye ekler
        self.close()


# 3. Hatırlatıcılar Penceresi
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

        # Hatırlatıcı için tarih seçici
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
            self.parent.addReminderToList(reminder, reminder_date)  # Hatırlatıcıyı ana pencereye ekler
        self.close()


# 4. Görev Durumu Penceresi
class TaskStatusWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Görev Durumu")
        self.resize(400, 300)

        self.setCentralWidget(QtWidgets.QWidget())
        layout = QtWidgets.QVBoxLayout()

        # Görevler için durumlar
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
            task_status = "Tamamlandı" if checkbox.isChecked() else "Tamamlanmadı"
            self.task_status_list.addItem(f"{item.text()} - {task_status}")


# 5. Kullanıcı Ayarları Penceresi
class UserSettingsWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Kullanıcı Ayarları")
        self.resize(400, 300)

        self.setCentralWidget(QtWidgets.QWidget())
        layout = QtWidgets.QVBoxLayout()

        # Kullanıcı adı ayarı
        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.setPlaceholderText("Kullanıcı Adı")
        layout.addWidget(self.username_input)

        # Tema tercihi
        self.theme_combo = QtWidgets.QComboBox(self)
        self.theme_combo.addItem("Koyu Tema")
        self.theme_combo.addItem("Açık Tema")
        layout.addWidget(self.theme_combo)

        # Bildirim ayarı
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

        # Burada kullanıcı ayarları kaydedilebilir
        print(f"Kullanıcı Adı: {username}")
        print(f"Seçilen Tema: {theme}")
        print(f"Bildirimler: {'Açık' if notifications else 'Kapalı'}")
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

#Kullanılan Kütüphaneler:
#PyQt5: Grafiksel kullanıcı arayüzü (GUI) oluşturmak için kullanılmıştır.
#QtWidgets: Ana pencere, diyalog pencereleri, butonlar, metin kutuları ve listeler gibi GUI öğeleri için kullanılmıştır.
#QtCore: Qt uygulamaları için temel işlevleri sağlar, zamanlayıcı ve metin işleme gibi işlemler için kullanılmıştır.

#Kullanılan Sınıflar ve Nesneler:
#QMainWindow: Her pencere için kullanılan temel sınıftır.
#QListWidget: Görevler ve hatırlatıcılar için liste öğelerini yönetir.
#QPushButton: Kullanıcı etkileşimlerini tetikleyen butonları oluşturur.
#QLineEdit: Kullanıcıdan metin girişi almak için kullanılır.
#QDateTimeEdit: Hatırlatıcılar için tarih ve saat seçici sağlar.
#QCheckBox: Görevlerin tamamlanıp tamamlanmadığını kontrol etmek için kullanılır.
#QComboBox: Tema tercihi yapmak için kullanılır.

