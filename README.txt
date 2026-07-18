================================================================
  SKINOVATE INVENTORY MANAGEMENT SYSTEM
  Built with Django (Python Web Framework)
================================================================

================================================================
  ALL LOGIN CREDENTIALS
================================================================

OWNER (sees ALL branches, manages everything):
  Username: owner     Password: owner@123
  Username: admin     Password: admin123

BRANCH / FRANCHISE STAFF (each sees their branch only):
  Branch              Username    Password
  ─────────────────── ─────────── ───────────────
  Nerul Branch 1      nerul1      nerul1@123
  Nerul Branch 2      nerul2      nerul2@123
  Nerul Branch 3      nerul3      nerul3@123
  Thane Branch 1      thane1      thane1@123
  Thane Branch 2      thane2      thane2@123
  Panvel Branch 1     panvel1     panvel1@123
  Panvel Branch 2     panvel2     panvel2@123
  Panvel Branch 3     panvel3     panvel3@123
  Panvel Branch 4     panvel4     panvel4@123
  Panvel Branch 5     panvel5     panvel5@123

Django Admin Panel: http://127.0.0.1:8000/admin
  (owner / admin login only)

================================================================
  WHAT EACH ROLE CAN DO
================================================================

OWNER (owner / admin):
  ✅ See all branches combined or one at a time
  ✅ Switch between branches on the dashboard
  ✅ Add / Edit / Delete branches
  ✅ Assign users to branches
  ✅ Set commission rate per branch (% or fixed ₹)
  ✅ Generate monthly commission for any branch
  ✅ Generate commission for ALL branches in one click
  ✅ Mark commission as Paid / Partial / Pending
  ✅ See paid vs pending commission per branch
  ✅ Full access to Sales, Stock In, Products, Alerts

BRANCH STAFF (nerul1, thane1, panvel1, etc.):
  ✅ See ONLY their own branch data (sales, stock)
  ✅ Add sales and stock entries for their branch
  ✅ See their own commission history (My Commission)
  ✅ See their commission rate, earned, paid, pending
  ❌ Cannot see other branches' data
  ❌ Cannot manage branches or set commission rates
  ❌ Cannot access /admin panel

================================================================
  WHAT THIS SYSTEM DOES
================================================================

DASHBOARD
  Summary: revenue, pending payments, purchases, stock alerts
  Owner: branch switcher to view one branch or all combined

STOCK IN
  Add/Edit/Delete purchase entries
  Stock increases automatically when added
  Each entry tagged to a branch

SALES
  Add/Edit/Delete sales with full discount control
  Stock decreases automatically when sale is saved
  Column filters: Date, Customer, Product, Qty, Discount On, Disc%
  Per-row Invoice + multi-select Combined Invoice
  Each sale tagged to a branch

STOCK ALERTS
  ⛔ OUT = 0 stock — order immediately
  ⚠️ LOW = 5 or fewer units — running low
  ✅ OK  = healthy stock level

PRODUCTS
  MRP is fixed (set once, cannot be changed after creation)
  DP (Distributor Price) is editable anytime
  Discount on MRP or DP chosen at time of each sale

BRANCHES (owner only)
  Add / Edit / Delete branches
  Assign users to branches with role (Staff / Manager)
  Each branch has its own sales and stock data

COMMISSION (owner only — branch staff can view their own)
  Owner sets rate per branch: % of sales OR fixed ₹/month
  Mark branch type: Company Branch or Franchise
  Generate commission for one branch or all at once
  Per branch: total commission, paid, pending
  Mark payments: Paid / Partial / Pending with date
  Branch staff see their own commission page (read-only)

================================================================
  HOW COMMISSION WORKS — STEP BY STEP
================================================================

STEP 1: Set the rate (one time per branch)
  → Login as owner
  → Go to 💰 Commission in the left menu
  → Click "⚙️ Rate" next to any branch
  → Choose:
      Branch Type: Company Branch or Franchise
      Commission Type: Percentage (%) or Fixed Amount (₹)
      Commission Value: e.g. 10 for 10%, or 5000 for ₹5000/month
  → Save

