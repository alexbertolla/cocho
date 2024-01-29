import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
from skimage import color, img_as_float, img_as_ubyte
from skimage.io import imread, imsave, imshow
from skimage.exposure import equalize_adapthist, rescale_intensity
import numpy as np
from skimage.filters import threshold_multiotsu
import os
from os import path
import shutil
from skimage.filters.rank import entropy
from skimage.morphology import disk, binary_opening, binary_closing, binary_erosion, binary_dilation
import cv2



caminho_origem = '../../2_pre_processamento/3_realce/output_realce/output_equalizacao_adaptativa/output_filtro_nlm/imagens_originais/3'
caminho_local = './imagens_segmentacao_entropia/'
lista_conteudo_origem = os.listdir(caminho_origem)
#print(lista_conteudo_origem)

#limiar_minimo = 7.5
#limiar_maximo = 8.9

limiar_minimo = 0.97
limiar_maximo = 0.999

for diretorio_origem in lista_conteudo_origem:
    #print(diretorio_origem)

    imagem_rgb = img_as_float(imread(caminho_origem + '/' + diretorio_origem))
    imagem_hsv = color.rgb2hsv(imagem_rgb)
    componente_h = imagem_hsv[:, :, 0]
    componente_s = imagem_hsv[:, :, 1]
    componente_v = imagem_hsv[:, :, 2]

    #array_janela = [5, 10]
    array_janela = [20, 25, 30, 35, 40, 45, 50, 55, 60]
    #array_janela = [55, 60, 65, 70, 75]
    # array_janela = [80, 85, 90, 95, 100]






    plt_linha = 4
    plt_coluna = len(array_janela)
    plt_posicao = 1
    figure = pylab.figure(), pylab.clf()
    pylab.get_current_fig_manager().window.attributes('-fullscreen', True)

    for janela_entropia in array_janela:


        imagem_entropia = entropy(img_as_ubyte(componente_v), disk(janela_entropia))
        img = np.array(imagem_entropia, dtype='uint8')

        imagem_entropia = equalize_adapthist(img)
        #imagem_entropia = rescale_intensity(img)
        #imagem_entropia = img_as_float(imagem_entropia)

        imagem_segmentada = np.copy(imagem_rgb)
        imagem_segmentada[(imagem_entropia[:, :] < limiar_minimo) | (imagem_entropia[:, :] >= limiar_maximo)] = 0
        #print(imagem_entropia.shape)

        imagem_segmentada_gray = color.rgb2gray(imagem_segmentada)
        imagem_segmentada_gray[imagem_segmentada_gray > 0] = 1

        im_opening = binary_opening(imagem_segmentada_gray, disk(17))
        im_closing = binary_closing(imagem_segmentada_gray, disk(21))


        #im_opening = img_as_float(im_opening)
        im_opening = img_as_ubyte(im_opening)
        #im_closing = img_as_float(im_closing)
        im_closing = img_as_ubyte(im_closing)

        imagem_segmentada2 = np.copy(imagem_rgb)
        imagem_segmentada2[(im_closing == 0)] = 0

        nome_arquivo = path.splitext(diretorio_origem)[0] + '_' + str(janela_entropia) + \
                       path.splitext(diretorio_origem)[1]
        print(caminho_local + nome_arquivo)
        imsave(caminho_local + nome_arquivo, img_as_ubyte(imagem_segmentada2))

        #cv2.imshow('im_opening', im_opening)
        #cv2.imshow('im_closing', im_closing)
        #cv2.imshow('imagem_segmentada', cv2.cvtColor(img_as_ubyte(imagem_segmentada), cv2.COLOR_RGB2BGR))
        #cv2.imshow('imagem_segmentada2', cv2.cvtColor(img_as_ubyte(imagem_segmentada2), cv2.COLOR_RGB2BGR))
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        #exit()

        #pylab.subplot(plt_linha, plt_coluna, plt_posicao)
        #pylab.axis('off')
        #pylab.title('Janela=' + str(janela_entropia))
        #pylab.imshow(imagem_entropia)


        #pylab.subplot(plt_linha, plt_coluna, plt_posicao + plt_coluna)
        #pylab.axis('off')
        #pylab.title(str(janela_entropia))
        #pylab.hist(imagem_entropia.flat, bins=100, color='black')
        #pylab.colorbar(orientation="horizontal")

        #pylab.subplot(plt_linha, plt_coluna, plt_posicao + (plt_coluna*2))
        #pylab.axis('off')
        #pylab.title(janela_entropia)
        #pylab.imshow(imagem_segmentada)

        #pylab.subplot(plt_linha, plt_coluna, plt_posicao + (plt_coluna * 3))
        #pylab.axis('off')
        #pylab.title('Fechamento')
        #pylab.imshow(imagem_segmentada2)

        #plt_posicao += 1




    #print('Nome imagem: ' + diretorio_origem)
    #nome_plot = 'plot_' + diretorio_origem.replace('jpg', 'png')
    #print('Nome plot: ' + nome_plot)
    ##pylab.show()

    #pylab.savefig('teste.png')

    #nome_arquivo = str(min(array_janela)) + '_' + str(max(array_janela)) + '_' + path.splitext(diretorio_origem)[0] + '.png'
    #print(caminho_local + nome_arquivo)
    #plt.savefig(caminho_local + nome_arquivo)
    #exit('FIM')



print('FIM')