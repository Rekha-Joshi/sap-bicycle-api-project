## Project Overview: SAP-Style Bicycle Manufacturing ERP (API Simulation)

This project simulates a lightweight, modular **ERP system** for a fictional **bicycle manufacturing company**, inspired by core **SAP modules** like SD, MM, PP, FI, and HCM.

The goal is to:
- Build backend APIs using **Python and Flask**
- Store master and transactional data in **SQLite**
- Test all APIs using **Postman**
- Document the full QA process using **GitHub**
- Practice Git-based version control and clean project structure

This end-to-end mini ERP project serves as a **QA portfolio piece**, showcasing:
- API development and testing skills using **Python + Flask**
- Understanding of **SAP-style business processes**
- Ability to work with databases using **SQL (SQLite)**
- Structured QA documentation, defect tracking, and test case management. (for later)
- Full version control with **Git and GitHub**

![Entity Relationship Diagram](../06_Diagrams/er_diagram.png)

This project is designed as a QA/Testing portfolio project, so the focus is on:
- Creating realistic API endpoints with validations
- Using SQLite as a lightweight backend
- Practicing Postman for functional and integration testing
- Showing end-to-end testing workflows

To keep the code simple and easy to follow, I placed validations directly inside the route functions instead of creating separate helper functions or classes.

In a production system, these checks would normally be moved into helper functions, classes, or middleware for reusability and maintainability.