from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QColor, QFont

class MyButton(QPushButton):
    def __init__(self, text, color, window_width, window_height):
        super().__init__(text)
        self._color = color
        self.setStyleSheet("background-color: {}".format(self._color))
        self._window_width = window_width
        self._window_height = window_height
        self._font_size = self._calculate_font_size()
        self._font_color = self._calculate_font_color()
        self._font_style = self._calculate_font_style()
        self._update_font()

    def get_color(self):
        return self._color

    def set_color(self, new_color):
        self._color = new_color
        self.setStyleSheet("background-color: {}".format(self._color))
        self._font_color = self._calculate_font_color()
        self._update_font()

    def _calculate_font_size(self):
        # Calculate the font size based on the window size
        min_size = 50
        max_size = 50
        width_ratio = self._window_width / 1980
        height_ratio = self._window_height / 880
        size_ratio = (width_ratio + height_ratio) / 2
        
        #font_size = int(min_size + (max_size - min_size) * size_ratio)
        font_size = 16*width_ratio
        return font_size

    def _calculate_font_color(self):
        font_color = "white"
        return font_color

    def _calculate_font_style(self):
        font_style = "Oswald"
        return font_style

    def _update_font(self):
        font = QFont(self._font_style,self._font_size)
        #font.setPointSize(self._font_size)
        #font.setFamily(self._font_style)
        self.setFont(font)
        self.setStyleSheet("color: {}".format(self._font_color))

    def resizeEvent(self, event):
        # Update the font when the button is resized
        self._window_width = event.size().width()
        self._window_height = event.size().height()
        self._font_size = self._calculate_font_size()
        self._font_color = self._calculate_font_color()
        self._font_style = self._calculate_font_style()
        self._update_font()