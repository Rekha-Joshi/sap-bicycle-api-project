# Use Case 05: Production Cost Tracking

This use case tracks how much it costs to produce finished goods like bicycles.

## Steps
1. Create production order using /production_orders (POST)
2. Calculate cost manually or assume fixed value
3. Log cost using /expenses (POST)
4. Link it to a cost center like "Manufacturing"

## Tables Involved
- production_orders
- expenses
- cost_centers
