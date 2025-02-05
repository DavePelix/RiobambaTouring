from flask import Flask, render_template, request, url_for
from booking import Hotel
from datetime import datetime

app = Flask(__name__)

hoteles = [
    Hotel("Hotel Hacienda Abraspungo", "Km 3 1/2 Via a Guano", 8, 125, "abraspungo.png"),
    Hotel("Hotel El Altar", "Av. 11 de Noviembre", 10, 25, "altar.jpg"),
    Hotel("Hotel Zeus", "Av. Daniel León Borja", 25, 120, "zeus.jpg"),
    Hotel("Hotel El Cisne", "Av. Daniel León Borja", 8, 90, "cisne.jpg"),
    Hotel("Hotel El Molino", "Av. 11 de Noviembre", 8, 20, "molino.jpg"),
    Hotel("Hotel Navarra", "Av. Unidad Nacional", 8, 31, "navarra.jpg"),
    Hotel("Hotel Shalom", "Av. Daniel León Borja", 10, 64, "shalom.webp"),
    Hotel("Hotel Velanez", "Chile y Juan Lavalle", 12, 20, "velanez.jpg"),
    Hotel("Hotel Montecarlo","10 de Agosto y España", 12, 40, "montecarlo.jpg")
]

@app.route('/')
def index():
    return render_template('index.html', hoteles=hoteles)

@app.route('/hoteles')
def mostrarHoteles():
    return render_template('hoteles.html', hoteles=hoteles)

@app.route('/reservas')
def mostrarReservar():
    return render_template('reservas.html', hoteles=hoteles)

@app.route('/contacto')
def mostrarContactos():
    return render_template('contacto.html', hoteles=hoteles)

@app.route('/pago')
def mostrarPago():
    return render_template('pago.html', hoteles = hoteles)

@app.route('/reservar', methods=['POST'])
def reservar():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    hotel_nombre = request.form.get('hotel')
    habitaciones = int(request.form.get('habitaciones'))
    fecha_entrada = request.form.get('fecha_entrada')
    fecha_salida = request.form.get('fecha_salida')
    fecha_entrada_dt = datetime.strptime(fecha_entrada, "%Y-%m-%d")
    fecha_salida_dt = datetime.strptime(fecha_salida, "%Y-%m-%d")
    hotel = next((h for h in hoteles if h.nombre == hotel_nombre), None)
    noches = max(1, (fecha_salida_dt - fecha_entrada_dt).days)
    
    total = noches * habitaciones * hotel.getPrecio()
    
    if (habitaciones > hotel.getHabitaciones()) or (habitaciones < 1):
        return "ERROR: No hay suficientes habitaciones disponibles"
    else:
        mensaje = f"""
        Nombre: {nombre}
        Email: {email}
        Hotel: {hotel}
        Habitaciones: {habitaciones}
        Fecha de Entrada: {fecha_entrada}
        Fecha de Salida: {fecha_salida}
        Total a pagar: ${total:.2f}
        """        
        nuevas_habitaciones = hotel.getHabitaciones() - habitaciones
        hotel.setHabitaciones(nuevas_habitaciones)
        
        return render_template('confirmacion.html', mensaje = mensaje)
        
    
    

@app.route("/pagoconfirmado", methods=["POST"])
def confirmarPago():
    return render_template("pagoconfirmado.html")
    

if __name__ == '__main__':
    app.run(debug=True)
    
    