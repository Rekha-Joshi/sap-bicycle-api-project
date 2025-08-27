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
CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    type TEXT,
    unit_price REAL,
    stock INTEGER,
    reorder_level INTEGER DEFAULT 30,
    vendor_id INTEGER,
    FOREIGN KEY (vendor_id) REFERENCES vendors(id)
);

-- Sales Order Table (SD)
CREATE Table IF NOT EXISTS sales_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    quantity INTEGER,
    order_date TEXT,
    status TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE RESTRICT,
    FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE RESTRICT
);

-- Production Orders Table (PP)
CREATE TABLE IF NOT EXISTS production_orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sales_order_id INTEGER NOT NULL,
  material_id INTEGER NOT NULL,
  planned_quantity INTEGER NOT NULL,
  start_date TEXT,   -- set when you create the PO (or now)
  end_date   TEXT,   -- set when you complete the PO
  status     TEXT,   -- "Planned" | "In-Progress" | "Completed"
  FOREIGN KEY (sales_order_id) REFERENCES sales_orders(id) ON DELETE RESTRICT,
  FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE RESTRICT
);

-- Cost Centers Table (FI/CO)
CREATE TABLE IF NOT EXISTS cost_centers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT
);

-- Expenses Table (FI/CO)
CREATE TABLE IF NOT EXISTS expenses (
  id                   INTEGER PRIMARY KEY AUTOINCREMENT,
  cost_center_id       INTEGER NOT NULL,
  sales_order_id       INTEGER,
  production_order_id  INTEGER,
  category             TEXT NOT NULL CHECK (category IN ('Manufacturing','PostProduction')),
  amount               REAL NOT NULL CHECK (amount >= 0),
  description          TEXT,
  expense_date         TEXT NOT NULL DEFAULT (DATE('now')),
  FOREIGN KEY (cost_center_id) REFERENCES cost_centers(id) ON DELETE RESTRICT,
  FOREIGN KEY (sales_order_id) REFERENCES sales_orders(id) ON DELETE RESTRICT,
  FOREIGN KEY (production_order_id) REFERENCES production_orders(id) ON DELETE RESTRICT,
  CHECK (
    (category = 'Manufacturing'  AND production_order_id IS NOT NULL AND sales_order_id IS NULL) OR
    (category = 'PostProduction' AND sales_order_id      IS NOT NULL AND production_order_id IS NULL)
  )
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