"""Ejercicio 1 - Sanitización y análisis estadístico de sensores (EcoTech Solutions)."""
import re

UBICACION_POR_DEFECTO = "Ubicación no registrada"


def _extraer_numero(valor) -> float:
    """Devuelve como float el número que contiene `valor` ('24.5C', '24,5 °C', 30, etc.)."""
    if isinstance(valor, (int, float)) and not isinstance(valor, bool):
        return float(valor)
    coincidencia = re.search(r"[-+]?\d+(?:[.,]\d+)?", str(valor))
    if coincidencia is None:
        raise ValueError(f"La temperatura {valor!r} no contiene ningún valor numérico")
    return float(coincidencia.group().replace(",", "."))


# Punto A: Normalización de lecturas
def limpiar_registro_sensor(registro_raw: dict) -> dict:
    """Normaliza un registro crudo de sensor y devuelve un diccionario NUEVO.

    - sensor_id: sin espacios sobrantes.
    - temperatura: float, sin sufijo de unidad.
    - ubicacion: si falta, es None o viene vacía, usa un valor por defecto.

    Lanza ValueError si falta el sensor_id o si la temperatura no tiene ningún número.
    """
    sensor_id = str(registro_raw.get("sensor_id") or "").strip()
    if not sensor_id:
        raise ValueError("El registro no tiene sensor_id")

    temperatura = _extraer_numero(registro_raw.get("temperatura"))

    ubicacion = str(registro_raw.get("ubicacion") or "").strip()
    if not ubicacion:
        ubicacion = UBICACION_POR_DEFECTO

    return {"sensor_id": sensor_id, "temperatura": temperatura, "ubicacion": ubicacion}


# Punto B: Monitoreo y mapeo estadístico
def generar_resumen_sensores(lista_sensores_limpios: list, umbral_temperatura: float) -> tuple:
    """Devuelve (lista_sensores_alerta, promedio_temperatura).

    lista_sensores_alerta: IDs de los sensores cuya temperatura SUPERA el umbral.
    promedio_temperatura: promedio de todos los sensores (0.0 si la lista está vacía).
    """
    if not lista_sensores_limpios:
        return [], 0.0

    lista_sensores_alerta = [
        sensor["sensor_id"]
        for sensor in lista_sensores_limpios
        if sensor["temperatura"] > umbral_temperatura
    ]
    total = sum(sensor["temperatura"] for sensor in lista_sensores_limpios)
    promedio_temperatura = total / len(lista_sensores_limpios)

    return lista_sensores_alerta, promedio_temperatura


if __name__ == "__main__":
    UMBRAL = 30.0

    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": "31,2 °C", "ubicacion": None},
        {"sensor_id": "  SENSOR-003", "temperatura": "38 C"},  # sin ubicación
        {"sensor_id": "SENSOR-004", "temperatura": "error", "ubicacion": "Planta Sur"},  # inválido
        {"sensor_id": "SENSOR-005 ", "temperatura": "27.8C", "ubicacion": "  Planta Sur "},
    ]

    # Limpieza: los registros inválidos se descartan sin cortar el programa
    registros_limpios = []
    for registro in registros_crudos:
        try:
            registros_limpios.append(limpiar_registro_sensor(registro))
        except ValueError as error:
            print(f"Registro descartado ({registro.get('sensor_id')!r}): {error}")

    alertas, promedio = generar_resumen_sensores(registros_limpios, UMBRAL)

    print()
    print("=" * 42)
    print("REPORTE DE SENSORES - ECOTECH SOLUTIONS")
    print("=" * 42)
    print(f"Registros válidos: {len(registros_limpios)} de {len(registros_crudos)}")
    print(f"Umbral de temperatura: {UMBRAL:.1f} °C")
    print(f"Temperatura promedio: {promedio:.2f} °C")
    print("Sensores en alerta: " + (", ".join(alertas) if alertas else "ninguno"))
    print()
    print("Detalle:")
    for sensor in registros_limpios:
        print(f"  {sensor['sensor_id']:<12} {sensor['temperatura']:>5.1f} °C  {sensor['ubicacion']}")
