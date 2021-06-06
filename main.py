from PyQt5 import QtWidgets, uic, QtCore
from downloader import Downloader
import sys, re

class MyThread(QtCore.QThread):
    
    mysignal = QtCore.pyqtSignal(str)
    
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.url = ""

    def my_hook(self, d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')
        if d['status'] == 'downloading':
            p = d['_percent_str']
            p = p.replace('%','')
            self.mysignal.emit(p)
            print(d['filename'], d['_percent_str'], d['_eta_str'])

    def run(self):
        Downloader.download(self, self.url)

class downloaderApp(QtWidgets.QMainWindow):

    def __init__(self):
        super(downloaderApp, self).__init__() # Call the inherited classes __init__ method
        self.ui = uic.loadUi('ui.ui', self) # Load the .ui file`
        self.ui.show()
        self.ui.progressBar.setVisible(False)
        self.mythread = MyThread() # Создаем экземпляр класса
        self.mythread.url = ""
        self.ui.downloadUrl.clicked.connect(self.on_clicked)
        self.mythread.started.connect(self.on_started)
        self.mythread.finished.connect(self.on_finished)
        self.mythread.mysignal.connect(self.on_change, QtCore.Qt.QueuedConnection)

    def on_clicked(self):
        self.mythread.url = self.ui.lineEdit.text()
        result = re.match(r'(http:|https:)?(\/\/)?(www\.)?(youtube.com|youtu.be)\/(watch|embed)?(\?v=|\/)?(\S+)?', self.mythread.url)
        if not result == None:
            self.ui.downloadUrl.setDisabled(True) # Делаем кнопку неактивной
            self.mythread.start() # Запускаем поток
        else:
            pass # TODO Need wrong url animation
    
    def on_started(self): # Вызывается при запуске потока
        if not self.ui.progressBar.isVisible():
            self.ui.progressBar.setVisible(True)
    
    def on_finished(self): # Вызывается при завершении потока
        self.ui.downloadUrl.setDisabled(False) # Делаем кнопку активной
        self.ui.progressBar.setVisible(False)
        self.ui.progressBar.setValue(0)
        #self.ui.lineEdit.setPlaceholderText("Paste youtube link here...")

    def on_change(self, p):
        self.ui.progressBar.setValue(float(p))

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = downloaderApp()  # Создаём объект класса ExampleApp
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':
    main()