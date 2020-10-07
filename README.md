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

# Ejecutar script

```python
python main.py
```

Al ejecutar el script se pedirá el siguiente listado de datos:

* la URI absoluta del vídeo. 
* El lenguaje del vídeo.
* El idioma original.
* El idioma destino a traducir.

El script generará el transcribe, translate y los subtitulos del vídeo.

Todos los archivos generados serán almancenados en el mismo bucket donde se encuentra el video. Esto con los siguientes prefijos.

* _transcribe
* _translate
* _subtitles

Los subtitulos de igual manerá serán almacenados en la maquina local, en la carpeta tmp.