from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox, QAbstractItemView, QListWidget
from janela import Ui_MainWindow

class Agenda:
    def __init__(self, ui):
        self.ui = ui
        self.ui.pushButton_Create.clicked.connect(self.add_task)
        self.ui.pushButton_Create.setToolTip('Adicionar tarefa')
        self.ui.pushButton_Update.clicked.connect(self.update_task)
        self.ui.pushButton_Update.setToolTip('Editar uma tarefa')
        self.ui.pushButton_Delete.clicked.connect(self.delete_task)
        self.ui.pushButton_Delete.setToolTip('Remover uma tarefa')
        self.ui.pushButton_DeleteAll.clicked.connect(self.clear_list)
        self.ui.pushButton_DeleteAll.setToolTip('Limpar agenda')
        self.ui.lineEdit_AddingItem.textChanged.connect(self.check_textbox)
     
        # Habilita a capacidade de reordenar itens usando arrastar e soltar
        self.ui.minhaLista_listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        # Reorganiza os itens da lista automaticamente conforme a posição do item reordenado
        self.ui.minhaLista_listWidget.setMovement(QListWidget.Snap)
        # Impede o usuário de arrastar e soltar a tarefa fora da aplicação
        self.ui.minhaLista_listWidget.setDragDropMode(self.ui.minhaLista_listWidget.InternalMove)

        # Desabilita o botão "Adicionar tarefa" inicialmente
        self.ui.pushButton_Create.setEnabled(False)

    def check_textbox(self):
        if self.ui.lineEdit_AddingItem.text() == "":
            self.ui.pushButton_Create.setEnabled(False)
        else:
            self.ui.pushButton_Create.setEnabled(True)

    def add_task(self):
        task_text = self.ui.lineEdit_AddingItem.text()
        if task_text == "":
            return

        for index in range(self.ui.minhaLista_listWidget.count()):
            item = self.ui.minhaLista_listWidget.item(index)
            if item.text() == task_text:
                QMessageBox.warning(self.ui.centralwidget, "Aviso", "Esta tarefa já está na lista.")
                return

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
        if self.ui.minhaLista_listWidget.count() == 0:
            QMessageBox.warning(self.ui.centralwidget, "Aviso", "A agenda já está vazia.")
            return
        confirm = QMessageBox.question(self.ui.centralwidget, "Confirmar", "Tem certeza que deseja limpar a agenda?")
        if confirm == QMessageBox.Yes:
            self.ui.minhaLista_listWidget.clear()

if __name__ == "__main__":
    app = QApplication([])

    app.setStyleSheet("""
        QMainWindow {
            background-color: "#1b1b1b";
        }

        QLineEdit {
            color: "#ffffff";
            font-family: 'Roboto', arial, cursive;
            background-color: "#4e4e4e";
            border-radius: 2px;
            height: 30px;
        }

        QListWidget {
            color: "#ffffff";
            font-size: 24px;
            font-family: 'Roboto', arial, cursive;
            background-color: "#4e4e4e";
            border-radius: 4px
        }

        QPushButton {
            padding-top: 6px;
            padding-bottom: 6px;
            background-color: "#93d849";
            border-radius: 10px
        }

        QPushButton:hover {
            background-color: "#a6f750";
        }

        QMessageBox {
            background-color: "#1b1b1b";
            color: "#ffffff";
            font-family: 'Roboto', arial, cursive;
            font-size: 16px;
        }

        QMessageBox QLabel {
            color: "#ffffff";
        }

        QMessageBox QPushButton {
            background-color: "#93d849";
            border-radius: 10px;
            padding: 5px
        }

        QMessageBox QPushButton:hover {
            background-color: "#a6f750";
        }

        QInputDialog {
            background-color: "#1b1b1b";
            color: "#ffffff";
            font-family: 'Roboto', arial, cursive;
        }

        QInputDialog QLabel {
            color: "#ffffff";
        }

        QInputDialog QLineEdit {
            color: "#ffffff";
            background-color: "#4e4e4e";
            border-radius: 2px;
            height: 30px;
        }

        QInputDialog QPushButton {
            background-color: "#93D849";
            border-radius: 10px;
            padding: 5px;
        }

        QInputDialog QPushButton:hover {
            background-color: "#a6f750";
        }

    """)

    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    agenda = Agenda(ui)
    window.show()
    app.exec_()
