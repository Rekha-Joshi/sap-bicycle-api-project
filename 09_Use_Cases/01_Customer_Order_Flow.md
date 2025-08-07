# Use Case 01: Customer Order to Delivery

A customer places an order for bicycles. The system checks if the product is available. If not, production is triggered. The cost of production is tracked, and the sales order is marked as shipped once ready.

## Steps

1. Add customer using /customers (POST)
2. Create sales order using /sales_orders (POST)
3. Check materials stock using /materials (GET)
4. Check if enough finished product is in stock:
   - If stock is available:
     - Skip production step
     - Go directly to fulfillment and reduce stock
   - If stock is too low:
     - Create a production order using /production_orders (POST)
     - After completion, increase stock in materials table
5. Log related costs using /expenses (POST)
6. Update sales order status to "shipped" using /sales_orders/<id> (PUT)

## Tables Involved

- customers
- sales_orders
- materials
- production_orders
- expenses
- cost_centers

Phase 1: Order Creation
  Customer orders a bicycle - Add customer
  Create /sales_orders POST
  Check if finished product stock is enough
  If yes → update stock + create order as confirmed
Phase 2: If Out of Stock
  Trigger /production_orders
  Add stock after production completes
  Update order status
Phase 3: Track Cost and Shipping
  Add expense record
  Update status to “shipped”