STEP 2: Generate commission at end of month
  → Go to 💰 Commission
  → Select Month and Year at the top
  → Click "⚡ Generate All" — calculates all branches at once
  → OR click "📋 Details" for one branch → Generate just that one

  How it calculates:
    If % type:  Commission = Total Sales of that month × Rate%
    If fixed:   Commission = Fixed ₹ amount (regardless of sales)

STEP 3: Record payment when you pay the branch
  → In Commission page, find the month's record
  → Click "💳 Pay"
  → Enter amount paid, date, and set status:
      Paid    = fully settled
      Partial = paid some, pending the rest
      Pending = not paid yet

STEP 4: Branch staff check their commission
  → Branch staff login (e.g. nerul1 / nerul1@123)
  → Click "💰 My Commission" in the left menu
  → They see: their rate, monthly earned, received, pending

================================================================
  MRP & DP DISCOUNT LOGIC
================================================================

Every product has:
  MRP = Fixed Maximum Retail Price (locked after creation)
  DP  = Distributor Price (editable anytime by owner)

When recording a sale, choose:
  "Discount on MRP" + 20.00% → Selling Price = MRP × 0.80
  "Discount on DP"  + 20.00% → Selling Price = DP  × 0.80
  "No Discount"              → Selling Price = full MRP

The sale form shows a LIVE calculator as you type.

================================================================
  STEP-BY-STEP SETUP (FOR BEGINNERS)
================================================================

STEP 1 — Install Python
  Download from https://www.python.org/downloads/
  ✅ CHECK "Add Python to PATH" during install
  Verify: open PowerShell → type: python --version

STEP 2 — Open the project folder in PowerShell
  cd C:\Users\YourName\Desktop\skinovate_django

STEP 3 — Install Django
  pip install django

STEP 4 — Setup database (ONE TIME ONLY)
  python setup.py
  You will see "🎉 SETUP COMPLETE!" when done

STEP 5 — Start the server
  python manage.py runserver
  Keep this window OPEN while using the website

STEP 6 — Open in browser (Chrome / Edge)
  DO NOT click the link in VS Code terminal
  Instead, open Chrome and type: http://127.0.0.1:8000

STEP 7 — Log in
  Use any credentials from the table at the top

To stop the server: press Ctrl + C in the terminal
To restart next time: just do Step 5 again

================================================================
  ADDING A NEW BRANCH / USER
================================================================

Add a new branch:
  → Login as owner → 🏢 Branches → + Add Branch

Add a new user for that branch:
  → Go to http://127.0.0.1:8000/admin
  → Users → Add User → set username and password
  → Back on website: Branches → Assign User to that branch

Change a user's password:
  → http://127.0.0.1:8000/admin → Users → click user → set password

================================================================
  COMMON ERRORS & FIXES
================================================================

"python not found"
  → Reinstall Python, check "Add to PATH"

"pip not found"
  → Try: python -m pip install django

"Port 8000 already in use"
  → Try: python manage.py runserver 8080
  → Open: http://127.0.0.1:8080

"No module named django"
  → Run: pip install django

Page opens in VS Code instead of browser
  → Copy http://127.0.0.1:8000 → paste in Chrome manually

================================================================
  PROJECT STRUCTURE
================================================================

skinovate_django/
├── manage.py          ← Run commands with this
├── setup.py           ← Run ONCE to load all data
├── db.sqlite3         ← The database file
├── README.txt         ← This file
├── skinovate/
│   ├── settings.py
│   └── urls.py
└── stock/
    ├── models.py      ← Database tables
    ├── views.py       ← Page logic + commission logic
    ├── forms.py       ← All forms
    ├── urls.py        ← URL routing
    └── templates/     ← All HTML pages

================================================================
