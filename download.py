from project.common import download_file

if __name__ == '__main__':

    bucket = input('Ingresa el nombre de tu bucket: ')
    mediafile_key = input('Ingresa el nombre del archivo a descargar: ')
    local_path = input('Dirección de descarga: ')

    download_file(bucket, mediafile_key, local_path)

    