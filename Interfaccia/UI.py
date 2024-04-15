import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDialog, QMessageBox, QMainWindow, QAction, QMenu, QProgressBar, QComboBox
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg

# Classe per la finestra di login
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.attempts = 3  # Limite di tentativi di accesso
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')
        self.setGeometry(300, 300, 300, 150)

        # Elementi dell'interfaccia
        self.label_username = QLabel('Username:', self)
        self.textbox_username = QLineEdit(self)
        self.label_password = QLabel('Password:', self)
        self.textbox_password = QLineEdit(self)
        self.textbox_password.setEchoMode(QLineEdit.Password)
        self.button_login = QPushButton('Login', self)
        self.button_login.clicked.connect(self.check_login)

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.label_username)
        vbox.addWidget(self.textbox_username)
        vbox.addWidget(self.label_password)
        vbox.addWidget(self.textbox_password)
        vbox.addWidget(self.button_login)
        self.setLayout(vbox)

    # Funzione per verificare il login
    def check_login(self):
        username = self.textbox_username.text()
        password = self.textbox_password.text()

        if username == 'admin' and password == 'password':
            QMessageBox.information(self, 'Login', 'Accesso consentito')
            self.accept()
        else:
            self.attempts -= 1  # Decrementa il numero di tentativi rimanenti
            if self.attempts == 0:
                QMessageBox.critical(self, 'Login', 'Tentativi esauriti. Uscita.')
                sys.exit()
            else:
                QMessageBox.warning(self, 'Login', f'Nome utente o password errati. Tentativi rimanenti: {self.attempts}')

# Classe per la finestra di monitoraggio delle batterie
class BatteryWindow(QMainWindow):
    def __init__(self, num_batteries, graph_window, battery_offset):
        super().__init__()
        self.num_batteries = num_batteries
        self.graph_window = graph_window
        self.battery_offset = battery_offset
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Monitoraggio Batterie')
        self.setGeometry(300, 200, 400, 300)

        layout = QVBoxLayout()

        for i in range(self.num_batteries):
            label_battery = QLabel(f'Batteria {i+1 + self.battery_offset}:', self)
            progress_bar_battery = QProgressBar(self)
            progress_bar_battery.setValue(random.randint(20, 100))

            button_discharge = QPushButton('Scarica', self)
            button_discharge.clicked.connect(lambda _, idx=i: self.adjust_battery_charge(idx, -1))

            button_charge = QPushButton('Carica', self)
            button_charge.clicked.connect(lambda _, idx=i: self.adjust_battery_charge(idx, 1))

            hbox = QHBoxLayout()
            hbox.addWidget(label_battery)
            hbox.addWidget(progress_bar_battery)
            hbox.addWidget(button_discharge)
            hbox.addWidget(button_charge)

            layout.addLayout(hbox)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_battery_status)
        self.timer.start(1000)

    # Funzione per aggiornare lo stato della batteria
    def update_battery_status(self):
        for progress_bar in self.centralWidget().findChildren(QProgressBar):
            current_value = progress_bar.value()
            progress_bar.setValue(max(0, current_value - random.randint(1, 3)))

        self.graph_window.plot_battery_data()

    # Funzione per regolare la carica della batteria
    def adjust_battery_charge(self, idx, change):
        progress_bar = self.centralWidget().findChildren(QProgressBar)[idx]
        current_value = progress_bar.value()
        progress_bar.setValue(max(0, min(100, current_value + change)))

# Classe per la finestra di monitoraggio del voltaggio
class VoltageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Monitoraggio Voltaggio')
        self.setGeometry(300, 200, 400, 200)

        self.label_voltage1 = QLabel('Voltaggio Batteria 1: 12.6V', self)
        self.label_voltage2 = QLabel('Voltaggio Batteria 2: 12.6V', self)

        layout = QVBoxLayout()
        layout.addWidget(self.label_voltage1)
        layout.addWidget(self.label_voltage2)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

