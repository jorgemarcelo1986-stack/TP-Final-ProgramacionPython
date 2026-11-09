"""Ejercicio 3 - Punto A: auditoría de calcular_emisiones_carbono con unittest.

Se ejecuta con:  python -m unittest -v
"""
import unittest

from emisiones import calcular_emisiones_carbono


class TestCalculoEmisiones(unittest.TestCase):

    # --- Exactitud numérica con valores nominales ---
    def test_consumo_nominal_con_factor_por_defecto(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(100), 40.0)

    def test_consumo_decimal(self):
        # 10.5 * 0.4 = 4.2; con floats se compara con assertAlmostEqual
        self.assertAlmostEqual(calcular_emisiones_carbono(10.5), 4.2)

    def test_factor_personalizado(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(200, factor_emision=0.5), 100.0)

    def test_consumo_cero_da_cero_emisiones(self):
        self.assertEqual(calcular_emisiones_carbono(0), 0)

    # --- Consumos fuera de rango ---
    def test_consumo_negativo_lanza_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-1)

    def test_consumo_negativo_mensaje_de_error(self):
        with self.assertRaises(ValueError) as contexto:
            calcular_emisiones_carbono(-50.5)
        self.assertIn("negativo", str(contexto.exception))

    def test_consumo_apenas_negativo_con_factor_personalizado(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-0.01, factor_emision=0.9)


if __name__ == "__main__":
    unittest.main()
