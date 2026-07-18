"""
Run this once to set up the database with all data.
Usage: python setup.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skinovate.settings')

import subprocess
subprocess.run(['python', 'manage.py', 'migrate'], check=True)

django.setup()

from django.contrib.auth.models import User
from stock.models import Product, StockIn, Sale
from datetime import date
from decimal import Decimal

print("\n✅ Step 1: Creating users...")
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@skinovate.com', 'admin123')
    print("   admin / admin123 created")
if not User.objects.filter(username='staff').exists():
    u = User.objects.create_user('staff', 'staff@skinovate.com', 'staff123')
    u.is_staff = True; u.save()
    print("   staff / staff123 created")
if not User.objects.filter(username='owner').exists():
    User.objects.create_superuser('owner', 'owner@skinovate.com', 'owner@123')
    print("   owner / owner@123 created")
else:
    u = User.objects.get(username='owner')
    u.set_password('owner@123')
    u.save()
    print("   owner / owner@123 updated")

print("\n✅ Step 2: Creating products...")
products_data = {
    "Skin Brightening Face Wash": 555,
    "Sunshield Sunscreen": 779,
    "Radiance Night Serum": 1499,
    "Tab Glutathione Glow Shots": 1499,
    "Rice Water Serum": 897,
    "Gentle Cleanser": 649,
    "Anti-acne Face Wash": 549,
    "Skinovate Mosturizer": 751,
    "Skin Brightening Night Cream": 595,
    "Hair Cocktail Tablets": 890,
    "Tab Immunity booster shots": 749,
    "Hair strengthening Shampoo": 888,
    "Hair Conditioner": 892,
    "Hair Oil": 555,
}
for name, mrp in products_data.items():
    p, created = Product.objects.get_or_create(name=name, defaults={
        'current_stock': 0,
        'mrp': Decimal(str(mrp)),
        'dp': Decimal(str(round(mrp * 0.7, 2))),
    })
    if not created and (p.mrp == 0):
        p.mrp = Decimal(str(mrp))
        p.dp = Decimal(str(round(mrp * 0.7, 2)))
        p.save()
print(f"   {Product.objects.count()} products ready (MRP set, DP defaulted to 70% of MRP - editable anytime)")

print("\n✅ Step 3: Loading Stock In entries...")
if StockIn.objects.count() == 0:
    stock_in_data = [
        ("Skin Brightening Face Wash", date(2026,1,13), 10, 555),
        ("Radiance Night Serum", date(2026,1,13), 10, 1499),
        ("Tab Glutathione Glow Shots", date(2026,1,13), 10, 1499),
        ("Rice Water Serum", date(2026,1,13), 10, 897),
        ("Gentle Cleanser", date(2026,1,13), 10, 649),
        ("Anti-acne Face Wash", date(2026,1,13), 10, 549),
        ("Skinovate Mosturizer", date(2026,1,13), 10, 751),
        ("Skin Brightening Night Cream", date(2026,1,13), 10, 595),
        ("Hair Cocktail Tablets", date(2026,1,13), 10, 890),
        ("Tab Immunity booster shots", date(2026,1,13), 10, 749),
        ("Hair strengthening Shampoo", date(2026,1,13), 10, 888),
        ("Hair Conditioner", date(2026,1,13), 10, 892),
        ("Hair Oil", date(2026,1,13), 10, 555),
        ("Sunshield Sunscreen", date(2026,1,19), 10, 779),
        ("Skin Brightening Face Wash", date(2026,2,3), 5, 555),
        ("Skin Brightening Night Cream", date(2026,2,10), 5, 595),
        ("Skin Brightening Face Wash", date(2026,2,10), 5, 555),
        ("Hair strengthening Shampoo", date(2026,2,10), 5, 888),
        ("Hair Cocktail Tablets", date(2026,2,10), 5, 890),
        ("Skin Brightening Face Wash", date(2026,2,17), 6, 555),
        ("Sunshield Sunscreen", date(2026,2,17), 15, 779),
        ("Radiance Night Serum", date(2026,2,17), 16, 1499),
        ("Tab Glutathione Glow Shots", date(2026,2,17), 10, 1499),
        ("Tab Immunity booster shots", date(2026,2,17), 10, 749),
        ("Hair strengthening Shampoo", date(2026,2,17), 9, 888),
        ("Hair Conditioner", date(2026,2,17), 13, 892),
        ("Hair Oil", date(2026,2,17), 9, 555),
        ("Rice Water Serum", date(2026,2,17), 20, 897),
        ("Gentle Cleanser", date(2026,2,17), 20, 649),
        ("Anti-acne Face Wash", date(2026,2,17), 18, 649),
        ("Skinovate Mosturizer", date(2026,2,17), 20, 892),
        ("Hair Cocktail Tablets", date(2026,2,17), 12, 890),
        ("Skin Brightening Night Cream", date(2026,2,17), 15, 595),
        ("Skin Brightening Face Wash", date(2026,3,4), 18, 595),
        ("Sunshield Sunscreen", date(2026,3,9), 10, 779),
        ("Skin Brightening Night Cream", date(2026,3,9), 10, 595),
        ("Tab Glutathione Glow Shots", date(2026,3,9), 10, 1891),
        ("Tab Immunity booster shots", date(2026,3,9), 10, 891),
    ]
    for pname, d, qty, price in stock_in_data:
        p = Product.objects.get(name=pname)
        StockIn.objects.create(product=p, date=d, quantity_in=qty, purchase_price=price, supplier="Dr. Susshil")
    print(f"   {StockIn.objects.count()} stock-in entries loaded")

print("\n✅ Step 4: Loading Sales...")
if Sale.objects.count() == 0:
    sales_data = [
        ("Skin Brightening Face Wash", date(2026,1,18), "Mr. Sandip Gujar", 1, "MRP", 555, 555, 555, 0, ""),
        ("Skin Brightening Night Cream", date(2026,1,18), "Mr. Sandip Gujar", 1, "MRP", 595, 595, 595, 0, ""),
        ("Sunshield Sunscreen", date(2026,1,18), "Mr. Sandip Gujar", 1, "MRP", 779, 779, 779, 0, ""),
        ("Skin Brightening Face Wash", date(2026,1,17), "Mr. Sanjay Mahadic", 5, "50%", 555, 277.5, 1387.5, 0, ""),
        ("Anti-acne Face Wash", date(2026,1,15), "Mr. Sanjay Mahadic", 1, "50%", 549, 274.5, 142, 132.5, "paid Rs.1520 on 16/02/2026"),
        ("Skin Brightening Face Wash", date(2026,1,20), "Mr. Sachin Patil (Barshi)", 2, "50%", 555, 277.5, 555, 0, ""),
        ("Anti-acne Face Wash", date(2026,1,20), "Mr. Sachin Patil (Barshi)", 2, "50%", 549, 274.5, 549, 0, ""),
        ("Skin Brightening Face Wash", date(2026,1,21), "Mr. Shyam (Pune)", 5, "50%", 555, 277.5, 1387.5, 0, ""),
        ("Anti-acne Face Wash", date(2026,1,21), "Mr. Shyam (Pune)", 5, "50%", 549, 274.5, 1372.5, 0, ""),
        ("Skin Brightening Face Wash", date(2026,1,22), "Mrs. Neha Patel", 1, "MRP", 555, 555, 555, 0, ""),
        ("Radiance Night Serum", date(2026,1,22), "Mrs. Neha Patel", 1, "MRP", 1499, 1499, 1499, 0, ""),
        ("Rice Water Serum", date(2026,1,25), "Mr. Anil Sharma", 2, "MRP", 897, 897, 1794, 0, ""),
        ("Gentle Cleanser", date(2026,1,25), "Mr. Anil Sharma", 1, "MRP", 649, 649, 649, 0, ""),
        ("Tab Glutathione Glow Shots", date(2026,1,27), "Dr. Mehta", 5, "50%", 1499, 749.5, 2000, 1747.5, "Partial payment"),
        ("Radiance Night Serum", date(2026,1,27), "Dr. Mehta", 3, "50%", 1499, 749.5, 1000, 1248.5, ""),
        ("Hair Oil", date(2026,1,28), "Ms. Priya Singh", 2, "MRP", 555, 555, 1110, 0, ""),
        ("Hair Conditioner", date(2026,1,28), "Ms. Priya Singh", 1, "MRP", 892, 892, 892, 0, ""),
        ("Skinovate Mosturizer", date(2026,1,30), "Mr. Ravi Kumar", 3, "50%", 751, 375.5, 1126.5, 0, ""),
        ("Skin Brightening Night Cream", date(2026,1,30), "Mr. Ravi Kumar", 4, "50%", 595, 297.5, 600, 590, "Balance due"),
        ("Rice Water Serum", date(2026,2,3), "Mrs. Kavya Reddy", 3, "MRP", 897, 897, 2691, 0, ""),
        ("Hair Cocktail Tablets", date(2026,2,5), "Dr. Patel", 2, "50%", 890, 445, 445, 445, "50% advance"),
        ("Anti-acne Face Wash", date(2026,2,7), "Mr. Suresh", 4, "50%", 549, 274.5, 1098, 0, ""),
        ("Sunshield Sunscreen", date(2026,2,10), "Mrs. Lata", 5, "MRP", 779, 779, 3895, 0, ""),
        ("Tab Immunity booster shots", date(2026,2,12), "Mr. Akash", 6, "50%", 749, 374.5, 2247, 0, ""),
        ("Skin Brightening Face Wash", date(2026,2,14), "Dr. Anjali", 3, "MRP", 555, 555, 1665, 0, ""),
        ("Radiance Night Serum", date(2026,2,14), "Dr. Anjali", 2, "MRP", 1499, 1499, 2998, 0, ""),
        ("Hair strengthening Shampoo", date(2026,2,18), "Mr. Vishal", 5, "50%", 888, 444, 2220, 0, ""),
        ("Gentle Cleanser", date(2026,2,20), "Mrs. Pooja", 2, "MRP", 649, 649, 1298, 0, ""),
        ("Tab Glutathione Glow Shots", date(2026,2,22), "Dr. Ramesh", 8, "50%", 1499, 749.5, 3000, 2996, "Payment pending"),
        ("Skin Brightening Night Cream", date(2026,2,25), "Ms. Swati", 5, "50%", 595, 297.5, 1487.5, 0, ""),
        ("Hair Oil", date(2026,2,28), "Mr. Ganesh", 3, "MRP", 555, 555, 1665, 0, ""),
        ("Rice Water Serum", date(2026,3,3), "Mrs. Sunita", 4, "MRP", 897, 897, 3588, 0, ""),
        ("Tab Immunity booster shots", date(2026,3,5), "Dr. Vikram", 10, "50%", 749, 374.5, 2000, 1745, "Remaining to collect"),
        ("Skinovate Mosturizer", date(2026,3,8), "Ms. Divya", 3, "MRP", 751, 751, 2253, 0, ""),
        ("Anti-acne Face Wash", date(2026,3,10), "Mr. Kiran", 4, "50%", 549, 274.5, 1098, 0, ""),
        ("Hair Conditioner", date(2026,3,12), "Mrs. Rekha", 5, "MRP", 892, 892, 4460, 0, ""),
        ("Skin Brightening Face Wash", date(2026,3,15), "Dr. Sharma", 6, "50%", 555, 277.5, 1665, 0, ""),
        ("Tab Glutathione Glow Shots", date(2026,3,18), "Mr. Rohit", 5, "50%", 1499, 749.5, 1500, 2247.5, "Pending"),
        ("Sunshield Sunscreen", date(2026,3,20), "Mrs. Meera", 8, "MRP", 779, 779, 6232, 0, ""),
        ("Radiance Night Serum", date(2026,3,22), "Dr. Priya", 4, "MRP", 1499, 1499, 5996, 0, ""),
        ("Hair Cocktail Tablets", date(2026,3,25), "Mr. Deepak", 5, "50%", 890, 445, 2225, 0, ""),
        ("Skin Brightening Night Cream", date(2026,3,28), "Mrs. Anita", 6, "50%", 595, 297.5, 900, 885, "Partial"),
        # Samples
        ("Skin Brightening Face Wash", date(2026,1,15), "Dr. Nandita", 1, "Sample", 555, 0, 0, 0, "Send By Anagha"),
        ("Radiance Night Serum", date(2026,1,15), "Dr. Nandita", 1, "Sample", 1499, 0, 0, 0, "Send By Anagha"),
        ("Skin Brightening Night Cream", date(2026,1,15), "Dr. Nandita", 1, "Sample", 595, 0, 0, 0, "Send By Anagha"),
        ("Tab Glutathione Glow Shots", date(2026,1,15), "Dr. Nandita", 1, "Sample", 1499, 0, 0, 0, "Send By Anagha"),
        ("Hair strengthening Shampoo", date(2026,1,15), "Dr. Nandita", 1, "Sample", 888, 0, 0, 0, "Send By Anagha"),
        ("Tab Glutathione Glow Shots", date(2026,1,17), "Dr. Sahu", 1, "Sample", 1499, 0, 0, 0, ""),
        ("Hair strengthening Shampoo", date(2026,1,17), "Dr. Sahu", 1, "Sample", 888, 0, 0, 0, ""),
        ("Skin Brightening Night Cream", date(2026,1,17), "Dr. Sahu", 1, "Sample", 595, 0, 0, 0, ""),
        ("Radiance Night Serum", date(2026,1,18), "Mr. Sandip Gujar", 1, "Sample", 1499, 0, 0, 0, "Given By Pravin Sir"),
        ("Skinovate Mosturizer", date(2026,1,18), "Mr. Sandip Gujar", 1, "Sample", 751, 0, 0, 0, ""),
        ("Skin Brightening Face Wash", date(2026,1,20), "Dr. Choudhary", 1, "Sample", 555, 0, 0, 0, ""),
        ("Radiance Night Serum", date(2026,1,20), "Dr. Choudhary", 1, "Sample", 1499, 0, 0, 0, ""),
        ("Sunshield Sunscreen", date(2026,1,20), "Dr. Choudhary", 1, "Sample", 779, 0, 0, 0, ""),
        ("Skin Brightening Face Wash", date(2026,1,20), "Dr. Navale", 1, "Sample", 555, 0, 0, 0, ""),
        ("Radiance Night Serum", date(2026,1,20), "Dr. Navale", 1, "Sample", 1499, 0, 0, 0, ""),
        ("Sunshield Sunscreen", date(2026,1,20), "Dr. Navale", 1, "Sample", 779, 0, 0, 0, ""),
    ]
    for pname, d, cust, qty, stype, mrp, sp, recv, pend, desc in sales_data:
        p = Product.objects.get(name=pname)
        Sale.objects.create(
            product=p, date=d, customer_name=cust, quantity_sold=qty,
            sale_type=stype, mrp=Decimal(str(mrp)), selling_price=Decimal(str(sp)),
            payment_received=Decimal(str(recv)), payment_pending=Decimal(str(pend)),
            description=desc
        )
    print(f"   {Sale.objects.count()} sales loaded")

print("\n✅ Step 5: Setting real stock levels from Excel...")
final_stock = {
    "Skin Brightening Face Wash": 0,   # was -7, setting to 0 for safety
    "Sunshield Sunscreen": 0,
    "Radiance Night Serum": 12,
    "Tab Glutathione Glow Shots": 0,   # was -5, setting to 0
    "Rice Water Serum": 18,
    "Gentle Cleanser": 26,
    "Anti-acne Face Wash": 15,
    "Skinovate Mosturizer": 23,
    "Skin Brightening Night Cream": 1,
    "Hair Cocktail Tablets": 9,
    "Tab Immunity booster shots": 3,
    "Hair strengthening Shampoo": 6,
    "Hair Conditioner": 12,
    "Hair Oil": 12,
}
for name, stock in final_stock.items():
    Product.objects.filter(name=name).update(current_stock=stock)
print("   Stock levels set!")

print("\n🎉 SETUP COMPLETE!")
print("=" * 40)
print("Run the server:  python manage.py runserver")
print("Open browser:    http://127.0.0.1:8000")
print("Login:           admin / admin123")
print("             OR  staff / staff123")
print("=" * 40)

print("\n✅ Step 6: Creating branches...")
from stock.models import Branch, UserProfile

branches_seed = [
    ("Nerul Branch 1", "Nerul", "Shop 1, Nerul Plaza, Nerul, Navi Mumbai"),
    ("Nerul Branch 2", "Nerul", "Shop 7, Sector 19, Nerul, Navi Mumbai"),
    ("Nerul Branch 3", "Nerul", "Shop 3, Palm Beach Road, Nerul"),
    ("Thane Branch 1", "Thane", "Shop 12, Viviana Mall, Thane West"),
    ("Thane Branch 2", "Thane", "Shop 5, Kapurbawdi, Thane"),
    ("Panvel Branch 1", "Panvel", "Shop 2, New Panvel East"),
    ("Panvel Branch 2", "Panvel", "Shop 8, Kamothe, Panvel"),
    ("Panvel Branch 3", "Panvel", "Shop 4, Kharghar, Panvel"),
    ("Panvel Branch 4", "Panvel", "Shop 11, Ulwe, Panvel"),
    ("Panvel Branch 5", "Panvel", "Shop 6, Kalamboli, Panvel"),
]
for name, location, address in branches_seed:
    Branch.objects.get_or_create(name=name, defaults={'location': location, 'address': address})
print(f"   {Branch.objects.count()} branches ready")

print("\n✅ Step 7: Creating owner user and assigning roles...")
if not User.objects.filter(username='owner').exists():
    owner_user = User.objects.create_superuser('owner', 'owner@skinovate.com', 'owner123')
    print("   owner / owner123 created")
else:
    owner_user = User.objects.get(username='owner')

for uname in ['owner', 'admin']:
    u = User.objects.filter(username=uname).first()
    if u:
        up, _ = UserProfile.objects.get_or_create(user=u, defaults={'role': 'owner', 'branch': None})
        up.role = 'owner'
        up.branch = None
        up.save()

staff_user = User.objects.filter(username='staff').first()
if staff_user:
    nerul1 = Branch.objects.get(name='Nerul Branch 1')
    up, _ = UserProfile.objects.get_or_create(user=staff_user, defaults={'role': 'staff', 'branch': nerul1})
    up.branch = nerul1
    up.role = 'staff'
    up.save()

from stock.models import Sale as S2, StockIn as SI2
nerul1 = Branch.objects.get(name='Nerul Branch 1')
S2.objects.filter(branch__isnull=True).update(branch=nerul1)
SI2.objects.filter(branch__isnull=True).update(branch=nerul1)
print("   Roles assigned. Existing data linked to Nerul Branch 1")

print("\n✅ Step 8: Creating individual branch user accounts...")
branch_users_seed = [
    (1,  'nerul1',  'nerul1@123',  'nerul1@skinovate.com',  'staff'),
    (2,  'nerul2',  'nerul2@123',  'nerul2@skinovate.com',  'staff'),
    (3,  'nerul3',  'nerul3@123',  'nerul3@skinovate.com',  'staff'),
    (4,  'thane1',  'thane1@123',  'thane1@skinovate.com',  'staff'),
    (5,  'thane2',  'thane2@123',  'thane2@skinovate.com',  'staff'),
    (6,  'panvel1', 'panvel1@123', 'panvel1@skinovate.com', 'staff'),
    (7,  'panvel2', 'panvel2@123', 'panvel2@skinovate.com', 'staff'),
    (8,  'panvel3', 'panvel3@123', 'panvel3@skinovate.com', 'staff'),
    (9,  'panvel4', 'panvel4@123', 'panvel4@skinovate.com', 'staff'),
    (10, 'panvel5', 'panvel5@123', 'panvel5@skinovate.com', 'staff'),
]
for branch_id, username, password, email, role in branch_users_seed:
    try:
        branch = Branch.objects.get(pk=branch_id)
    except Branch.DoesNotExist:
        branch = Branch.objects.filter(name__icontains=username[:6]).first()
        if not branch:
            continue
    if User.objects.filter(username=username).exists():
        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()
    else:
        u = User.objects.create_user(username=username, email=email, password=password)
    up, _ = UserProfile.objects.get_or_create(user=u, defaults={'role': role, 'branch': branch})
    up.branch = branch
    up.role = role
    up.save()
    print(f"   {username:10s} / {password:15s} -> {branch.name}")

print()
print("🎉 SETUP COMPLETE!")
print("=" * 60)
print("OWNER LOGIN (sees ALL branches):")
print("  owner  / owner@123")
print("  admin  / admin123")
print()
print("BRANCH LOGINS (each sees their branch only):")
print("  nerul1  / nerul1@123   -> Nerul Branch 1")
print("  nerul2  / nerul2@123   -> Nerul Branch 2")
print("  nerul3  / nerul3@123   -> Nerul Branch 3")
print("  thane1  / thane1@123   -> Thane Branch 1")
print("  thane2  / thane2@123   -> Thane Branch 2")
print("  panvel1 / panvel1@123  -> Panvel Branch 1")
print("  panvel2 / panvel2@123  -> Panvel Branch 2")
print("  panvel3 / panvel3@123  -> Panvel Branch 3")
print("  panvel4 / panvel4@123  -> Panvel Branch 4")
print("  panvel5 / panvel5@123  -> Panvel Branch 5")
print()
print("Run server: python manage.py runserver")
print("Open:       http://127.0.0.1:8000")
print("=" * 60)

print("\n✅ Step 9: Commission system ready...")
from stock.models import CommissionSetting
print("   CommissionSetting table created and ready.")
print("   → Login as owner → go to Commission → Set Rate for each branch")
print("   → At month end, click 'Generate All' to auto-calculate commissions")
