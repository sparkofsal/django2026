# ==========================================================
# Primera etapa.py
# Proyecto: Videos ASM - Avance 1 (Consola + Validaciones + salida.txt)
# Requisitos del PDF:
# - Captura: nómina (alfanumérico), nombre (solo letras), cantidad de videos (numérico)
# - Confirmación Sí/No
# - Si Sí: por cada video capturar título, nombre, extensión (alfanumérico) y tamaño (numérico <= 3MB)
# - Mensajes de error específicos
# - Guardar TODO en salida.txt en UNA sola línea separado por " | "
# ==========================================================

import re


# --------------------------
# Validaciones de entrada
# --------------------------

def validar_no_vacio(texto: str, campo: str) -> str:
    valor = texto.strip()
    if not valor:
        raise ValueError(f"Error: {campo} no puede estar vacío.")
    return valor


def validar_nomina(entrada: str) -> str:
    """
    Nómina: alfanumérico (letras/números) sin símbolos.
    """
    valor = validar_no_vacio(entrada, "Nómina")
    if not re.fullmatch(r"[A-Za-z0-9]+", valor):
        raise ValueError("Error: Nómina debe ser alfanumérica (solo letras y números, sin espacios).")
    return valor


def validar_nombre_persona(entrada: str) -> str:
    """
    Nombre: solo letras y espacios, permite acentos.
    Ejemplos válidos: "José Pérez", "Armando", "Ana Maria"
    """
    valor = validar_no_vacio(entrada, "Nombre")
    # Letras (incluye acentos) + espacios. No permite números ni símbolos.
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+", valor):
        raise ValueError("Error: Nombre debe contener solo letras y espacios (sin números ni símbolos).")
    # Evitar doble espacio al inicio/fin y colapsar espacios múltiples
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
    """
    Acepta: SI, SÍ, S, NO, N (en cualquier combinación de may/min).
    Devuelve "SI" o "NO".
    """
    valor = validar_no_vacio(entrada, "Confirmación").upper().strip()
    # Normalizar acento en "SÍ"
    valor = valor.replace("Í", "I")
    if valor in ("SI", "S"):
        return "SI"
    if valor in ("NO", "N"):
        return "NO"
    raise ValueError("Error: Respuesta inválida. Escribe SI o NO.")


def validar_texto_alfanumerico_con_espacios(entrada: str, campo: str) -> str:
    """
    Alfanumérico con espacios permitido, permite acentos.
    No permite símbolos como /, ., -, etc.
    """
    valor = validar_no_vacio(entrada, campo)
    # Letras/números + espacios + acentos. (sin símbolos)
    if not re.fullmatch(r"[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ ]+", valor):
        raise ValueError(f"Error: {campo} debe ser alfanumérico (letras/números) y puede incluir espacios, sin símbolos.")
    valor = re.sub(r"\s+", " ", valor).strip()
    return valor


def validar_tamano_mb(entrada: str) -> float:
    """
    Tamaño: numérico (permite decimal) y máximo 3MB.
    """
    valor = validar_no_vacio(entrada, "Tamaño (MB)")
    try:
        tam = float(valor)
    except ValueError:
        raise ValueError("Error: Tamaño (MB) debe ser numérico (entero o decimal).")
    if tam <= 0:
        raise ValueError("Error: Tamaño (MB) debe ser mayor que 0.")
    if tam > 3:
        raise ValueError("Error: Tamaño (MB) excede el máximo permitido (3MB).")
    # Redondeo razonable solo para presentación, no cambia la lógica
    return tam


# --------------------------
# Utilidades de captura
# --------------------------

def pedir_hasta_valido(mensaje: str, funcion_validacion):
    while True:
        try:
            entrada = input(mensaje)
            return funcion_validacion(entrada)
        except ValueError as e:
            print(e)


def construir_linea_salida(nomina: str, nombre: str, cant_videos: int, videos: list[dict]) -> str:
    partes = [
        f"NOMINA={nomina}",
        f"NOMBRE={nombre}",
        f"CANT_VIDEOS={cant_videos}",
    ]
    for i, v in enumerate(videos, start=1):
        partes.append(f"VIDEO{i}_TITULO={v['titulo']}")
        partes.append(f"VIDEO{i}_NOMBRE={v['nombre']}")
        partes.append(f"VIDEO{i}_EXTENSION={v['extension']}")
        # Mantener el valor como se capturó (con posible decimal)
        partes.append(f"VIDEO{i}_TAM={v['tamano']}")
    return " | ".join(partes)


def guardar_salida_txt(linea: str, ruta_archivo: str = "salida.txt") -> None:
    # Se escribe UNA sola línea (sin saltos extra)
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(linea.strip())


# --------------------------
# Programa principal
# --------------------------

def main():
    print("=== Videos ASM | Avance 1 ===")

    # Captura de usuario
    nomina = pedir_hasta_valido("Captura tu nómina (alfanumérico, sin espacios): ", validar_nomina)
    nombre = pedir_hasta_valido("Captura tu nombre (solo letras y espacios): ", validar_nombre_persona)
    cant_videos = pedir_hasta_valido("Cantidad de videos a registrar (entero): ", lambda x: validar_entero_positivo(x, "Cantidad de videos"))

    # Confirmación
    confirmacion = pedir_hasta_valido("¿Deseas registrar los videos? (SI/NO): ", confirmar_si_no)

    videos = []
    if confirmacion == "SI":
        for idx in range(1, cant_videos + 1):
            print(f"\n--- Captura de Video {idx} de {cant_videos} ---")
            titulo = pedir_hasta_valido("Título (alfanumérico, permite espacios): ",
                                       lambda x: validar_texto_alfanumerico_con_espacios(x, "Título"))
            nombre_video = pedir_hasta_valido("Nombre del video (alfanumérico, permite espacios): ",
                                              lambda x: validar_texto_alfanumerico_con_espacios(x, "Nombre del video"))
            extension = pedir_hasta_valido("Extensión (alfanumérico, permite espacios): ",
                                           lambda x: validar_texto_alfanumerico_con_espacios(x, "Extensión"))
            tamano = pedir_hasta_valido("Tamaño (MB) (numérico, máximo 3MB): ", validar_tamano_mb)

            videos.append({
                "titulo": titulo,
                "nombre": nombre_video,
                "extension": extension,
                "tamano": tamano,
            })
    else:
        print("\nRegistro cancelado por el usuario (NO). No se capturarán videos.")

    # Guardar TODO en salida.txt (una sola línea)
    linea = construir_linea_salida(nomina, nombre, cant_videos, videos)
    guardar_salida_txt(linea, "salida.txt")

    print("\n✅ Datos guardados en salida.txt")
    print("Fin del programa.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Captura final por si ocurre algo no previsto (evidencia de uso de excepciones)
        print(f"Error inesperado: {e}")