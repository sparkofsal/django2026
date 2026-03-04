# ==========================================================
# Segunda etapa.py
# Proyecto: Videos ASM - Avance 2 (POO)
# Requisitos del PDF:
# - Clase Persona (nombre, nómina) con métodos capturar e imprimir
# - Clase Videos (nombre, extensión, tamaño) con métodos capturar e imprimir
# - Mantener funcionalidad de Avance 1:
#   nómina, nombre, cantidad videos, confirmación SI/NO,
#   y si SI: capturar N videos (incluye título), validaciones y salida.txt
# - Guardar TODO en salida.txt en UNA sola línea separado por " | "
# ==========================================================

import re


# --------------------------
# Validaciones (funciones de apoyo)
# --------------------------

def validar_no_vacio(texto: str, campo: str) -> str:
    valor = texto.strip()
    if not valor:
        raise ValueError(f"Error: {campo} no puede estar vacío.")
    return valor


def validar_nomina(entrada: str) -> str:
    valor = validar_no_vacio(entrada, "Nómina")
    if not re.fullmatch(r"[A-Za-z0-9]+", valor):
        raise ValueError("Error: Nómina debe ser alfanumérica (solo letras y números, sin espacios).")
    return valor


def validar_nombre_persona(entrada: str) -> str:
    valor = validar_no_vacio(entrada, "Nombre")
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+", valor):
        raise ValueError("Error: Nombre debe contener solo letras y espacios (sin números ni símbolos).")
    valor = re.sub(r"\s+", " ", valor).strip()
    return valor


def validar_entero_positivo(entrada: str, campo: str) -> int:
    valor = validar_no_vacio(entrada, campo)
    try:
        n = int(valor)
    except ValueError:
        raise ValueError(f"Error: {campo} debe ser numérico (entero).")
    if n <= 0:
        raise ValueError(f"Error: {campo} debe ser mayor que 0.")
    return n


def confirmar_si_no(entrada: str) -> str:
    valor = validar_no_vacio(entrada, "Confirmación").upper().strip()
    valor = valor.replace("Í", "I")  # normaliza SÍ -> SI
    if valor in ("SI", "S"):
        return "SI"
    if valor in ("NO", "N"):
        return "NO"
    raise ValueError("Error: Respuesta inválida. Escribe SI o NO.")


def validar_texto_alfanumerico_con_espacios(entrada: str, campo: str) -> str:
    valor = validar_no_vacio(entrada, campo)
    if not re.fullmatch(r"[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ ]+", valor):
        raise ValueError(
            f"Error: {campo} debe ser alfanumérico (letras/números) y puede incluir espacios, sin símbolos."
        )
    valor = re.sub(r"\s+", " ", valor).strip()
    return valor


def validar_tamano_mb(entrada: str) -> float:
    valor = validar_no_vacio(entrada, "Tamaño (MB)")
    try:
        tam = float(valor)
    except ValueError:
        raise ValueError("Error: Tamaño (MB) debe ser numérico (entero o decimal).")
    if tam <= 0:
        raise ValueError("Error: Tamaño (MB) debe ser mayor que 0.")
    if tam > 3:
        raise ValueError("Error: Tamaño (MB) excede el máximo permitido (3MB).")
    return tam


def pedir_hasta_valido(mensaje: str, funcion_validacion):
    while True:
        try:
            entrada = input(mensaje)
            return funcion_validacion(entrada)
        except ValueError as e:
            print(e)


# --------------------------
# Clases (POO)
# --------------------------

class Persona:
    def __init__(self, nombre: str = "", nomina: str = ""):
        self.nombre = nombre
        self.nomina = nomina

    def capturar(self):
        self.nomina = pedir_hasta_valido(
            "Captura tu nómina (alfanumérico, sin espacios): ",
            validar_nomina
        )
        self.nombre = pedir_hasta_valido(
            "Captura tu nombre (solo letras y espacios): ",
            validar_nombre_persona
        )

    def imprimir(self) -> str:
        return f"NOMINA={self.nomina} | NOMBRE={self.nombre}"


class Videos:
    """
    PDF pide: nombre, extensión, tamaño.
    Para mantener funcionalidad de Avance 1 (que exige título), se conserva 'titulo'.
    """
    def __init__(self, titulo: str = "", nombre: str = "", extension: str = "", tamano: float = 0.0):
        self.titulo = titulo
        self.nombre = nombre
        self.extension = extension
        self.tamano = tamano

    def capturar(self, idx: int, total: int):
        print(f"\n--- Captura de Video {idx} de {total} ---")
        self.titulo = pedir_hasta_valido(
            "Título (alfanumérico, permite espacios): ",
            lambda x: validar_texto_alfanumerico_con_espacios(x, "Título")
        )
        self.nombre = pedir_hasta_valido(
            "Nombre del video (alfanumérico, permite espacios): ",
            lambda x: validar_texto_alfanumerico_con_espacios(x, "Nombre del video")
        )
        self.extension = pedir_hasta_valido(
            "Extensión (alfanumérico, permite espacios): ",
            lambda x: validar_texto_alfanumerico_con_espacios(x, "Extensión")
        )
        self.tamano = pedir_hasta_valido(
            "Tamaño (MB) (numérico, máximo 3MB): ",
            validar_tamano_mb
        )

    def imprimir(self, idx: int) -> str:
        return (
            f"VIDEO{idx}_TITULO={self.titulo} | "
            f"VIDEO{idx}_NOMBRE={self.nombre} | "
            f"VIDEO{idx}_EXTENSION={self.extension} | "
            f"VIDEO{idx}_TAM={self.tamano}"
        )


# --------------------------
# Salida
# --------------------------

def construir_linea_salida(persona: Persona, cant_videos: int, lista_videos: list[Videos]) -> str:
    partes = [
        f"NOMINA={persona.nomina}",
        f"NOMBRE={persona.nombre}",
        f"CANT_VIDEOS={cant_videos}",
    ]
    for i, v in enumerate(lista_videos, start=1):
        partes.append(f"VIDEO{i}_TITULO={v.titulo}")
        partes.append(f"VIDEO{i}_NOMBRE={v.nombre}")
        partes.append(f"VIDEO{i}_EXTENSION={v.extension}")
        partes.append(f"VIDEO{i}_TAM={v.tamano}")
    return " | ".join(partes).strip()


def guardar_salida_txt(linea: str, ruta_archivo: str = "salida.txt") -> None:
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(linea.strip())


# --------------------------
# Programa principal
# --------------------------

def main():
    print("=== Videos ASM | Avance 2 (POO) ===")

    persona = Persona()
    persona.capturar()

    cant_videos = pedir_hasta_valido(
        "Cantidad de videos a registrar (entero): ",
        lambda x: validar_entero_positivo(x, "Cantidad de videos")
    )

    confirmacion = pedir_hasta_valido("¿Deseas registrar los videos? (SI/NO): ", confirmar_si_no)

    videos = []
    if confirmacion == "SI":
        for idx in range(1, cant_videos + 1):
            v = Videos()
            v.capturar(idx, cant_videos)
            videos.append(v)
    else:
        print("\nRegistro cancelado por el usuario (NO). No se capturarán videos.")

    linea = construir_linea_salida(persona, cant_videos, videos)
    guardar_salida_txt(linea, "salida.txt")

    print("\n✅ Datos guardados en salida.txt")
    print("Fin del programa.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error inesperado: {e}")