from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, 
                            QLineEdit, QAction)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys

class MiniBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Browser")
        self.setGeometry(100, 100, 800, 600)
        
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://secure.covendis.com/cov/covendis.htm"))
        self.setCentralWidget(self.browser)
        
        # Navigation bar
        nav_bar = QToolBar()
        self.addToolBar(nav_bar)
        
        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.browser.back)
        nav_bar.addAction(back_btn)
        
        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(self.browser.forward)
        nav_bar.addAction(forward_btn)
        
        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        nav_bar.addAction(reload_btn)
        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)
        
        self.browser.urlChanged.connect(self.update_url)
    
    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        self.browser.setUrl(QUrl(url))
    
    def update_url(self, q):
        self.url_bar.setText(q.toString())

app = QApplication(sys.argv)
window = MiniBrowser()
window.show()
sys.exit(app.exec_())
