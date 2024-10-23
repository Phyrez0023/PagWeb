from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta' 

# Ruta principal que muestra la lista de productos
@app.route('/')
def index():
    productos = session.get('productos', [])
    return render_template('index.html', productos=productos)

# Ruta para agregar un nuevo producto
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        id_producto = request.form['id']
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        fecha_vencimiento = request.form['fecha_vencimiento']
        categoria = request.form['categoria']

        # Verificar si el ID es único
        productos = session.get('productos', [])
        if any(prod['id'] == id_producto for prod in productos):
            flash('El ID del producto debe ser único.')
            return redirect(url_for('add_product'))

        # Crear un nuevo producto
        nuevo_producto = {
            'id': id_producto,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }
        
        # Agregar el producto a la sesión
        productos.append(nuevo_producto)
        session['productos'] = productos
        flash('Producto agregado exitosamente.')
        return redirect(url_for('index'))

    return render_template('add_product.html')

# Ruta para editar un producto
@app.route('/edit_product/<id_producto>', methods=['GET', 'POST'])
def edit_product(id_producto):
    productos = session.get('productos', [])
    producto = next((prod for prod in productos if prod['id'] == id_producto), None)

    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        flash('Producto editado exitosamente.')
        return redirect(url_for('index'))

    return render_template('edit_product.html', producto=producto)

# Ruta para eliminar un producto
@app.route('/delete_product/<id_producto>')
def delete_product(id_producto):
    productos = session.get('productos', [])
    productos = [prod for prod in productos if prod['id'] != id_producto]
    session['productos'] = productos
    flash('Producto eliminado exitosamente.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
