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

## Testing
- Open Postman and make a GET request to /materials/low-stock
- Add a query parameter called threshold (e.g., ?threshold=30)
- Check the response:
    - If some materials have stock below 30, they should be listed in the "items" array
    - If all materials have stock above 30, the message should say: "All materials are sufficiently stocked"
    - Try changing the threshold value (e.g., 10 or 100) to see different results
    - Confirm that the response shows both a clear message and the matching materials (if any)