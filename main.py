# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
import sys
import shutil
import qrcode
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QMessageBox
from PIL import Image
from ui import Ui_MainWindow
from tempfile import TemporaryFile


def generate_qrcode(data, preview, output):
    box_size = 10 if preview == True else 1
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=0,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # generate qrcode
    img = qr.make_image()
    img.save(output)
    # img.show()


def load_image(img_path):
    im = Image.open(img_path)
    # im.show()

    arr = np.array(im)
    return arr


def image_to_coordinate(arr):
    width, height = len(arr[0]), len(arr)
    print("width=", width)
    print("height=", height)
    result_arr = []
    for row_index, row in enumerate(arr):
        row_arr = []
        for col_index, col in enumerate(arr[row_index]):
            if not col:
                row_arr.append(col_index + 1)
        print("row_index={} details: ".format(row_index + 1), ", ".join([str(loc) for loc in row_arr]))
        result_arr.append(row_arr)
    # 返回坐标
    return result_arr

def paint(arr, output):
    x1, x2 = 0, len(arr[0])
    y1, y2 = 0, len(arr[0])

    print("x1={}, x2={}, y1={}, y2={}".format(x1, x2, y1, y2))

    ax = plt.gca()
    ax.set_xlim(x1, x2)
    xmiloc = plt.MultipleLocator(1)
    xmaloc = plt.MultipleLocator(1)
    # ax.xaxis.set_minor_locator(xmiloc)
    ax.xaxis.set_major_locator(xmaloc)
    ax.grid(axis='x', linestyle='-.', linewidth=1, color='r', alpha=0.4, which='major')

    ay = plt.gca()
    ay.set_ylim(y1, y2)
    ymiloc = plt.MultipleLocator(1)
    ymaloc = plt.MultipleLocator(1)
    # ay.yaxis.set_minor_locator(ymiloc)
    ay.yaxis.set_major_locator(ymaloc)
    ay.grid(axis='y', linestyle='-.', linewidth=1, color='r', alpha=0.4, which='major')

    plt.xlabel("COLUMN")
    plt.ylabel("ROW")
    plt.title("Manual QR Code")
    plt.savefig(output)
    # plt.show()



class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._init_variables()
        self._bind_actions()

    def _init_variables(self):
        self.qrcode_img_path_preview = './qrcode_preview.png'
        self.qrcode_img_path = './qrcode.png'
        self.output_img_path = './output.png'
        self.output_steps = []

    def _bind_actions(self):
        # 绑定按钮点击事件
        self.previewBtn.clicked.connect(self._preview_qrcode)
        self.exportBtn.clicked.connect(self._export_axis)

        # 输入框文本变化时
        self.lineEdit.textChanged.connect(self._text_changed)

    def _text_changed(self):
        img_path = self.qrcode_img_path_preview
        msg = self.lineEdit.text()
        generate_qrcode(msg, True, img_path)

        # 实时预览
        pix = QPixmap(img_path)
        self.label_image.setGeometry(220, 210, 300, 300)
        self.label_image.setStyleSheet("border: 1px dash grey")
        self.label_image.setPixmap(pix)


    def _preview_qrcode(self):
        msg = self.lineEdit.text()
        # img_path = "./qrcode.png"
        img_path = self.qrcode_img_path
        generate_qrcode(msg, False, img_path)
        raw_arr = load_image(img_path)
        arr = image_to_coordinate(raw_arr)
        self.output_steps = arr

        output = self.output_img_path
        paint(raw_arr, output)
        # 回显坐标图
        pix = QPixmap(output)
        # pix.scaledToWidth(280)
        # pix.scaledToHeight(280)
        self.label_image.setGeometry(220, 210, 300, 300)
        self.label_image.setScaledContents(True)
        self.label_image.setStyleSheet("border: 1px dash grey")
        self.label_image.setPixmap(pix)



    def _export_axis(self):
        # 选择输出位置
        output, ok2 = QFileDialog.getSaveFileName(None, "文件保存", "~/")
        print(output)  # 打印保存文件的全部路径（包括文件名和后缀名）
        msg = "手工二维码绘制步骤如下:\n\n"
        for row_index, row in enumerate(self.output_steps):
            line = "第{}行：".format(row_index+1) + ",  ".join([str(item) for item in row])
            msg += line + "\n"
        shutil.copy(self.output_img_path, output)
        QMessageBox.information(self, "绘制步骤", msg, QMessageBox.Yes, QMessageBox.Yes)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # iconPath = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'gastric.icns')
    # app.setWindowIcon(QIcon(iconPath))
    win = Main()
    win.setWindowTitle("手工二维码工具🔧")
    win.show()
    sys.exit(app.exec_())

