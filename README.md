# Smart-Image-Resize

Smart-Image-Resize es un script de Python que permite modificar la relación de aspecto (ancho) de una imagen sin deformarla o perder información relevante.

El script utiliza el algoritmo Seam Carving. Este algoritmo permite encontrar las costuras mínimas (pixeles adyacentes de mínima energía). Una vez calculada la costura mínima ésta puede eliminarse o duplicarse con el objetivo de disminuir o aumentar, respectivamente, el ancho de la imagen.

## Dependendias
Probado con python 3.6

```bash
numpy
scipy
cv2
```

## Uso

```
$ python main.py --image/-i [path to image] --num/-n [columns to add/remove] --mode/-m [add/remove] --out/-o [output file path]
```

## Ejemplo

Disminución y ampliación de una imagen con un factor de 100 píxeles de ancho:

```
$ python main.py -i img_original.jpg -n 100 -m remove -o img_reducida.jpg
```

```
$ python main.py -i img_original.jpg -n 100 -m add -o img_ampliada.jpg
```

![imagen original](/images/img_original.jpg)

**Imagen original: 427 x 640**

![imagen reducida](/images/img_reducida.jpg)

**Imagen reducida: 427 x 540**

![imagen ampliada](/images/img_ampliada.jpg)

**Imagen ampliada: 427 x 740**

## Referencias

Basado en la documentación de Antonio Tabernero Galán, departamento de Lenguajes y Sistemas Informáticos e Ingeniería de Software, Escuela Técnica Superior de Ingenieros Informáticos, Universidad Politécnica de Madrid.

## License

[GNU-GPL](https://www.gnu.org/licenses/gpl-3.0-standalone.html)
