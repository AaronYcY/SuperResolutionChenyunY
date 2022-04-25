import os

import cv2
import numpy as np
from PyQt5 import QtGui, QtWidgets
from tensorflow import keras

import config
import utils
from interfaces.UI_SR_ResDialog import Ui_SR_Results


class SRDialog(Ui_SR_Results, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SRDialog, self).__init__()
        self.setupUi(self)

        self._srcnn_model = keras.models.load_model(config.SRCNN_MODEL_PATH)
        self._srgan_model = keras.models.load_model(config.SRGAN_MODEL_PATH)
        print(config.ESRGAN_MODEL_PATH)
        self._esrgan_model = keras.models.load_model(config.ESRGAN_MODEL_PATH)
        self._lr_image = None
        self._hr_image = None
        self._bic_image = None
        self._srcnn_image = None
        self._srgan_image = None
        self._esrgan_image = None

        self.startButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.selLRButton.clicked.connect(self.select_LR_picture_and_show)
        self.selHRButton.clicked.connect(self.select_HR_picture_and_show)
        self.startButton.clicked.connect(self.start_calculate)
        self.saveButton.clicked.connect(self.save_results)

    def start_calculate(self):
        if self._lr_image is not None:
            width = self._lr_image.shape[1]
            height = self._lr_image.shape[0]

            if width == config.IMAGE_LR_WIDTH and height == config.IMAGE_LR_HEIGHT:
                self._bic_image = cv2.resize(self._lr_image, dsize=(height * config.DOWN_SCALE, width * config.DOWN_SCALE),
                                        interpolation=cv2.INTER_CUBIC)
                cvRGBImg = cv2.cvtColor(self._bic_image, cv2.COLOR_BGR2RGB)
                qimage = QtGui.QImage(cvRGBImg.data, cvRGBImg.shape[1], cvRGBImg.shape[0], QtGui.QImage.Format_RGB888)
                p = QtGui.QPixmap(qimage)
                self.BicViewer.setPixmap(p)
                self.BicViewer.setScaledContents(True)

                self._srcnn_image = self._srcnn_model.predict(np.asarray([utils.normalize_image(self._bic_image)]))[0]
                self._srcnn_image = utils.normalized_array_to_image(self._srcnn_image)
                cvRGBImg = cv2.cvtColor(self._srcnn_image, cv2.COLOR_BGR2RGB)
                qimage = QtGui.QImage(cvRGBImg.data, cvRGBImg.shape[1], cvRGBImg.shape[0], QtGui.QImage.Format_RGB888)
                p = QtGui.QPixmap(qimage)
                self.SRCNNViewer.setPixmap(p)
                self.SRCNNViewer.setScaledContents(True)

                self._srgan_image = self._srgan_model.predict(np.asarray([utils.normalize_image(self._lr_image)]))[0]
                self._srgan_image = utils.normalized_array_to_image(self._srgan_image)
                cvRGBImg = cv2.cvtColor(self._srgan_image, cv2.COLOR_BGR2RGB)
                qimage = QtGui.QImage(cvRGBImg.data, cvRGBImg.shape[1], cvRGBImg.shape[0], QtGui.QImage.Format_RGB888)
                p = QtGui.QPixmap(qimage)
                self.SRGANViewer.setPixmap(p)
                self.SRGANViewer.setScaledContents(True)

                self._esrgan_image = self._esrgan_model.predict(np.asarray([utils.normalize_image(self._lr_image)]))[0]
                self._esrgan_image = utils.normalized_array_to_image(self._esrgan_image)
                cvRGBImg = cv2.cvtColor(self._esrgan_image, cv2.COLOR_BGR2RGB)
                qimage = QtGui.QImage(cvRGBImg.data, cvRGBImg.shape[1], cvRGBImg.shape[0], QtGui.QImage.Format_RGB888)
                p = QtGui.QPixmap(qimage)
                self.ESRGANViewer.setPixmap(p)
                self.ESRGANViewer.setScaledContents(True)

                self.saveButton.setEnabled(True)
            else:
                QtWidgets.QMessageBox.warning(self, "Warning", "Only support %d * %d LR pictures." \
                                              % (config.IMAGE_LR_HEIGHT, config.IMAGE_LR_WIDTH),
                                              QtWidgets.QMessageBox.Ok)
                self.LRViewer.clear()
                self.clear_res_viewers()


    def select_HR_picture_and_show(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(parent=self, directory="TestSet")
        if fname[0]:
            self.img_path = fname[0]
            p = QtGui.QPixmap()
            p.load(fname[0])
            self._hr_image = utils.read_image(fname[0])
            self.HRViewer.setPixmap(p)
            self.HRViewer.setScaledContents(True)
        else:
            self.HRViewer.clear()

    def select_LR_picture_and_show(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(parent=self, directory="TestSet")
        if fname[0]:
            self.img_path = fname[0]
            p = QtGui.QPixmap()
            p.load(fname[0])
            self._lr_image = utils.read_image(fname[0])
            self.LRViewer.setPixmap(p)
            self.LRViewer.setScaledContents(True)
            self.startButton.setEnabled(True)
            self.saveButton.setEnabled(False)
            self.clear_res_viewers()
        else:
            self.startButton.setEnabled(False)
            self.LRViewer.clear()
            self.clear_res_viewers()

    def has_correct_suffix(self, file_name: str):
        for suffix in config.IMAGE_SUFFIXS:
            if file_name.endswith(suffix):
                return True
        return False


    def save_results(self):
        if not os.path.exists("Res"):
            os.mkdir("Res")
        fname = QtWidgets.QFileDialog.getSaveFileName(self, "Save Result",
                                                      directory="Res/res.jpg", filter="*.jpg, *.png")
        if fname[0] and self.has_correct_suffix(fname[0]):
            save_path = fname[0]
            save_image = utils.concat_images_horizontal([
                self._bic_image,
                self._srcnn_image,
                self._srgan_image,
                self._esrgan_image]
            )
            print("save result as", os.path.join("Res", save_path))
            cv2.imwrite(os.path.join("Res", save_path), save_image)
        else:
            QtWidgets.QMessageBox.warning(self, "Warning",
                                          "Please select appropriate filename:\nmust end with jpg or png.",
                                          QtWidgets.QMessageBox.Ok)

    def clear_res_viewers(self):
        self.HRViewer.clear()
        self.BicViewer.clear()
        self.SRCNNViewer.clear()
        self.SRGANViewer.clear()
        self.ESRGANViewer.clear()

