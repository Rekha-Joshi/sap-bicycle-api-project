# Use Case 03: Employee Onboarding

When a new employee joins the company, they need to be added to the system and assigned to a department.

## Steps
1. Add department if it does not exist using /departments (POST)
2. Add employee using /employees (POST)
3. Optionally assign cost center or note role in production

## Tables Involved
- employees
- departments

## Testing
- I tested the /employees endpoint using Postman.
- I added a new employee with name, department name, and job title.
- It worked and showed a success message.
- I also tested with a wrong department name, and it gave an error.
- Then I tried missing fields like name or job title, and it showed a proper error message.