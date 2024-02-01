import cv2 as cv
from matplotlib import pyplot as plt


def exibir_plot(*imagens, cmap='gray'):
    lin = 1
    col = len(imagens)
    plt.figure(figsize=(20, 10))
    for num, imagem in enumerate(imagens):
        plt.subplot(lin, col, num + 1)
        plt.imshow(imagem, cmap=cmap)
    plt.show()


def selecionar_roi(imagem_original):
    return imagem_original[180:350, 10:600]


def equalizar_histograma(imagem_cinza, limit, grid):
    clahe = cv.createCLAHE(clipLimit=limit, tileGridSize=grid)
    return clahe.apply(imagem_cinza)


def segmentar_adaptative_gaussian(imagem_cinza):
    _, seg = cv.threshold(imagem_cinza, 1, 255, cv.THRESH_OTSU)
    return seg


def erosao(imagem_binaria, kernel):
    erosion_size = 9
    shape = cv.MORPH_ELLIPSE
    element = cv.getStructuringElement(shape, kernel, (erosion_size, erosion_size))
    return cv.erode(imagem_binaria, element)


def dilatacao(imagem, kernel):
    dilatation_size = 15
    shape = cv.MORPH_ELLIPSE
    element = cv.getStructuringElement(shape, kernel, (dilatation_size, dilatation_size))
    return cv.dilate(imagem, element)
