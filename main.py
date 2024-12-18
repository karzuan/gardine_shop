from flask import Flask, render_template, request, redirect, url_for, Response
import psycopg2
import psycopg2.extras
import csv

conn = psycopg2.connect(
        host="localhost",
        database="gardine_db",
        user="postgres",
        password="07072021"
)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur.execute("Select * from products")
items = cur.fetchall()
cur.execute("Select * from brands")
brands = cur.fetchall()
cur.execute("Select * from status")
status = cur.fetchall()
cur.execute("Select * from categories")
categories = cur.fetchall()

def get_to_csv(data):
    with open ('products.csv', 'w', newline='',  encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "description", "status", "price", "discount"])
        for row in data:
            writer.writerow(row)


app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/tables')
def tables():
    conn = psycopg2.connect(
        host="localhost",
        database="gardine_db",
        user="postgres",
        password="07072021"
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
                WITH cte_products AS (
                    SELECT id as "prod_id", name as "prod_name", description as "prod_desc", brand as "brand_id", status_id, price, category_id
                    FROM products ),
                cte_brands AS (
                    select id as "brand_id", name as "brand_name", "desc" as "brand_desc"
                    FROM brands ),
                cte_status AS (
                    select id as "status_id", name as "status_name"
                    FROM status ),
                cte_categories AS (
                    select id as "category_id", name as "category_name"
                    FROM categories )
                select prod_id, prod_name, prod_desc, price, brand_name, status_name, category_name
                from cte_products p
                join cte_brands b on p.brand_id = b.brand_id
                join cte_status s on p.status_id = s.status_id
                join cte_categories c on p.category_id = c.category_id
                Order By prod_id;
            """)
    items = cur.fetchall()
    cur.execute("Select * from brands")
    brands = cur.fetchall()
    cur.execute("Select * from status")
    status = cur.fetchall()
    cur.execute("Select * from categories")
    categories = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('tables.html', items=items, brands=brands, status=status, categories=categories)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/settings')
def contacts():
    return render_template('settings.html')

@app.route('/products')
def products():
    conn = psycopg2.connect(
        host="localhost",
        database="gardine_db",
        user="postgres",
        password="07072021"
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
                    WITH cte_products AS (
                        SELECT id as "prod_id", name as "prod_name", description as "prod_desc", brand as "brand_id", status_id, price, category_id
                        FROM products ),
                    cte_brands AS (
                        select id as "brand_id", name as "brand_name", "desc" as "brand_desc"
                        FROM brands ),
                    cte_status AS (
                        select id as "status_id", name as "status_name"
                        FROM status ),
                    cte_categories AS (
                        select id as "category_id", name as "category_name"
                        FROM categories )
                    select prod_id, prod_name, prod_desc, price, brand_name, status_name, category_name 
                    from cte_products p
                    join cte_brands b on p.brand_id = b.brand_id
                    join cte_status s on p.status_id = s.status_id
                    join cte_categories c on p.category_id = c.category_id;
                """)
    items = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('products.html', items=items)

@app.route('/product/<int:id>')
def product(id):
    conn = psycopg2.connect(
        host="localhost",
        database="gardine_db",
        user="postgres",
        password="07072021"
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM products WHERE id=%s", (id,))
    item = cur.fetchone()
    cur.execute("Select * from brands")
    brands = cur.fetchall()
    cur.execute("Select * from status")
    status = cur.fetchall()
    cur.execute("Select * from categories")
    categories = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('product.html', item=item, brands=brands, status=status, categories=categories)


@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    discount = request.form['discount']
    brand = request.form['brand_id']
    status = request.form['status_id']
    category = request.form['category_id']
    conn = psycopg2.connect(
        host="localhost",
        database="gardine_db",
        user="postgres",
        password="07072021"
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("INSERT INTO products (name, description, price, discount, brand, status_id, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, description, price, discount, brand, status, category))
    conn.commit()
    cur.close()
    conn.close()
    ## toDo: make redirect to just created single product page
    return redirect(url_for('products'))

@app.route('/add')
def add():
    return render_template('add.html', brands=brands, status=status, categories=categories)

@app.route('/update_product', methods=['POST'])
def edit_product():
    id = request.form['id']
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    discount = request.form['discount']
    brand = request.form['brand_id']
    status = request.form['status_id']
    category = request.form['category_id']
    conn = psycopg2.connect(
        host="localhost",
        database="gardine_db",
        user="postgres",
        password="07072021"
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("UPDATE products SET name=%s, description=%s, price=%s, discount=%s, brand=%s, status_id=%s, category_id=%s WHERE id=%s", (name, description, price, discount, brand, status, category, id))
    conn.commit()
    cur.close()
    conn.close()
    ##return redirect(url_for('tables'))
    return redirect(url_for('product', id=id))

@app.route('/edit/<int:id>')
def edit(id):
    conn = psycopg2.connect(
        host="localhost",
        database="gardine_db",
        user="postgres",
        password="07072021"
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM products WHERE id=%s", (id,))
    item = cur.fetchone()
    cur.execute("Select * from brands")
    brands = cur.fetchall()
    cur.execute("Select * from status")
    status = cur.fetchall()
    cur.execute("Select * from categories")
    categories = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('edit.html', item=item, brands=brands, status=status, categories=categories)

@app.route('/export-csv')
def export_csv():
    conn = psycopg2.connect(
        host="localhost",
        database="gardine_db",
        user="postgres",
        password="07072021"
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("Select id, name, description, status_id, price, discount from products")
    products_export = cur.fetchall()
    get_to_csv(products_export)
    return Response(open('products.csv', 'r'), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=products.csv'})



if __name__ == "__main__":
    app.run(debug=True)