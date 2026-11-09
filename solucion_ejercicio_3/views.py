"""Ejercicio 3 - Punto B: vista Django del panel de sustentabilidad.

Este archivo está pensado para vivir dentro de una app de Django (un paquete),
junto a emisiones.py. Por eso el import es relativo.
"""
from django.shortcuts import render

from .emisiones import obtener_metricas_consumo

# Historial de consumos por planta. En un sistema real saldría de la base de datos.
REGISTROS_CONSUMO = [
    {"planta": "Planta Norte", "consumo_kwh": 1200.5},
    {"planta": "Planta Sur", "consumo_kwh": 950.0},
    {"planta": "Planta Norte", "consumo_kwh": 1100.0},
    {"planta": "Planta Este", "consumo_kwh": 780.25},
    {"planta": "Planta Sur", "consumo_kwh": 1020.0},
]


def vista_panel_sustentabilidad(request):
    metricas = obtener_metricas_consumo(REGISTROS_CONSUMO)

    contexto = {
        "titulo": "Panel de sustentabilidad",
        "emisiones_totales": metricas["emisiones_totales"],
        "planta_mayor_consumo": metricas["planta_mayor_consumo"],
        "consumo_por_planta": metricas["consumo_por_planta"],
    }
    return render(request, "sustentabilidad/panel.html", contexto)
