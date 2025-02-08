# trading-algoritmico
Algoritmo para la automatización de ordenes en trading


## Utiliza venv
venv es un módulo que viene incluido por defecto con Python 3,
por lo que no es necesario instalarlo de forma separada


## Creación del entorno virtual
    
1. Abre la terminal y navega hasta el directorio de tu proyecto.

2. Ejecuta el siguiente comando para crear un entorno virtual llamado "env"

`python -m venv env`

> Este comando creará un directorio llamado env (si no existe)
que contendrá una copia del intérprete de Python y varios archivos
de soporte.

## Activación del entorno virtual

> Antes de instalar paquetes en tu entorno virtual, debes activarlo

* **En Linux/Mac:**
`source env/bin/activate`
  
* **En Windows:**
`.\env\Scripts\activate`

> Cuando hayas terminado de trabajar en el entorno virtual, puedes desactivarlo ejecutando el siguiente comando:

`deactivate`

## Instalar las dependencias 'requirements.txt'
* **Ejecuta el siguiente comando**
``pip install -r requirements.txt``
    