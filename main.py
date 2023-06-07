from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QInputDialog, 
    QMessageBox, QAbstractItemView, QListWidget, 
    QListWidgetItem
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
        self.ui.pushButton_Update.clicked.connect(self.update_task)
        self.ui.pushButton_Update.setToolTip('Editar uma tarefa')
        self.ui.pushButton_Delete.clicked.connect(self.delete_task)
        self.ui.pushButton_Delete.setToolTip('Remover uma tarefa')
        self.ui.pushButton_DeleteAll.clicked.connect(self.clear_list)
        self.ui.pushButton_DeleteAll.setToolTip('Limpar agenda')
        self.ui.pushButton_Find.clicked.connect(self.find_task)
        self.ui.pushButton_Find.setToolTip('Buscar tarefa')
        self.ui.lineEdit_AddingItem.textChanged.connect(self.check_textbox)
        self.ui.lineEdit_AddingItem.setPlaceholderText("Digite uma tarefa")
     
        # Habilita a capacidade de reordenar itens usando arrastar e soltar
        self.ui.minhaLista_listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        # Reorganiza os itens da lista automaticamente conforme a posição do item reordenado
        self.ui.minhaLista_listWidget.setMovement(QListWidget.Snap)
        # Impede o usuário de arrastar e soltar a tarefa fora da aplicação
        self.ui.minhaLista_listWidget.setDragDropMode(self.ui.minhaLista_listWidget.InternalMove)

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

        # Adiciona a tarefa à lista
        item = QListWidgetItem(task_text)
        item.setCheckState(Qt.Unchecked)
        item.setText(task_text)

        self.ui.minhaLista_listWidget.addItem(item)
        self.ui.lineEdit_AddingItem.clear()
        self.ui.minhaLista_listWidget.setCurrentItem(None)

    def update_task(self):
        """
        Edita uma tarefa selecionada na lista de tarefas.
        """
        selected_item = self.ui.minhaLista_listWidget.currentItem()
        if selected_item is None:
            QMessageBox.warning(self.ui.centralwidget, "Aviso", "Por favor, selecione uma tarefa para editar.")
            return

        # Abre uma caixa de diálogo para inserir o novo texto da tarefa
        new_text, ok = QInputDialog.getText(self.ui.centralwidget, "Editar Tarefa", "Digite a nova tarefa:", text=selected_item.text())
        if ok:
            selected_item.setText(new_text)
            self.ui.minhaLista_listWidget.setCurrentItem(None)

    def delete_task(self):
        """
        Remove uma tarefa selecionada da lista de tarefas.
        """
        selected_item = self.ui.minhaLista_listWidget.currentItem()
        if selected_item is None:
            QMessageBox.warning(self.ui.centralwidget, "Aviso", "Por favor, selecione uma tarefa para remover.")
            return

        # Pede uma confirmação antes de remover a tarefa
        confirm = QMessageBox.question(self.ui.centralwidget, "Confirmar", "Tem certeza que deseja remover esta tarefa?")
        if confirm == QMessageBox.Yes:
            self.ui.minhaLista_listWidget.takeItem(self.ui.minhaLista_listWidget.row(selected_item))
            self.ui.minhaLista_listWidget.setCurrentItem(None)
            return

    def clear_list(self):
        """
        Limpa a lista de tarefas.
        """
        if self.ui.minhaLista_listWidget.count() == 0:
            QMessageBox.warning(self.ui.centralwidget, "Aviso", "A agenda já está vazia.")
            return
        
        # Pede uma confirmação antes de limpar a lista de tarefas
        confirm = QMessageBox.question(self.ui.centralwidget, "Confirmar", "Tem certeza que deseja limpar a agenda?")
        if confirm == QMessageBox.Yes:
            self.ui.minhaLista_listWidget.clear()

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
