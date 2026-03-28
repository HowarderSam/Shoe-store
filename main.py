from database import add_order , add_user,get_products,get_product, get_users, get_user, get_orders
from flask import Flask, render_template,request,redirect , url_for


app = Flask(__name__)

# Головна сторінка
@app.route('/')
def index():
    products = get_products()
    return render_template('index.html',
                           products = products)

@app.route('/<int:id>/',methods =['GET','POST'])
def buy_product(id):
    product = get_product(id)
    if request.method =='POST':
        name = request.form.get('name')
        phone = request.form['phone']
        address = request.form.get('address')
        if not get_user(phone):
            add_user(name,phone,address)
        user = get_user(phone)
        add_order(id, user.id)
        return render_template('thanks.html')
    return render_template('buy.html',
                           i = product)

@app.route('/us/')
def us():
    users = get_users()
    return render_template('us.html',
                           users = users)


@app.route('/cabinet/',methods=['GET','POST'])
def cabinet():
    if request.method == 'POST':
        phone = request.form['phone']
        if not get_user(phone):
            return 'Error'
        user = get_user(phone)
        orders = get_orders(user.id)
        return render_template('cabinet.html',orders=orders)
    return render_template('cabinet.html', orders = ())



if __name__ == '__main__':
    app.run(debug=True, port=5000)