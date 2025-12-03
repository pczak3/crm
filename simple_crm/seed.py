import random
from datetime import datetime, timedelta
from app import create_app, db
from app.models import Customer, Order, Contact
import os

app = create_app()
app.app_context().push()

# If DB exists, remove to reseed cleanly (optional)
db_path = os.path.join(os.path.dirname(__file__), 'crm.db')
if os.path.exists(db_path):
    os.remove(db_path)

db.create_all()

first_names = ['Anna','Benjamin','Claudia','Daniel','Eva','Felix','Gabriele','Hans','Ines','Jürgen','Katrin','Lukas','Maria','Nina']
last_names = ['Müller','Schmidt','Schneider','Fischer','Weber','Meyer','Wagner','Becker','Hoffmann','Schäfer','Klein']

emails = ['gmail.com','hotmail.com','example.com','yahoo.de']

contact_kinds = ['Email','Telefon','persönlich']

# create >=10 customers
customers = []
for i in range(12):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    email = f"{fn.lower()}.{ln.lower()}{i}@{random.choice(emails)}"
    phone = f"+49 170 {random.randint(1000000,9999999)}"
    c = Customer(first_name=fn, last_name=ln, email=email, phone=phone, created_at=datetime.utcnow() - timedelta(days=random.randint(0,700)))
    db.session.add(c)
    customers.append(c)
db.session.commit()

# create >=50 orders in last 2 years
for i in range(60):
    cust = random.choice(customers)
    amount = round(random.uniform(50, 500),2)
    days_ago = random.randint(0, 730)
    created = datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0,23))
    descr = random.choice(['Website Redesign','Jährliche Wartung','Beratung','Lizenzkauf','Hardware Bestellung','Sonderanfertigung'])
    o = Order(customer_id=cust.id, amount=amount, created_at=created, description=descr)
    db.session.add(o)

# create >=50 contacts in last 2 years
notes = ['Kundengespräch', 'Follow-up', 'Preisangebot geschickt', 'Termin vereinbart', 'Anrufbeantworter', 'Persönliches Meeting']
for i in range(70):
    cust = random.choice(customers)
    kind = random.choice(contact_kinds)
    days_ago = random.randint(0, 730)
    created = datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0,23))
    note = random.choice(notes)
    ct = Contact(customer_id=cust.id, kind=kind, note=note, created_at=created)
    db.session.add(ct)

db.session.commit()

print('Seeding finished. Created %d customers, %d orders, %d contacts.' % (len(customers), Order.query.count(), Contact.query.count()))
