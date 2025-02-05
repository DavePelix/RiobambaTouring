from flask import url_for
from datetime import datetime

class Hotel:
    def __init__(self, nombre, ubicacion, habitaciones_disponibles, precio_por_noche, imagen):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.habitaciones_disponibles = habitaciones_disponibles
        self.precio_por_noche = precio_por_noche
        self.imagen=imagen

    def __str__(self):
        return f"{self.nombre} - {self.ubicacion} - ${self.precio_por_noche}/noche - Habitaciones disponibles: {self.habitaciones_disponibles}"
    
    def getPrecio(self):
        return self.precio_por_noche
    
    def getImagen(self):
        return url_for('static', filename=f'{self.imagen}')
    
    def getHabitaciones(self):
        return self.habitaciones_disponibles    
    def setHabitaciones(self, nuevasHabitaciones_disponibles):
        self.habitaciones_disponibles = nuevasHabitaciones_disponibles

class Reserva:
    def __init__(self, cliente, email, hotel, habitaciones, fEntrada, fSalida):
        self.cliente = cliente
        self.hotel = hotel
        self.email = email
        self.habitaciones = habitaciones
        self.fEntrada=fEntrada
        self.fSalida=fSalida
        
        fecha_entrada_dt = datetime.strptime(fEntrada, "%Y-%m-%d")
        fecha_salida_dt = datetime.strptime(fSalida, "%Y-%m-%d")
        noches = max(1, (fecha_salida_dt - fecha_entrada_dt).days)
        
        if not hotel.reservar_habitacion(habitaciones):
            raise ValueError("No hay suficientes habitaciones disponibles en este hotel.")

        # Calcular el total de la reserva
        self.total = noches * habitaciones * hotel.getPrecio()

    def confirmar_reserva(self):
        if self.hotel.reservar_habitacion(self.cantidad_habitaciones):
            return f"Reserva confirmada para {self.cliente.nombre} en {self.hotel.nombre} por {self.cantidad_noches} noches. Total: ${self.total}"
        return "Lo sentimos, no hay suficientes habitaciones disponibles."

    def __str__(self):
        return f"Reserva de {self.cantidad_habitaciones} habitaciones en {self.hotel.nombre} por {self.cantidad_noches} noches. Total: ${self.total}"
