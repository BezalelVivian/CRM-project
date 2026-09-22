USE crm_db;

INSERT INTO clients
(client_date, name, email, phone, company, budget, status, source, notes)
VALUES
('2026-09-01', 'Arun Kumar', 'arun@example.com', '+91 9876543210', 'Arun Tech', 85000, 'Lead', 'Website', 'Interested in annual service plan.'),
('2026-09-03', 'Priya Menon', 'priya@example.com', '+91 9876543211', 'Menon Foods', 125000, 'Prospect', 'Referral', 'Follow up next week.'),
('2026-09-05', 'Rahul Nair', 'rahul@example.com', '+91 9876543212', 'Nair Solutions', 210000, 'Customer', 'LinkedIn', 'Converted customer.'),
('2026-09-07', 'Divya Raj', 'divya@example.com', '+91 9876543213', 'DR Studio', 65000, 'Churned', 'Advertisement', 'Previous customer.'),
('2026-09-10', 'Karthik S', 'karthik@example.com', '+91 9876543214', 'Karthik Retail', 175000, 'Prospect', 'Event', 'Needs a proposal.'),
('2026-09-12', 'Meera Joseph', 'meera@example.com', '+91 9876543215', 'MJ Consulting', 95000, 'Lead', 'Cold Call', 'Initial conversation completed.');
