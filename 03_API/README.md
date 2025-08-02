# API Route Summary – Bicycle Manufacturing ERP Project

This file lists all API routes planned and implemented for this bicycle manufacturing system.

Each route supports one or more business use cases and connects to a corresponding database table.

---

## Customers

| Method | Route        | Description                   |
|--------|--------------|-------------------------------|
| GET    | /customers   | Fetch all customer records    |
| POST   | /customers   | Add a new customer            |

---

## Vendors

| Method | Route       | Description          |
|--------|-------------|----------------------|
| GET    | /vendors    | List all vendors     |
| POST   | /vendors    | Add a new vendor     |

---

## Materials (Raw and Finished)

| Method | Route                  | Description                          |
|--------|------------------------|--------------------------------------|
| GET    | /materials             | View all materials                   |
| POST   | /materials             | Add a new material                   |
| PUT    | /materials/<id>/stock  | Update stock of a material           |

---

## Departments and Employees

| Method | Route         | Description                      |
|--------|---------------|----------------------------------|
| GET    | /departments  | List all departments             |
| GET    | /employees    | List all employees with details  |
| POST   | /employees    | Add a new employee               |

---

## Cost Centers and Expenses

| Method | Route           | Description                   |
|--------|-----------------|-------------------------------|
| GET    | /cost_centers   | List all cost centers         |
| POST   | /expenses       | Log a new expense             |

---

## Sales Orders

| Method | Route                        | Description                          |
|--------|------------------------------|--------------------------------------|
| POST   | /sales_orders                | Create new sales order               |
| PUT    | /sales_orders/<id>/status    | Update sales order status            |
| GET    | /sales_orders/<id>           | Get details of a specific order      |

---

## Production Orders

| Method | Route                            | Description                          |
|--------|----------------------------------|--------------------------------------|
| POST   | /production_orders               | Create new production order          |
| PUT    | /production_orders/<id>/status  | Update production order status       |

---

## Optional and Helper Routes

| Method | Route               | Description                             |
|--------|---------------------|-----------------------------------------|
| GET    | /materials/low-stock| List materials below stock threshold    |

---

## Total: 15 Core Routes

These routes cover all master data and transaction flows needed to support the six business use cases documented in the project.