-- Customer Table (SD)
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    address TEXT
);

-- Vendors Table(MM)
CREATE TABLE IF NOT EXISTS vendors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    contact TEXT
);

-- Materials Table (MM + PP)
CREATE Table IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    type TEXT, --raw or finished
    unit_price REAL,
    stock INTEGER
);

-- Sales Order Table (SD)
CREATE Table IF NOT EXISTS sales_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    quantity INTEGER,
    order_date TEXT,
    status TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (material_id) REFERENCES materials(id)
);

-- Production Orders Table (PP)
CREATE TABLE IF NOT EXISTS production_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id INTEGER NOT NULL,
    quantity INTEGER,
    start_date TEXT,
    end_date TEXT,
    status TEXT,
    FOREIGN KEY (material_id) REFERENCES materials(id)
);

-- Cost Centers Table (FI/CO)
CREATE TABLE IF NOT EXISTS cost_centers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT
);

-- Expenses Table (FI/CO)
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cost_center_id INTEGER NOT NULL,
    amount REAL,
    description TEXT,
    expense_date TEXT,
    FOREIGN KEY (cost_center_id) REFERENCES cost_centers(id)
);

-- Departments Table (HCM)
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Employees Table (HCM)
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department_name TEXT,
    job_title TEXT,
    FOREIGN KEY (department_name) REFERENCES departments(name)
);