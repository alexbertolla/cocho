import cv2
import matplotlib
from matplotlib import pyplot as plt
from skimage.filters.rank import entropy
from skimage.morphology import disk, binary_opening, binary_closing, binary_erosion, binary_dilation


cocho = cv2.imread("cocho.jpeg")
recorte_cocho = cv2.imread("recorte_cocho.jpeg")

cocho_lab = cv2.cvtColor(cocho, cv2.COLOR_BGR2Lab)
cocho_l, cocho_a, cocho_b = cv2.split(cocho_lab)

cocho_hsv = cv2.cvtColor(cocho, cv2.COLOR_BGR2HSV)
cocho_h, cocho_s, cocho_v = cv2.split(cocho_hsv)

recorte_cocho_lab = cv2.cvtColor(recorte_cocho, cv2.COLOR_BGR2Lab)
recorte_cocho_l, recorte_cocho_a, recorte_cocho_b = cv2.split(recorte_cocho_lab)

recorte_cocho_hsv = cv2.cvtColor(recorte_cocho, cv2.COLOR_BGR2HSV)
recorte_cocho_h, recorte_cocho_s, recorte_cocho_v = cv2.split(recorte_cocho_hsv)



l = 4
c = 2


imagem_processar = recorte_cocho_s

plt.figure()

plt.subplot(l, c, 1)
plt.axis("off")
plt.title("Imagem Recorte Cocho")
#plt.imshow(cv2.cvtColor(recorte_cocho, cv2.COLOR_BGR2RGB))
plt.imshow(imagem_processar, cmap="gray")

array_janela = [5, 10, 15, 20, 25, 30, 35] #20, 25,
for p, janela_entropia in enumerate(array_janela):
    print(p)
    recorte_cocho_h_entropia = entropy(imagem_processar, disk(janela_entropia))

    plt.subplot(l, c, p+2)
    plt.axis("off")
    plt.title("Imagem Recorte Cocho (" + str(janela_entropia) + ")")
    plt.imshow(recorte_cocho_h_entropia, cmap="gray")


plt.show()





print("FIM")

