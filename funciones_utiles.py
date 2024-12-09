"""
Módulo con funciones útiles para el manejo de archivos y directorios.
"""

import re

def tamanio_a_bytes(tamanio_formateado):
    """
    Convierte una cadena de tamaño formateado (ej. "117.74 MB") a su valor en bytes.

    Args:
        tamanio_formateado (str): Tamaño en formato de cadena con sufijo (ej. "1.5 GB").

    Returns:
        int: El tamaño convertido a bytes.

    Raises:
        ValueError: Si el formato de entrada no es válido.
    """
    # Quitar espacios, convertir a mayúsculas, y eliminar la letra "B" si existe
    tamanio_formateado = tamanio_formateado.replace(" ", "").upper().replace("B", "")

    # Diccionario de sufijos y su potencia de 1024 correspondiente
    sufijos = {"K": 1, "M": 2, "G": 3, "T": 4, "P": 5}

    # Recorrer el diccionario para encontrar el sufijo que coincida al final de la cadena
    for sufijo, potencia in sufijos.items():
        if tamanio_formateado.endswith(sufijo):
            # Extraer la parte numérica y convertirla a float
            valor = float(tamanio_formateado[:-len(sufijo)])
            # Calcular el tamaño en bytes usando la potencia de 1024
            return int(valor * (1024 ** potencia))

    # Si no hay sufijo (es decir, el valor está en bytes), convertir directamente
    return int(float(tamanio_formateado))

def tamanio_a_gb(tamanio_bytes):
    """
    Convierte un tamaño en bytes a su valor en gigabytes.

    Args:
        tamanio_bytes (int): Tamaño en bytes.

    Returns:
        float: El tamaño convertido a gigabytes.
    """
    return tamanio_bytes / (1024 ** 3)

def buscar_prefijo(numero):
    """Busca el prefijo del número de celular"""
    return numero[:2]

def validar_numero(numero):
    """Valida si el número de celular es válido"""
    from central import Central
    
    formato = r'^\d{2} \d{8}$'
    if bool(re.match(formato, numero)):
        if numero[:2] in Central.centrales:
            return True
    return False
