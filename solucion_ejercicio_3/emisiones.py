"""Ejercicio 3 - Lógica de emisiones de EcoTech Solutions (no depende de Django)."""


def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    """Emisiones de carbono (kg CO2) = consumo en kWh * factor de emisión.

    Lanza ValueError si el consumo es negativo.
    """
    if consumo_kwh < 0:
        raise ValueError("El consumo no puede ser negativo")
    return consumo_kwh * factor_emision


def obtener_metricas_consumo(registros):
    """Procesa el historial de consumos por planta.

    `registros` es una lista de diccionarios {"planta": str, "consumo_kwh": float};
    una misma planta puede aparecer varias veces (historial).

    Devuelve un diccionario con:
      - emisiones_totales: emisiones globales de todos los registros (kg CO2)
      - planta_mayor_consumo: planta con más kWh acumulados (None si no hay registros)
      - consumo_por_planta: kWh acumulados de cada planta
    """
    consumo_por_planta = {}
    emisiones_totales = 0.0

    for registro in registros:
        planta = registro["planta"]
        consumo = registro["consumo_kwh"]

        emisiones_totales += calcular_emisiones_carbono(consumo)
        consumo_por_planta[planta] = consumo_por_planta.get(planta, 0) + consumo

    if consumo_por_planta:
        planta_mayor_consumo = max(consumo_por_planta, key=consumo_por_planta.get)
    else:
        planta_mayor_consumo = None

    return {
        "emisiones_totales": round(emisiones_totales, 2),
        "planta_mayor_consumo": planta_mayor_consumo,
        "consumo_por_planta": consumo_por_planta,
    }
