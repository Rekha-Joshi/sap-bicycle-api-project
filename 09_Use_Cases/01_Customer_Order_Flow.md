# 🚴‍♀️ Use Case: Customer Order to Delivery (End-to-End Flow)

This use case simulates a complete ERP-style process where a customer places an order for a bicycle. It follows the key SAP modules: SD, MM, PP, FI/CO, and HCM.

---

## 📦 Scenario Summary

A customer places an order for 2 “Mountain Bikes.”  
The system checks inventory, triggers production if needed, tracks employee involvement, and logs costs — mimicking real SAP-style processes.

---

## 🔁 Step-by-Step Flow

### 1️⃣ Add New Customer
- Endpoint: `POST /customers`
- Data stored in: `customers` table

### 2️⃣ Create Sales Order
- Endpoint: `POST /sales_orders`
- References:
  - `customer_id` → `customers`
  - `material_id` → `materials`
- Status: `"pending"` or `"confirmed"`

### 3️⃣ Check Inventory
- Endpoint: `GET /materials`
- Logic:
  - If `stock < quantity ordered`, create a production order

### 4️⃣ Trigger Production Order (if needed)
- Endpoint: `POST /production_orders`
- References:
  - `material_id` (finished product)
- Status: `"in_progress"` → `"completed"`
- Stock updates:
  - Reduce raw material stock
  - Increase finished product stock

### 5️⃣ Log Production Cost
- Endpoint: `POST /expenses`
- References:
  - `cost_center_id` → `cost_centers`
- Example:
  - Labor cost, materials used, machine time

### 6️⃣ Employee Assignment (optional for now)
- Link employees involved in production via `employees` table
- Each belongs to a `department`

### 7️⃣ Update Sales Order Status
- Endpoint: `PUT /sales_orders/<id>`
- Set status to `"shipped"`

---

## 🔗 Tables Involved

| Table | Role |
|-------|------|
| `customers` | Stores customer details |
| `sales_orders` | Tracks customer orders |
| `materials` | Tracks inventory (bikes, raw materials) |
| `production_orders` | Records internal manufacturing |
| `expenses` | Logs cost of production |
| `cost_centers` | Categorizes financial tracking |
| `employees` | Stores worker info |
| `departments` | Groups employees |

---

## 🧠 SAP Module Mapping

| SAP Module | Simulated Tables |
|------------|------------------|
| **SD** (Sales & Distribution) | `customers`, `sales_orders` |
| **MM** (Material Management) | `materials`, `vendors` |
| **PP** (Production Planning) | `production_orders` |
| **FI/CO** (Finance/Controlling) | `expenses`, `cost_centers` |
| **HCM** (Human Capital Mgmt) | `employees`, `departments` |

---

## ✅ Goal of This Use Case

- Demonstrate end-to-end API flow like a real ERP system
- Test integration between modules
- Showcase realistic QA testing scenarios for interviews or demos

