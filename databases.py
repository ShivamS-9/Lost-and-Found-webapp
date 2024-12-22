import sqlite3
import base64
from flask import Flask, request, render_template, redirect, url_for

app=Flask(__name__)

conn=sqlite3.connect('databases.db')
c=conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS lost_items
    (id INTEGER PRIMARY KEY AUTOINCREMENT, item_img BLOB, item_description TEXT, found_by TEXT, found_by_email TEXT, found_at TEXT, lost_by TEXT, lost_by_email TEXT, lost_at TEXT);
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS borrowed_items
    (id INTEGER PRIMARY KEY AUTOINCREMENT, item_name TEXT, item_image BLOB, item_description TEXT, item_price TEXT, seller_name TEXT, seller_email TEXT, borrower_name TEXT, borrower_email TEXT);
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS buy_items
    (id INTEGER PRIMARY KEY AUTOINCREMENT, item_name TEXT, item_image BLOB, item_description TEXT, item_price TEXT, seller_name TEXT, seller_email TEXT);
''')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/sell_items')
def sell():
    return render_template('sell.html')

@app.route('/lost_items_list')
def lost():
    conn=sqlite3.connect('databases.db')
    c=conn.cursor()
    
    c.execute('SELECT * FROM lost_items')
    data=c.fetchall()
    
    rows=[]
    
    for id, item_img, item_description, found_by, found_by_email, found_at, lost_by, lost_by_email, lost_at in data:
        encoded_image = base64.b64encode(item_img).decode('utf-8')
        rows.append((id, encoded_image, item_description, found_by, found_by_email, found_at, lost_by, lost_by_email, lost_at))
    
    return render_template('lost.html', data=rows)

@app.route('/lost_item_form')
def post():
    return render_template('post.html')

@app.route('/upload_lost_item', methods=['POST'])
def upload_lost_item():
    lost_found=request.form.get('lost-found')
    item_img=request.files['image'].read()
    item_description=request.form['description']
    poster_name=request.form['poster_name']
    poster_email=request.form['poster_email']
    location=request.form['location']
    
    conn=sqlite3.connect('databases.db')
    c=conn.cursor()
    
    if(lost_found=='found'):
        c.execute('''INSERT INTO lost_items (item_img, item_description, found_by, found_by_email, found_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (item_img, item_description, poster_name, poster_email, location))
    elif(lost_found=='lost'):
        c.execute('''INSERT INTO lost_items (item_img, item_description, lost_by, lost_by_email, lost_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (item_img, item_description, poster_name, poster_email, location))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('lost'))

@app.route('/buy_items_list')
def buy():
    conn=sqlite3.connect('databases.db')
    c=conn.cursor()
    c.execute('SELECT * FROM buy_items')
    data=c.fetchall()
    rows=[]
    for id, name, image, description, price, seller_name, seller_email in data:
        encoded_image = base64.b64encode(image).decode('utf-8')
        rows.append((id, name, encoded_image, description, price, seller_name, seller_email, id))
    return render_template('buy.html', data=rows)

@app.route('/sell_item', methods=['POST'])
def sell_item():
    item_name=request.form['name']
    item_img=request.files['image'].read()
    item_description=request.form['description']
    item_price=request.form['price']
    seller_name=request.form['seller_name']
    seller_email=request.form['seller_email']
    
    conn=sqlite3.connect('databases.db')
    c=conn.cursor()
    
    c.execute('''
        INSERT INTO buy_items (item_name, item_image, item_description, item_price, seller_name, seller_email)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (item_name, item_img, item_description, item_price, seller_name, seller_email))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('buy'))

@app.route('/buy_item_form', methods=['POST'])
def buydetails():
    item_id=request.form['item_id']
    return render_template('buydetails.html', data=item_id)

@app.route('/buy_item', methods=['POST'])
def buy_item():
    item_id=request.form['item_id']
    
    conn=sqlite3.connect('databases.db')
    c=conn.cursor()
    
    c.execute('DELETE FROM buy_items WHERE id = ?', (item_id,))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('buy'))

@app.route('/borrowed_items_list')
def borrowed():
    conn=sqlite3.connect('databases.db')
    c=conn.cursor()
    
    c.execute('SELECT * FROM borrowed_items')
    data=c.fetchall()
    
    return render_template('borrowed.html', data=data)

@app.route('/borrow_item_form', methods=['POST'])
def borrowdetails():
    item_id=request.form['item_id']
    item_name=request.form['item_name']
    item_img=request.form['item_img']
    description=request.form['description']
    price=request.form['price']
    seller_name=request.form['seller_name']
    seller_email=request.form['seller_email']
    data=()
    data=(item_id, item_name, item_img, description, price, seller_name, seller_email)
    return render_template('borrowdetails.html', data=data)

@app.route('/borrow_item', methods=['POST'])
def borrow_item():
    item_id=int(request.form['item_id'])
    item_name=request.form['item_name']
    item_img=request.form['item_img']
    item_description=request.form['description']
    item_price=request.form['price']
    seller_name=request.form['seller_name']
    seller_email=request.form['seller_email']
    borrower_name=request.form['borrower_name']
    borrower_email=request.form['borrower_email']
    
    conn=sqlite3.connect('databases.db')
    c=conn.cursor()
    
    c.execute('''
        INSERT INTO borrowed_items (item_name, item_image, item_description, item_price, seller_name, seller_email, borrower_name, borrower_email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (item_name, item_img, item_description, item_price, seller_name, seller_email, borrower_name, borrower_email))
    
    c.execute('''
        DELETE FROM buy_items WHERE id = ?
    ''', (item_id,))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('buy'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)