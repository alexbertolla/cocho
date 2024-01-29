import cv2
from matplotlib import pyplot as plt



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

plt.figure()

plt.subplot(l, c, 1)
plt.axis("off")
plt.title("Imagem Cocho Original")
plt.imshow(cv2.cvtColor(cocho, cv2.COLOR_BGR2RGB))

plt.subplot(l, c, 2)
plt.axis("off")
plt.title("Imagem Recorte Cocho")
plt.imshow(cv2.cvtColor(recorte_cocho, cv2.COLOR_BGR2RGB))

plt.subplot(l, c, 3)
plt.axis("off")
plt.title("Imagem Cocho A")
plt.imshow(cocho_a, cmap="seismic")

plt.subplot(l, c, 4)
plt.axis("off")
plt.title("Imagem Recorte Cocho A")
plt.imshow(recorte_cocho_a, cmap="seismic")

plt.subplot(l, c, 5)
plt.axis("off")
plt.title("Imagem Cocho B")
plt.imshow(cocho_b, cmap="seismic")

plt.subplot(l, c, 6)
plt.axis("off")
plt.title("Imagem Recorte Cocho B")
plt.imshow(recorte_cocho_b, cmap="seismic")

plt.subplot(l, c, 7)
plt.axis("off")
plt.title("Imagem  Cocho H")
plt.imshow(cocho_h, cmap="hsv")

plt.subplot(l, c, 8)
plt.axis("off")
plt.title("Imagem Recorte Cocho H")
plt.imshow(recorte_cocho_h, cmap="hsv")


plt.show()
plt.close()
print("FIM")
