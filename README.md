# Pharmacy System

A web system for a pharmacy that tracks medicine stock by batch and expiry
date, records sales, and shows which medicines are running low or expiring.

Built with Python, Flask and SQLite. Status: in development.

## What works so far
- Database for users, medicine families, products, batches, sales and sold items
- Add a new medicine with its first batch, and add stock to an existing one
- Stock list with a low-stock check, where expired batches are not counted
- Expiring and expired batch lists
- Medicine families with their total quantities
- Selling from a chosen batch, saved all or nothing

## Still to do
- Login and roles (owner, pharmacist, cashier)
- Filters and low stock screen
- History log
- Web pages with Flask
- Owner reports
