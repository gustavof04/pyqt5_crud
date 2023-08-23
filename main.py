import sqlite3
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import *
from janela import Ui_MainWindow

# Criando conexão com db
conn = sqlite3.connect('tasks.db')
# Criando cursor
c = conn.cursor()

# Criando tabela
c.execute("""CREATE TABLE if not exists tasks(
    list_item TEXT)
    """)

# Commitando as mudanças
conn.commit()

# Fechando conexão
conn.close()
class ListaTodo:
    def __init__(self, ui):
        """
        Inicializa a aplicação.
        Args:
            ui: Instância da classe Ui_MainWindow gerada pelo Qt Designer.
        """
        self.ui = ui
        self.ui.pushButton_Create.clicked.connect(self.setup_task)
        self.ui.pushButton_Create.setToolTip('Adicionar tarefa')
        self.ui.pushButton_Create.setEnabled(False)
        self.ui.pushButton_Create.clicked.connect(self.save_task_on_db)
        self.ui.pushButton_Find.clicked.connect(self.search_task)
        self.ui.pushButton_Find.setToolTip('Buscar tarefa')
        self.ui.lineEdit_AddingItem.textChanged.connect(self.check_textbox)
        self.ui.lineEdit_AddingItem.setPlaceholderText("Adicionar ao todo")
        self.ui.lineEdit_AddingItem.selectionChanged.connect(self.clear_search_input)
        self.ui.lineEdit_SearchItem.textChanged.connect(self.check_textbox)
        self.ui.lineEdit_SearchItem.setPlaceholderText("Pesquisar uma tarefa")
        self.ui.minhaLista_listWidget.setSelectionMode(QAbstractItemView.NoSelection)

    def check_textbox(self):
        """
        Verifica se o lineEdit_AddingItem está vazio e habilita/desabilita o botão "Adicionar tarefa" de acordo.
        """
        if self.ui.lineEdit_AddingItem.text() == "":
            self.ui.pushButton_Create.setEnabled(False)
        else:
            self.ui.pushButton_Create.setEnabled(True)

    def setup_task(self):
        """
        Adiciona a tarefa à lista e configura as propriedades de edição e remoção nela.
        """
        task_text = self.ui.lineEdit_AddingItem.text()
        if task_text == "":
            return

        # Verifica se a tarefa já está na lista
        for index in range(self.ui.minhaLista_listWidget.count()):
            item = self.ui.minhaLista_listWidget.item(index)
            item_widget = self.ui.minhaLista_listWidget.itemWidget(item)
            task_label = item_widget.findChild(QLabel)

        # Verifica se o texto da tarefa é igual ao texto informado
            if task_label.text() == task_text:
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

        # Cria o botão de editar ao lado da tarefa adicionada
        edit_button = QPushButton()
        edit_button.setIcon(QIcon("assets/edit.svg"))
        edit_button.setIconSize(QtCore.QSize(24, 24))
        edit_button.setToolTip("Editar esta tarefa")
        edit_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        layout.addWidget(edit_button)
        # Cria o botão de remover ao lado da tarefa adicionada
        remove_button = QPushButton()
        remove_button.setIcon(QIcon("assets/remove.svg"))
        remove_button.setIconSize(QtCore.QSize(24, 24))
        remove_button.setToolTip("Remover esta tarefa")
        remove_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        layout.addWidget(remove_button)

        checkbox.stateChanged.connect(lambda state, label=task_label: label.setStyleSheet("text-decoration: line-through;" if state == Qt.Checked else ""))

        # Cria o item da lista
        item = QListWidgetItem()
        item.setSizeHint(item_widget.sizeHint())  # Define o tamanho do item com base no tamanho do widget
        item.task_text = task_text
        self.ui.minhaLista_listWidget.addItem(item)
        self.ui.minhaLista_listWidget.setItemWidget(item, item_widget)

        # Conecta o botão de remover à função de remoção
        remove_button.clicked.connect(lambda: self.delete_task(item))

        # Conecta o botão de editar à função de edição
        edit_button.clicked.connect(lambda: self.edit_task(item))

        self.ui.lineEdit_AddingItem.clear()
        self.ui.minhaLista_listWidget.setCurrentItem(None)

    def save_task_on_db(self):
        """
        Salva as tarefas da lista da interface gráfica, conforme as adiciona, em um banco de dados sqlite.
        """
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        # Exclui tudo na tabela do banco de dados
        c.execute('DELETE FROM tasks;',)

        # Cria lista em branco para armazenar itens de tarefas
        items = []
        # Percorre a lista e retira cada item
        for index in range(self.ui.minhaLista_listWidget.count()):
            items.append(self.ui.minhaLista_listWidget.item(index))

        for item in items:
            # Adiciona as coisas na tabela
            c.execute("INSERT INTO tasks VALUES (:item)", {'item': item.task_text,})

        conn.commit()
        conn.close()

    def grab_all(self):
        """
        Recupera os dados do banco e preenche a lista com esses dados.
        """
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        c.execute("SELECT * FROM tasks")
        records = c.fetchall()

        conn.commit()
        conn.close()

        # Faz loop através de registros e adiciona à tela
        for record in records:
            self.ui.minhaLista_listWidget.addItem(str(record))

    def edit_task(self, item):
        """
        Edita uma tarefa da lista.
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

            conn = sqlite3.connect('tasks.db')
            c = conn.cursor()
            c.execute("UPDATE tasks SET list_item = ? WHERE list_item = ?", (new_text, current_text))
            conn.commit()
            conn.close()

            self.ui.minhaLista_listWidget.setCurrentItem(None)

    def delete_task(self, item):
        """
        Remove uma tarefa da lista.
        """
        confirm = QMessageBox.question(self.ui.centralwidget, "Confirmar", "Tem certeza que deseja remover esta tarefa?")
        if confirm == QMessageBox.Yes:
            text = item.task_text

            conn = sqlite3.connect('tasks.db')
            c = conn.cursor()
            c.execute("DELETE FROM tasks WHERE list_item = ?", (text,))
            conn.commit()
            conn.close()

            self.ui.minhaLista_listWidget.takeItem(self.ui.minhaLista_listWidget.row(item))

    def search_task(self):
        """
        Busca uma tarefa na lista.
        """
        task_text = self.ui.lineEdit_SearchItem.text()
        if task_text == "":
            QMessageBox.warning(self.ui.centralwidget, "Aviso", "Por favor, digite uma tarefa para buscar.")
            return
        
        for index in range(self.ui.minhaLista_listWidget.count()):
            item = self.ui.minhaLista_listWidget.item(index)
            item_widget = self.ui.minhaLista_listWidget.itemWidget(item)
            task_label = item_widget.findChild(QLabel)

            if task_text in task_label.text():
                self.ui.minhaLista_listWidget.setSelectionMode(QAbstractItemView.SingleSelection)
                self.ui.minhaLista_listWidget.setCurrentItem(item)
                self.ui.minhaLista_listWidget.scrollToItem(item)
                return

        QMessageBox.information(self.ui.centralwidget, "Informação", "A tarefa não foi encontrada.")

    def clear_search_input(self):
        """
        Limpa o texto do input de pesquisa quando adiciona uma tarefa.
        """
        self.ui.lineEdit_SearchItem.clear() # Limpa o texto em si
        self.ui.minhaLista_listWidget.clearSelection() # Limpa a seleção do texto
        self.ui.minhaLista_listWidget.setSelectionMode(QAbstractItemView.NoSelection) # Valor padrão (sem seleção)

if __name__ == "__main__":
    app = QApplication([])

    # Carrega as estilizações
    with open("styles.qss", "r") as f:
        qss = f.read()
        app.setStyleSheet(qss)

    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    lista = ListaTodo(ui)
    window.show()
    app.exec_()