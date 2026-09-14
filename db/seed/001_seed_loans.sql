INSERT INTO loans (
    borrower_name,
    loan_amount,
    property_city,
    status
)
SELECT *
FROM (
    VALUES
        ('Aarav Sharma', 4500000.00, 'Lucknow', 'APPROVED'),
        ('Priya Verma', 3200000.00, 'Kanpur', 'PENDING'),
        ('Rohan Singh', 5750000.00, 'Noida', 'UNDER_REVIEW'),
        ('Neha Gupta', 2800000.00, 'Lucknow', 'APPROVED'),
        ('Arjun Mehta', 6100000.00, 'Delhi', 'PENDING')
) AS seed_data(
    borrower_name,
    loan_amount,
    property_city,
    status
)
WHERE NOT EXISTS (
    SELECT 1 FROM loans
);