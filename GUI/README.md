# Configurando paquetes necesarios 

> (!) Esta guía se creo para ser utilizada Debian o Raspbian Jessie y posiblemente Ubuntu (No lo probé)
> (!) Puedes utilizar apt-get en lugar de aptitude (gusto personal)
> (!) A partir de ahora todos los comandos se ejecutaran en el entorno virtual, por lo que podemos usar pip y python en lugar de pip3 o python3

## Instalación de herramientas

### 1. Instalar  librerías y paquetes para la GUI con QT 4

- QT4 Designer (Herramienta que permite la creación de GUIs de forma visual)
- PyQt4 (Bindings para QT4 en Python)

```bash
sudo aptitude install qt4-designer python3-pyqt4 
```

Crear enlace simbólico desde la librería global a nuestro virtualenv
```bash
ln -s /usr/lib/python3/dist-packages/PyQt4/ ~/venvs/ProyectoFinal/lib/python3.4/site-packages/
```

Para 64 bits
```bash
ln -s /usr/lib/python3/dist-packages/sip.cpython-34m-x86_64-linux-gnu.so ~/venvs/ProyectoFinal/lib/python3.4/site-packages/
```

Para 32 bits
```bash
ln -s /usr/lib/python3/dist-packages/sip.cpython-34m-i386-linux-gnu.so ~/venvs/ProyectoFinal/lib/python3.4/site-packages/
```

> *Referencias:*
> - http://pythonforengineers.com/your-first-gui-app-with-python-and-pyqt/
> - https://www.tutorialspoint.com/pyqt/index.htm

-------------------------------------------------------------------------------------------------------------------

## Configuración

- Ejecutar *designer-qt4* puede ser desde terminal
- Abrir el archivo *gui.ui*
- Modificar al gusto conservando los nombres de los elementos para evitar editar el archivo principal *Neuralog.py*
- Este archivo será cargado desde PyQt en el archivo principal, toda la lógica se encuentra en ese archivo mientras toda la parte gráfica en el archivo .ui
