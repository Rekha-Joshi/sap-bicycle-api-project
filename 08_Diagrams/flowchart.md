erDiagram

CUSTOMERS ||--o{ SALES_ORDERS : has
MATERIALS ||--o{ SALES_ORDERS : contains
MATERIALS ||--o{ PRODUCTION_ORDERS : used_in

VENDORS ||--o{ MATERIALS : supplies

COST_CENTERS ||--o{ EXPENSES : funds
DEPARTMENTS ||--o{ EMPLOYEES : has

SALES_ORDERS {
    int id
    int customer_id
    int material_id
    int quantity
    text order_date
    text status
}

PRODUCTION_ORDERS {
    int id
    int material_id
    int quantity
    text start_date
    text end_date
    text status
}

CUSTOMERS {
    int id
    text name
    text email
    text phone
    text address
}

MATERIALS {
    int id
    text name
    text type
    real unit_price
    int stock
}

VENDORS {
    int id
    text name
    text contact
}

COST_CENTERS {
    int id
    text code
    text name
}

EXPENSES {
    int id
    int cost_center_id
    real amount
    text description
    text expense_date
}

DEPARTMENTS {
    int id
    text name
}

EMPLOYEES {
    int id
    text name
    int department_id
    text job_title
}