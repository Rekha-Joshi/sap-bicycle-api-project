# Use Case 02: Material Stock Reorder Trigger

When stock for a raw material (like tires) falls below a certain level, the system needs to place a reorder from the vendor.

## Steps
1. Check current stock using /materials (GET)
2. If stock < threshold, identify vendor from /vendors
3. Create a new order request (could be simulated via a note or log)
4. Optionally update stock manually to simulate delivery

## Tables Involved
- materials
- vendors