# Classe per la finestra dei grafici delle batterie
class BatteryGraphWindow(QMainWindow):
    def __init__(self, num_batteries):
        super().__init__()
        self.num_batteries = num_batteries
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Grafici Batterie')
        self.setGeometry(300, 200, 600, 400)

        self.battery_plots = []
        self.colors = [(31, 119, 180), (255, 127, 14), (44, 160, 44)]

        layout = QVBoxLayout()

        self.combo_box = QComboBox(self)
        for i in range(self.num_batteries):
            self.combo_box.addItem(f'Batteria {i+1}')

        layout.addWidget(self.combo_box)

        self.graph_widget = pg.PlotWidget(self)
        self.graph_widget.setBackground('w')
        self.graph_widget.addLegend()
        self.graph_widget.showGrid(x=True, y=True)
        self.graph_widget.setLabel('left', 'Carica (%)')
        self.graph_widget.setLabel('bottom', 'Tempo (s)')
        layout.addWidget(self.graph_widget)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.plot_battery_data()

        self.combo_box.currentIndexChanged.connect(self.update_graph)

    # Funzione per tracciare i dati della batteria
    def plot_battery_data(self):
        self.graph_widget.clear()
        selected_battery = self.combo_box.currentIndex()
        x = [0, 1, 2, 3, 4, 5]
        y = [random.randint(20, 100) for _ in range(len(x))]
        pen = pg.mkPen(color=self.colors[selected_battery % len(self.colors)], width=2)
        self.graph_widget.plot(x, y, pen=pen, name=f'Batteria {selected_battery+1}')

    # Funzione per aggiornare il grafico
    def update_graph(self):
        self.plot_battery_data()

# Classe per la finestra dei grafici di tutte le batterie
class AllBatteryGraphWindow(QMainWindow):
    def __init__(self, num_batteries):
        super().__init__()
        self.num_batteries = num_batteries
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tutti i Grafici Batterie')
        self.setGeometry(300, 200, 800, 600)

        self.graph_widget = pg.PlotWidget(self)
        self.graph_widget.setBackground('w')
        self.graph_widget.addLegend()
        self.graph_widget.showGrid(x=True, y=True)
        self.graph_widget.setLabel('left', 'Carica (%)')
        self.graph_widget.setLabel('bottom', 'Tempo (s)')

        layout = QVBoxLayout()
        layout.addWidget(self.graph_widget)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.plot_all_battery_data()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(1000)

    # Funzione per tracciare i dati di tutte le batterie
    def plot_all_battery_data(self):
        self.data = [[] for _ in range(self.num_batteries)]
        self.lines = []

        for i in range(self.num_batteries):
            pen = pg.mkPen(color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), width=2)
            line = self.graph_widget.plot([], [], pen=pen, name=f'Batteria {i+1}')
            self.lines.append(line)

    # Funzione per aggiornare il grafico
    def update_graph(self):
        for i in range(self.num_batteries):
            x = [0, 1, 2, 3, 4, 5]  # Esempio di tempo
            y = [random.randint(20, 100) for _ in range(len(x))]  # Esempio di dati della batteria
            self.lines[i].setData(x, y)

# Funzione principale
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Finestra di login
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        num_batteries = random.randint(1, 10)
        num_battery_windows = (num_batteries - 1) // 3 + 1
        graph_window = BatteryGraphWindow(num_batteries)

        all_battery_graph_window = AllBatteryGraphWindow(num_batteries)

        battery_offset = 0
        battery_windows = []

        for i in range(num_battery_windows):
            batteries_remaining = num_batteries - battery_offset
            num_batteries_on_page = min(batteries_remaining, 3)
            if num_batteries_on_page > 0:
                battery_window = BatteryWindow(num_batteries_on_page, graph_window, battery_offset)
                battery_windows.append(battery_window)
                battery_offset += num_batteries_on_page

        # Se ci sono finestre delle batterie create, mostriamo la finestra principale
        if battery_windows:
            for battery_window in battery_windows:
                battery_window.show()

            main_window = graph_window
            menu_bar = main_window.menuBar()
            view_menu = menu_bar.addMenu('View')

            voltage_action = QAction('Monitoraggio Voltaggio', main_window)
            voltage_action.triggered.connect(lambda: VoltageWindow().show())
            view_menu.addAction(voltage_action)

            graph_action = QAction('Grafici Batterie', main_window)
            graph_action.triggered.connect(lambda: graph_window.show())
            view_menu.addAction(graph_action)

            all_graph_action = QAction('Tutti i Grafici Batterie', main_window)
            all_graph_action.triggered.connect(lambda: all_battery_graph_window.show())
            view_menu.addAction(all_graph_action)

            main_window.show()

    sys.exit(app.exec_())
