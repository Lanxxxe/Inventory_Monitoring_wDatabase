from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('inventory.db')
conn.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
''')
conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/add', methods=['POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO products (name, quantity) VALUES (?, ?)', (name, quantity))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']

        cursor.execute('UPDATE products SET name=?, quantity=? WHERE id=?', (name, quantity, product_id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM products WHERE id=?', (product_id,))
    product = cursor.fetchone()
    conn.close()

    return render_template('edit.html', product=product)

@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id=?', (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
