from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)


class products(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
#     

# @app.before_request
# def create_tables():
#     db.create_all()

@app.route('/product', methods=['POST'])
def create_product():
    data = request.json
    new_product = products(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"id": new_product.id}), 201

@app.route('/product', methods=['GET'])
def get_all_products():
    product = products.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price} for p in product])

@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = products.query.get_or_404(id)
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price})

@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    print("Received data:", data)
    product = products.query.get_or_404(id)
    print("Current product:", product.name, product.price)
    product.name = data['name']
    product.price = data['price']
    db.session.commit()
    print("Updated product:", product.name, product.price)
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price})

@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = products.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"Message":"Product Deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)




