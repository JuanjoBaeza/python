from os import error
import boto3
from botocore.exceptions import ClientError

def obtener_bytes_imagen(ruta_imagen):
    with open(ruta_imagen,'rb') as imagen:
        return imagen.read()

def comparar_rostros(ruta_imagen1, ruta_imagen2):
    imagen1 = obtener_bytes_imagen(ruta_imagen1)
    imagen2 = obtener_bytes_imagen(ruta_imagen2)

    cliente=boto3.client('rekognition')

    try:
        respuesta = cliente.compare_faces(SourceImage={'Bytes': imagen1},
                                          TargetImage={'Bytes': imagen2},
                                          SimilarityThreshold = 0,
                                          QualityFilter = 'AUTO')

        # Quality filter = NONE|AUTO|LOW|MEDIUM|HIGH

        if respuesta and respuesta['ResponseMetadata']['HTTPStatusCode'] == 200:
            # Caras que no alcanzan el 60% de similitud
            for i in respuesta['UnmatchedFaces']:
                print(str(i) + ' \n')
            
            # Caras con silimitud
            for i in respuesta['FaceMatches']:
                q = "%.2f" % i['Similarity']
                print('Similitud: ' + str(q))

    except ClientError as error:
        print('Ocurrió un error al llamar a la API:' + str(error))

if __name__ == "__main__":

    ruta_imagen1 = '/mnt/c/Repo/python/rus1.jpg'
    ruta_imagen2 = '/mnt/c/Repo/python/rus4.jpg'

    comparar_rostros(ruta_imagen1, ruta_imagen2)