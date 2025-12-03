from flask import render_template, request
from . import db
from .models import Customer, Order, Contact
from .forms import SearchForm, DateRangeForm, ContactFilterForm
from datetime import datetime, timedelta
from sqlalchemy import func
from flask import current_app as app

@app.route('/')
def index():
    q = request.args.get('q', '')
    order_q = request.args.get('order_q', '')
    contact_q = request.args.get('contact_q', '')
    # Customers search
    if q:
        customers = Customer.query.filter(func.lower(Customer.first_name + ' ' + Customer.last_name).like(f"%{q.lower()}%"))            .order_by(Customer.last_name).all()
    else:
        customers = Customer.query.order_by(Customer.last_name).limit(20).all()

    # Orders global, desc by date
    orders_query = Order.query
    if order_q:
        orders_query = orders_query.filter(Order.description.ilike(f"%{order_q}%"))
    orders = orders_query.order_by(Order.created_at.desc()).limit(10).all()

    # Contacts global, desc by date
    contacts_query = Contact.query
    if contact_q:
        contacts_query = contacts_query.filter(Contact.note.ilike(f"%{contact_q}%"))
    contacts = contacts_query.order_by(Contact.created_at.desc()).limit(10).all()

    return render_template('index.html', customers=customers, orders=orders, contacts=contacts, q=q, order_q=order_q, contact_q=contact_q)

@app.route('/customer/<int:id>/')
def customer_detail(id):
    customer = Customer.query.get_or_404(id)
    # totals
    total_revenue = db.session.query(func.coalesce(func.sum(Order.amount),0)).filter(Order.customer_id==customer.id).scalar()
    one_year_ago = datetime.utcnow() - timedelta(days=365)
    revenue_last_year = db.session.query(func.coalesce(func.sum(Order.amount),0)).filter(Order.customer_id==customer.id, Order.created_at >= one_year_ago).scalar()

    # date range filter
    start = request.args.get('start')
    end = request.args.get('end')
    orders_q = Order.query.filter_by(customer_id=customer.id)
    contacts_q = Contact.query.filter_by(customer_id=customer.id)

    if start:
        try:
            s = datetime.fromisoformat(start)
            orders_q = orders_q.filter(Order.created_at >= s)
            contacts_q = contacts_q.filter(Contact.created_at >= s)
        except:
            pass
    if end:
        try:
            e = datetime.fromisoformat(end)
            orders_q = orders_q.filter(Order.created_at <= e)
            contacts_q = contacts_q.filter(Contact.created_at <= e)
        except:
            pass

    orders = orders_q.order_by(Order.created_at.desc()).limit(20).all()
    contacts = contacts_q.order_by(Contact.created_at.desc()).limit(20).all()

    return render_template('customer_detail.html', customer=customer, total_revenue=total_revenue, revenue_last_year=revenue_last_year, orders=orders, contacts=contacts, start=start, end=end)
