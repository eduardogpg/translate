Para generar el subtitulo del vídeo es necesario un par de cosas:

1.- Ingresar la dirección completa del vídeo a generar los subtitulos. Ejemplo:
https://pywombat.s3.us-east-2.amazonaws.com/video.mp4

2.-Ingresa el lenguaje del vídeo. Por ejemplo: es-Es

# Instalación

Crear entono

```python
python -m venv env
```

Iniciar entorno (Unix)

```python
source env/bin/activate
```

Iniciar entorno (Windows)

```python
env\Scripts\activate.bat
```

Instalar dependencias

```python
pip install -r requirements.txt
```

Ejecutar script

```python
python main.py
```

Al ejecutar el script se pedirá la URI absoluta del vídeo y el lenguaje de este.
El script generará el transcribe, translate y los subtitulos (En el idoma original) del vídeo.

Todos los archivos generados serán almancenados en el mismo bucket  donde se encuentra el video.
Por default los subtitulos serán almacenados en la maquina local.