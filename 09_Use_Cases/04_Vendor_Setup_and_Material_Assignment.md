# Use Case 04: Vendor Setup and Material Assignment

A new vendor is added to the system. The vendor is assigned to supply certain raw materials.

## Steps
1. Add vendor using /vendors (POST)
2. Add or update materials to link vendor name
3. Vendor name or ID can be used later to simulate procurement

## Tables Involved
- vendors
- materials

## Testing
- Added a new vendor using POST /vendors with name and contact details.
- Added a new raw material using POST /materials (if it didn’t already exist).
- Assigned the vendor to a raw material using PUT /materials/assign-vendor.
- Verified that:
    - The vendor and material both exist before assignment
    - Finished products cannot be assigned a vendor
    - Appropriate error messages are returned for invalid inputs
    - Tested all routes successfully using Postman.