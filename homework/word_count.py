"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os.path
from itertools import groupby


#
# Escriba la función load_input que recive como parámetro un folder y retorna
# una lista de tuplas donde el primer elemento de cada tupla es el nombre del
# archivo y el segundo es una línea del archivo. La función convierte a tuplas
# todas las lineas de cada uno de los archivos. La función es genérica y debe
# leer todos los archivos de folder entregado como parámetro.
#
# Por ejemplo:
#   [
#     ('text0'.txt', 'Analytics is the discovery, inter ...'),
#     ('text0'.txt', 'in data. Especially valuable in ar...').
#     ...
#     ('text2.txt'. 'hypotheses.')
#   ]
#
def load_input(input_directory:str)->list:
    """Funcion load_input
    params:
        input_directory: str
    return: 
        list_files: list[tuple]
    """

    list_files: list = []
    for file in glob.glob(f"{input_directory}/*.txt"):
        with open(file, "r") as file:
            for line in file:
                list_files.append((os.path.basename(file.name), line))
    
    return list_files


#
# Escriba la función line_preprocessing que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). Esta función
# realiza el preprocesamiento de las líneas de texto,
#
def line_preprocessing(sequence:list[tuple]) -> list[tuple]:
    """Line Preprocessing
    params:
        sequence: list[tuple]
    return: 
        list_preprocessed: list[tuple]
    """

    preprocessing = lambda x: x.lower().replace(",", "").replace(".", "").replace(":", "").replace(";", "").replace("!", "").replace("?", "")
    list_preprocessed: list = []

    for folder, line in sequence:
        list_preprocessed.append((folder, preprocessing(line)))
    
    return list_preprocessed


#
# Escriba una función llamada maper que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). En este caso,
# la clave es cada palabra y el valor es 1, puesto que se está realizando un
# conteo.
#
#   [
#     ('Analytics', 1),
#     ('is', 1),
#     ...
#   ]
#
def mapper(sequence) -> list[tuple]:
    """Mapper
    params:
        sequence: list
    return: 
        words_count: list[tuple]
    """

    words_count: list = []

    for _, line in sequence:
        for word in line.split():
            words_count.append((word, 1))
    return words_count



#
# Escriba la función shuffle_and_sort que recibe la lista de tuplas entregada
# por el mapper, y retorna una lista con el mismo contenido ordenado por la
# clave.
#
#   [
#     ('Analytics', 1),
#     ('Analytics', 1),
#     ...
#   ]
#
def shuffle_and_sort(sequence) -> list[tuple]:
    """Shuffle and Sort
    params:
        sequence: list[tuple]
    return: 
        list[tuple]
    """

    return sorted(sequence)


#
# Escriba la función reducer, la cual recibe el resultado de shuffle_and_sort y
# reduce los valores asociados a cada clave sumandolos. Como resultado, por
# ejemplo, la reducción indica cuantas veces aparece la palabra analytics en el
# texto.
#
def reducer(sequence) -> list[tuple]:
    """Reducer
    params:
        sequence: list
    return: 
        list_reducer: list[tuple]
    """
    
    list_reducer: list = []

    for key, group in groupby(sequence, lambda x: x[0]):
        list_reducer.append((key, sum([value for _, value in group])))
    
    return list_reducer


#
# Escriba la función create_ouptput_directory que recibe un nombre de
# directorio y lo crea. Si el directorio existe, lo borra
#
def create_ouptput_directory(output_directory) -> None:
    """Create Output Directory
    params:
        output_directory: str
    return:
        output_directory: None
    """
    
    if os.path.exists(output_directory):
        os.system(f"rm -Rf {output_directory}")
        
    os.mkdir(output_directory)

    return None

#
# Escriba la función save_output, la cual almacena en un archivo de texto
# llamado part-00000 el resultado del reducer. El archivo debe ser guardado en
# el directorio entregado como parámetro, y que se creo en el paso anterior.
# Adicionalmente, el archivo debe contener una tupla por línea, donde el primer
# elemento es la clave y el segundo el valor. Los elementos de la tupla están
# separados por un tabulador.
#
def save_output(output_directory, sequence):
    """Save Output
    params:
        output_directory: str
        sequence: list
    return: 
        None
    """
    
    with open(f"{output_directory}/part-00000", "w") as file:
        for key, value in sequence:
            file.write(f"{key}\t{value}\n")
    
    return None


#
# La siguiente función crea un archivo llamado _SUCCESS en el directorio
# entregado como parámetro.
#
def create_marker(output_directory) -> None:
    """Create Marker
    params:
        output_directory: str
    return:
        None
    """

    with open(f"{output_directory}/_SUCCESS", "w") as file:
        pass

    return None


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run_job(input_directory, output_directory):
    """Job
    Orchestrator Function
    params:
        input_directory: str
        output_directory: str
    return:
        None
    """
    
    # 1. Create Directory
    create_ouptput_directory(output_directory)
    # 2. Load Texts
    sequence = load_input(input_directory)
    # 3. Preprocessing
    sequence = line_preprocessing(sequence)
    # 4. Maps, order and sort
    sequence = mapper(sequence)
    sequence = shuffle_and_sort(sequence)
    sequence = reducer(sequence)\
    # 5. Save Output
    save_output(output_directory, sequence)
    # 6. Create files
    create_marker(output_directory)

    return None



if __name__ == "__main__":
    run_job(
        "input",
        "output",
    )
