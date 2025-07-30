-- Customer Table (SD)
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    address TEXT
);

-- Vendors Table(MM)
CREATE TABLE vendors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    contact TEXT
);

-- Materials Table (MM + PP)
CREATE Table materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT, --raw or finished
    unit price REAL,
    stock INTEGER
);

-- Sales Order Table (SD)
CREATE Table sales_orders (
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
CREATE TABLE production_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id INTEGER NOT NULL,
    quantity INTEGER,
    start_date TEXT,
    end_date TEXT,
    status TEXT,
    FOREIGN KEY (material_id) REFERENCES materials(id)
);

-- Cost Centers Table (FI/CO)
CREATE TABLE cost_centers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    name TEXT
);

-- Expenses Table (FI/CO)
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cost_center_id INTEGER NOT NULL,
    amount REAL,
    description TEXT,
    expense_date TEXT,
    FOREIGN KEY (cost_center_id) REFERENCES cost_centers(id)
);

-- Departments Table (HCM)
CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Employees Table (HCM)
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department_id INTEGER,
    job_title TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);