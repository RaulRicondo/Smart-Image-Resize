import numpy as np
import scipy.ndimage
import cv2
import argparse
import sys

def energia(im):
    im = cv2.normalize(im, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F) # de 0..1 a 0..255
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) # convertir a escala de grises
    im = cv2.normalize(im.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX) # de 0..255 a 0..1
    im_gaus = cv2.GaussianBlur(im,(5,5),1.5) # aplicar filtro gausiano tam 5 y sigma 1.5 a imagen de grises
    E = im_gaus - im
    E = np.absolute(E)*100
    return E

def calcula_M(E):
    alto,ancho = E.shape
    M = float('inf')*E
    for j in range(1,ancho-1):
        M[0,j] = E[0,j]
    for i in range(1,alto):
        for j in range(1,ancho-1):
            M[i,j] = E[i,j] + min([M[i-1,j-1] , M[i-1,j] , M[i-1, j+1]])

    return M

def find_seam(M):
    alto,ancho = M.shape
    s = np.zeros((alto),np.dtype(int))
    min_position = np.where(M[alto-1] == np.amin(M[alto-1]))
    j = min_position[0][0] 
    s[alto-1] = j
    for i in range(alto-1,0,-1):
        rang1 = s[i]-1
        rang2 = s[i]+3
        min_position = np.where(M[i-1] == np.amin(M[i-1][rang1:rang2]))
        s[i-1] = min_position[0][0] 

    return s

def elimina_costura(im,s):
    N,M,C = im.shape
    imout = np.zeros((N,M-1,C))
    for j in range(N):
        aux = im[j][:][:]
        aux = np.delete(aux,s[j], axis=0)
        imout[j,:,:] = aux

    return imout

def aniade_costura(im,s):
    N,M,C = im.shape
    imout = np.zeros((N,M+1,C)) 
    for j in range(N):
        valor_added = np.expand_dims(im[j,s[j]], axis=0)
        aux = np.append(im[j,:s[j]+1],valor_added,axis=0)
        aux = np.append(aux,im[j,s[j]+1:],axis=0)
        imout[j] = aux

    return imout

def reducir_imagen(im_nom,n):
    im = cv2.imread(im_nom)
    try:
        im = cv2.normalize(im.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)
    except:
        sys.exit("La imagen no existe.")
    print("Reduciendo imagen")
    for i in range(n):
        E = energia(im)
        M = calcula_M(E)
        s = find_seam(M)
        im = elimina_costura(im,s)
        cv2.imshow('reducida', im)
        cv2.waitKey(1)

    return im

def ampliar_imagen(im_nom,n):
    im = cv2.imread(im_nom)
    try:
        im = cv2.normalize(im.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)
    except:
        sys.exit("La imagen no existe.")
    print("Ampliando imagen")
    alto,ancho,canales = im.shape
    E = energia(im)
    for i in range(n):
        M = calcula_M(E)
        s = find_seam(M)
        for j in range(alto):
            E[j,s[j]] = E[j,s[j]]*1.5
        im = aniade_costura(im,s)
        cv2.imshow('ampliada', im)
        cv2.waitKey(1)

    return im

# Main
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Image path",type=str)
ap.add_argument("-n", "--num", required = True, help = "Number of columns to add/remove",type=int)
ap.add_argument("-m", "--mode", required = True, help = "Type of operation: add or remove",type=str)
ap.add_argument("-o", "--out", required = True, help = "Output file path",type=str)
args = vars(ap.parse_args())

try:
    int(args["num"])
    if args["num"] < 1:
        sys.exit()
except:
    sys.exit("El número ingresado no es valido")

if (args["mode"] != "add") and (args["mode"] != "remove"):
    sys.exit("El modo ingresado no es valido: usa 'add' o 'remove'")


nombre_imagen = args["image"]
num = args["num"]
mode = args["mode"]
try:
    im_original = cv2.imread(nombre_imagen)
except:
    sys.exit("El path de la imagen no es valido.")

if mode == "add":
    imout = ampliar_imagen(nombre_imagen,num)
    cv2.imshow('ampliada', imout)
else:
    imout = reducir_imagen(nombre_imagen,num)
    cv2.imshow('reducida', imout)

imout = cv2.normalize(imout, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)
cv2.imwrite("imout.jpg", imout)
cv2.imshow('original', im_original)
cv2.waitKey(0)
cv2.destroyAllWindows()