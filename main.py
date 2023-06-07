from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QInputDialog, 
    QMessageBox, QAbstractItemView, QListWidget, 
    QListWidgetItem, QPushButton, QHBoxLayout,
    QWidget, QLabel, QSpacerItem, QSizePolicy,
    QCheckBox
)
from janela import Ui_MainWindow

class Agenda:
    def __init__(self, ui):
        """
        Inicializa a Agenda.
        Args:
            ui: Instância da classe Ui_MainWindow gerada pelo Qt Designer.
        """
        self.ui = ui
        self.ui.pushButton_Create.clicked.connect(self.add_task)
        self.ui.pushButton_Create.setToolTip('Adicionar tarefa')
        self.ui.pushButton_Find.clicked.connect(self.find_task)
        self.ui.pushButton_Find.setToolTip('Buscar tarefa')
        self.ui.lineEdit_AddingItem.textChanged.connect(self.check_textbox)
        self.ui.lineEdit_AddingItem.setPlaceholderText("Digite uma tarefa")
     
        # Habilita a capacidade de reordenar itens usando arrastar e soltar
        self.ui.minhaLista_listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        # Reorganiza os itens da lista automaticamente conforme a posição do item reordenado
        self.ui.minhaLista_listWidget.setMovement(QListWidget.Snap)

        # Desabilita o botão "Adicionar tarefa" inicialmente
        self.ui.pushButton_Create.setEnabled(False)

    def check_textbox(self):
        """
        Verifica se o lineEdit_AddingItem está vazio e habilita/desabilita o botão "Adicionar tarefa" de acordo.
        """
        if self.ui.lineEdit_AddingItem.text() == "":
            self.ui.pushButton_Create.setEnabled(False)
        else:
            self.ui.pushButton_Create.setEnabled(True)

    def add_task(self):
        """
        Adiciona uma tarefa à lista de tarefas da agenda.
        """
        task_text = self.ui.lineEdit_AddingItem.text()
        if task_text == "":
            return

        # Verifica se a tarefa já está na lista
        for index in range(self.ui.minhaLista_listWidget.count()):
            item = self.ui.minhaLista_listWidget.item(index)
            if item.text() == task_text:
                QMessageBox.warning(self.ui.centralwidget, "Aviso", "Esta tarefa já está na lista.")
                return

        # Cria o widget do item
        item_widget = QWidget()
        layout = QHBoxLayout(item_widget)
        layout.setContentsMargins(10, 0, 0, 0)

        # Cria o checkbox
        checkbox = QCheckBox()
        checkbox.setChecked(False)
        layout.addWidget(checkbox)

        # Cria o label da tarefa
        task_label = QLabel(task_text)
        layout.addWidget(task_label)

        spacer_item = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer_item)

        # Cria o botão de editar
        edit_button = QPushButton()
        edit_button.setIcon(QIcon("assets/edit.svg"))
        edit_button.setIconSize(QtCore.QSize(24, 24))
        edit_button.setToolTip("Editar esta tarefa")
        edit_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        layout.addWidget(edit_button)
        # Cria o botão de remover
        remove_button = QPushButton()
        remove_button.setIcon(QIcon("assets/remove.svg"))
        remove_button.setIconSize(QtCore.QSize(24, 24))
        remove_button.setToolTip("Remover esta tarefa")
        remove_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        layout.addWidget(remove_button)

        # Cria o item da lista
        item = QListWidgetItem()
        item.setSizeHint(item_widget.sizeHint())  # Define o tamanho do item com base no tamanho do widget
        self.ui.minhaLista_listWidget.addItem(item)
        self.ui.minhaLista_listWidget.setItemWidget(item, item_widget)

        # Conecta o botão de remover à função de remoção
        remove_button.clicked.connect(lambda: self.delete_task(item))

        # Conecta o botão de editar à função de edição
        edit_button.clicked.connect(lambda: self.edit_task(item))

        self.ui.lineEdit_AddingItem.clear()
        self.ui.minhaLista_listWidget.setCurrentItem(None)

    def edit_task(self, item):
        """
        Edita uma tarefa selecionada na lista de tarefas.
        """
        # Obtém o widget associado ao item
        item_widget = self.ui.minhaLista_listWidget.itemWidget(item)

        # Obtém o label da tarefa dentro do widget
        task_label = item_widget.findChild(QLabel)

        # Obtém o texto atual da tarefa
        current_text = task_label.text()

        # Abre uma caixa de diálogo para inserir o novo texto da tarefa
        new_text, ok = QInputDialog.getText(self.ui.centralwidget, "Editar Tarefa", "Digite a nova tarefa:", text=current_text)
        if ok:
            task_label.setText(new_text)
            self.ui.minhaLista_listWidget.setCurrentItem(None)

    def delete_task(self, item):
        """
        Remove uma tarefa selecionada da lista de tarefas.
        """
        confirm = QMessageBox.question(self.ui.centralwidget, "Confirmar", "Tem certeza que deseja remover esta tarefa?")
        if confirm == QMessageBox.Yes:
            self.ui.minhaLista_listWidget.takeItem(self.ui.minhaLista_listWidget.row(item))

    def find_task(self):
        """
        Busca uma tarefa na lista da agenda.
        """
        task_text = self.ui.lineEdit_AddingItem.text()
        if task_text == "":
            QMessageBox.warning(self.ui.centralwidget, "Aviso", "Por favor, digite uma tarefa para buscar.")
            return
        
        found_items = self.ui.minhaLista_listWidget.findItems(task_text, QtCore.Qt.MatchContains)
        if len(found_items) > 0:
            self.ui.minhaLista_listWidget.setCurrentItem(found_items[0])
        else:
            QMessageBox.information(self.ui.centralwidget, "Informação", "A tarefa não foi encontrada.")

if __name__ == "__main__":
    app = QApplication([])

    # Carrega as estilizações
    with open("styles.qss", "r") as f:
        qss = f.read()
        app.setStyleSheet(qss)

    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    agenda = Agenda(ui)
    window.show()
    app.exec_()
