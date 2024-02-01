import os

import cv2 as cv

from pre_processamento import erosao, dilatacao
from pre_processamento import selecionar_roi, exibir_plot, equalizar_histograma, segmentar_adaptative_gaussian

dir_imagens = '../imanges/'
arquivos = sorted(os.listdir(dir_imagens))
for arquivo in arquivos:
    imagem_original = cv.cvtColor(cv.imread(dir_imagens + arquivo), cv.COLOR_BGR2RGB)

    imagem_roi = selecionar_roi(imagem_original)
    exibir_plot(imagem_original, imagem_roi)

    imagem_equalizada = equalizar_histograma(cv.cvtColor(imagem_roi, cv.COLOR_RGB2GRAY), 3.0, (8, 8))
    # exibir_plot(imagem_roi, imagem_equalizada)

    imagem_segmentada = segmentar_adaptative_gaussian(imagem_equalizada)
    # exibir_plot(imagem_roi, imagem_segmentada)

    imagem_dilatada = dilatacao(imagem_segmentada, (19, 19))
    exibir_plot(imagem_segmentada, imagem_dilatada)

    imagem_erodida = erosao(imagem_dilatada, (11, 11))
    exibir_plot(imagem_dilatada, imagem_erodida)


