# Database Design Overview

Below is a summary of the tables used in this project and what each one stores.

| Table Name          | Description | Key Info |
|---------------------|-------------|----------|
| `customers`         | Stores customer name, email, phone number, and address | `id` (PK) |
| `vendors`           | Stores vendor details such as name and contact info | `id` (PK) |
| `materials`         | List of raw materials and finished products with stock and price | `id` (PK) |
| `sales_orders`      | Records customer orders for specific materials | `id` (PK), `customer_id` (FK), `material_id` (FK) |
| `production_orders` | Tracks bicycle production using materials | `id` (PK), `material_id` (FK) |
| `cost_centers`      | Tracks financial cost centers and their descriptions | `id` (PK) |
| `expenses`          | Logs expenses assigned to cost centers | `id` (PK), `cost_center_id` (FK) |
| `departments`       | Stores department names | `id` (PK) |
| `employees`         | Stores employee name, job title, and department | `id` (PK), `department_id` (FK) |