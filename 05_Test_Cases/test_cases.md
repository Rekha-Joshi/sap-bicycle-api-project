## Materials
- Create new material → should save successfully with all details
- Create new material (batch mixed) → should reject when one item is invalid
- Create new material (default reorder level) → if not given, system should set a default value
- Create new material (duplicate) → should not allow same material name twice
- Create new material (missing name) → should show error for missing name
- Get all materials → should return a list of materials (can be empty)
- Get material by ID → should return the material if it exists, or error if not
- Filter materials by type, name, or stock → should only return matching items
- Update material details (name, type, unit price) → should update fields correctly
- Update stock by ID → should change the stock level for that material
- Assign vendor → should work for raw materials, and show error for finished ones
- Get low stock list → should return items below the given threshold

## Customers
- Create new customer → should save successfully with all details
- Create duplicate customer (email) → should not allow same email twice
- Get all customers → should return a list of customers
- Get customer by ID → should return the customer if it exists, or error if not
- Update customer fields → should update given fields correctly

## Vendors
- Create new vendor → should save successfully with all details
- Create duplicate vendor (name) → should not allow same vendor name twice
- Get all vendors → should return a list of vendors
- Get vendor by ID → should return the vendor if it exists, or error if not
- Get materials by vendor ID → should return only materials linked to that vendor

## Sales Orders
- Create new sales order → should create an order with default status as Pending
- Create sales order with missing customer/material → should show error
- Get all sales orders → should return a list of orders
- Get sales order by ID → should return the order if it exists, or error if not
- Mark order as Shipped → should only work if order is Confirmed
- Mark order as Cancelled → should only work if order is Pending, and linked production/expenses should also be cancelled

## Production Orders
- Create new production order → should link to a Pending sales order
- Get all production orders → should return a list of production orders
- Get production order by ID → should return the production order if it exists, or error if not
- Mark order as Started → should only work if order is Planned
- Mark order as Completed → should update order status correctly. update materials and sales order accordingly.

## Employees
- Create new employee → should save successfully with details
- Get all employees → should return a list of employees

## Expenses
- Create new expense → should link to either a sales order or a production order
- Get all expenses → should return a list of expenses
- Get expense by ID → should return the expense if it exists, or error if not

## Cost Centers
- Create new cost center → should not allow duplicates
- Get all cost centers → should return a list of cost centers
- Get cost center by ID → should return the cost center if it exists, or error if not
