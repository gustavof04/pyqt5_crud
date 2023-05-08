from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox
from janela import Ui_MainWindow

class Agenda:
    def __init__(self, ui):
        self.ui = ui
        self.ui.pushButton_Create.clicked.connect(self.add_task)
        self.ui.pushButton_Update.clicked.connect(self.update_task)
        self.ui.pushButton_Delete.clicked.connect(self.delete_task)
        self.ui.pushButton_DeleteAll.clicked.connect(self.clear_list)
        self.ui.lineEdit_AddingItem.textChanged.connect(self.check_textbox)
     
        # Desabilita o botão "Adicionar tarefa" inicialmente
        self.ui.pushButton_Create.setEnabled(False)

    def check_textbox(self):
        if self.ui.lineEdit_AddingItem.text() == "":
            self.ui.pushButton_Create.setEnabled(False)
        else:
            self.ui.pushButton_Create.setEnabled(True)

    def add_task(self):
        task_text = self.ui.lineEdit_AddingItem.text()
        if task_text != "":
            self.ui.minhaLista_listWidget.addItem(task_text)
            self.ui.lineEdit_AddingItem.clear()
            self.ui.minhaLista_listWidget.setCurrentItem(None)

    def update_task(self):
        selected_item = self.ui.minhaLista_listWidget.currentItem()
        if selected_item is None:
            QMessageBox.warning(self.ui.centralwidget, "Aviso", "Por favor, selecione uma tarefa para editar.")
            return

        new_text, ok = QInputDialog.getText(self.ui.centralwidget, "Editar Tarefa", "Digite a nova tarefa:", text=selected_item.text())
        if ok:
            selected_item.setText(new_text)
            self.ui.minhaLista_listWidget.setCurrentItem(None)

    def delete_task(self):
        selected_item = self.ui.minhaLista_listWidget.currentItem()
        if selected_item is None:
            QMessageBox.warning(self.ui.centralwidget, "Aviso", "Por favor, selecione uma tarefa para remover.")
            return
        
        confirm = QMessageBox.question(self.ui.centralwidget, "Confirmar", "Tem certeza que deseja remover esta tarefa?")
        if confirm == QMessageBox.Yes:
            self.ui.minhaLista_listWidget.takeItem(self.ui.minhaLista_listWidget.row(selected_item))
            self.ui.minhaLista_listWidget.setCurrentItem(None)
            return
        
    def clear_list(self):
        confirm = QMessageBox.question(self.ui.centralwidget, "Confirmar", "Tem certeza que deseja limpar a lista de tarefas?")
        if confirm == QMessageBox.Yes:
            self.ui.minhaLista_listWidget.clear()

if __name__ == "__main__":
    app = QApplication([])
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    agenda = Agenda(ui)
    window.show()
    app.exec_()
