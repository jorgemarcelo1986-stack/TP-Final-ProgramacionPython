"""Ejercicio 2 - Modelo de productos, excepciones y persistencia (EcoTech Solutions)."""
import json


class StockInvalidoError(Exception):
    """Se lanza cuando se intenta asignar un stock negativo."""


class DispositivoEcológico:
    """Clase base de los productos ecológicos del catálogo."""

    def __init__(self, codigo: str, nombre: str, stock: int):
        self.codigo = codigo
        self.nombre = nombre
        self.stock = stock  # pasa por el setter, así valida también al crear el objeto

    # Encapsulamiento: el stock real vive en un atributo privado
    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, valor: int):
        if valor < 0:
            raise StockInvalidoError(
                f"Stock inválido para {self.codigo}: {valor}. No puede ser negativo."
            )
        self.__stock = valor

    def ficha_tecnica(self) -> str:
        return f"[{self.codigo}] {self.nombre} | Stock disponible: {self.stock} u."

    def a_diccionario(self) -> dict:
        """Datos listos para serializar (el atributo privado se expone vía la property)."""
        return {
            "tipo": type(self).__name__,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "stock": self.stock,
        }


class PanelSolar(DispositivoEcológico):
    """Dispositivo especializado: suma potencia y eficiencia."""

    def __init__(self, codigo: str, nombre: str, stock: int, potencia_watts: float, eficiencia: float):
        super().__init__(codigo, nombre, stock)
        self.potencia_watts = potencia_watts
        self.eficiencia = eficiencia  # en porcentaje

    # Polimorfismo: misma llamada, ficha comercial propia del panel
    def ficha_tecnica(self) -> str:
        return (
            f"PANEL SOLAR {self.nombre} (cód. {self.codigo})\n"
            f"  Potencia: {self.potencia_watts} W | Eficiencia: {self.eficiencia}%\n"
            f"  Stock disponible: {self.stock} u."
        )

    def a_diccionario(self) -> dict:
        datos = super().a_diccionario()
        datos["potencia_watts"] = self.potencia_watts
        datos["eficiencia"] = self.eficiencia
        return datos


class GestorInventario:
    """Se encarga de la persistencia del catálogo."""

    @staticmethod
    def guardar_catalogo_json(lista_dispositivos, ruta_archivo):
        """Serializa los dispositivos y los guarda en `ruta_archivo`. Devuelve cuántos guardó."""
        catalogo = [dispositivo.a_diccionario() for dispositivo in lista_dispositivos]
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(catalogo, archivo, ensure_ascii=False, indent=4)
        return len(catalogo)


if __name__ == "__main__":
    catalogo = []

    # Productos válidos
    catalogo.append(DispositivoEcológico("DE-001", "Cargador solar portátil", 25))
    catalogo.append(PanelSolar("PS-100", "Monocristalino 450W", 12, 450, 21.5))
    catalogo.append(PanelSolar("PS-200", "Policristalino 320W", 30, 320, 17.8))

    # 1) Intento de crear un producto con stock negativo
    try:
        catalogo.append(PanelSolar("PS-300", "Panel defectuoso", -5, 400, 20.0))
    except StockInvalidoError as error:
        print(f"Error controlado al crear: {error}")

    # 2) Intento de asignar un stock erróneo a un producto existente
    try:
        catalogo[1].stock = -3
    except StockInvalidoError as error:
        print(f"Error controlado al asignar: {error}")
    print(f"El stock de {catalogo[1].codigo} sigue en {catalogo[1].stock}\n")

    # Polimorfismo: cada objeto emite su propia ficha técnica
    for dispositivo in catalogo:
        print(dispositivo.ficha_tecnica())
        print()

    # Persistencia: solo se exportan los productos válidos
    cantidad = GestorInventario.guardar_catalogo_json(catalogo, "catalogo_ecotech.json")
    print(f"Exportación exitosa: {cantidad} productos guardados en catalogo_ecotech.json")
