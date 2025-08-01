# Use Case 06: Sales Order Cancellation

If a customer cancels their order, the system updates the sales order and restores the product stock if needed.

## Steps
1. Find the sales order by ID using /sales_orders (GET)
2. Update order status to "cancelled" using /sales_orders/<id> (PUT)
3. Optionally adjust stock in materials table manually or through a helper route

## Tables Involved
- sales_orders
- materials
