# Configurando paquetes necesarios 

> (!) Esta guía se creo para ser utilizada Debian o Raspbian Jessie y posiblemente Ubuntu (No lo probé)
> (!) Puedes utilizar apt-get en lugar de aptitude (gusto personal)
> (!) A partir de ahora todos los comandos se ejecutaran en el entorno virtual, por lo que podemos usar pip y python en lugar de pip3 o python3

## Instalar herramientas

###1. Instalar Prolog

- SWI-Prolog (Implementación de prolog más usada)

```bash
sudo aptitude install swi-prolog
```

###2. Instalar PYSWIP

- PySWIP (Librería que permite interactuar con SWI-Prolog desde Python, no esta muy actualizada ni tiene mucha documentación, pero es la más reciente de las que existen, tampoco tiene soporte para Python 3 :c )

Nos movemos a nuestro virualenv
```bash
surce venvs/ProyectoFinal/bin/activate
```

Instalamos la libreria
```bash
pip install pyswip_alt
```

> *Referencias:*
> - https://github.com/yuce/pyswip

-------------------------------------------------------------------------------------------------------------------

## Configuración

Para modificar estos archivos se requiere algo de conocimientos en Prolog, recomiendo [*Adventure in Prolog*](http://www.amzi.com/AdventureInProlog/advtop.php)
pero hay que tomar en cuenta que no usa SWI-Prolog

### bdc.pl
Es la base de conocimientos del sistema, en este archivo se encuentran los objetos, su tipo, el pin al que están conectados en el registro de corrimiento, su estado,
el cuarto en que se encuentran.

### predicados.pl
En este archivo se encuentran las "acciones" que se pueden realizar sobre los objetos en la base de conocimiento, por lo que este archivo consulta a *bdc.pl* y este
a es consultado por PySWIP en el archivo principal *Neuralog.py*.
