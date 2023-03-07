import io
import sys
import folium

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets


class mapWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initMap()

    def initMap(self):
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.lay = QtWidgets.QHBoxLayout()
        self.setMinimumSize(100, 200)
        
        self.lay.addWidget(self.view, stretch=1)
        self.setLayout(self.lay)


    def update(self,lat=0,lon=0):
        m = folium.Map(location=[lat, lon], zoom_start=10
        )
        data = io.BytesIO()
        folium.Marker(
            location=[lat,lon],
            icon=folium.DivIcon(html=f"""
                <div><svg>
                    <circle cx="50" cy="50" r="4" fill="#000000" opacity="1"/>
                    </svg></div>""")
                ).add_to(m)
        m.save(data, close_file=False)

        self.view.setHtml(data.getvalue().decode())
        self.lay.removeWidget(self.view)
        self.lay.addWidget(self.view)
