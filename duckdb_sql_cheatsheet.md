# DuckDB SQL Cheatsheet for Beginners

> **What is DuckDB?**  
> DuckDB is a fast, embedded analytical database — think SQLite but designed for analytics. You can query CSV, Parquet, and JSON files directly, without loading them into a database first.

---

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Data Types](#data-types)
3. [Creating & Managing Tables](#creating--managing-tables)
4. [Inserting Data](#inserting-data)
5. [Querying Data — SELECT](#querying-data--select)
6. [Filtering — WHERE](#filtering--where)
7. [Sorting — ORDER BY](#sorting--order-by)
8. [Limiting Results — LIMIT & OFFSET](#limiting-results--limit--offset)
9. [Aggregations — GROUP BY](#aggregations--group-by)
10. [Filtering Groups — HAVING](#filtering-groups--having)
11. [Joining Tables — JOIN](#joining-tables--join)
12. [Subqueries](#subqueries)
13. [Common Table Expressions — WITH (CTE)](#common-table-expressions--with-cte)
14. [Window Functions](#window-functions)
15. [Updating & Deleting Data](#updating--deleting-data)
16. [Altering Tables](#altering-tables)
17. [DuckDB Superpowers — Reading Files Directly](#duckdb-superpowers--reading-files-directly)
18. [String Functions](#string-functions)
19. [Date & Time Functions](#date--time-functions)
20. [Conditional Logic — CASE WHEN](#conditional-logic--case-when)
21. [NULL Handling](#null-handling)
22. [Set Operations — UNION, INTERSECT, EXCEPT](#set-operations--union-intersect-except)
23. [Useful DuckDB-Specific Commands](#useful-duckdb-specific-commands)
24. [Quick Reference Card](#quick-reference-card)

---

## Core Concepts

SQL (Structured Query Language) is how you talk to a database. Think of it like this:

- A **database** is a collection of tables.
- A **table** is like an Excel sheet — rows and columns.
- A **row** is one record (e.g., one person, one sale).
- A **column** is one field (e.g., `name`, `age`, `price`).
- A **query** is a question you ask the database (e.g., "give me all sales from last month").

SQL keywords are case-insensitive (`SELECT` = `select`), but uppercase is convention.

---

## Data Types

When you create a table, each column must have a type.

| Type | What it stores | Example |
|------|---------------|---------|
| `INTEGER` / `INT` | Whole numbers | `42`, `-7` |
| `BIGINT` | Very large whole numbers | `9000000000` |
| `DOUBLE` / `FLOAT` | Decimal numbers | `3.14` |
| `VARCHAR` / `TEXT` | Text strings | `'hello'` |
| `BOOLEAN` | True or false | `true`, `false` |
| `DATE` | Calendar date | `'2024-01-15'` |
| `TIMESTAMP` | Date + time | `'2024-01-15 09:30:00'` |
| `BLOB` | Raw binary data | file bytes |

---

## Creating & Managing Tables

### CREATE TABLE

Define a new table with its columns and types.

```sql
CREATE TABLE employees (
    id        INTEGER,
    name      VARCHAR,
    department VARCHAR,
    salary    DOUBLE,
    hire_date DATE
);
```

### CREATE TABLE IF NOT EXISTS

Only creates the table if it doesn't already exist. Safe to run multiple times.

```sql
CREATE TABLE IF NOT EXISTS employees (
    id   INTEGER,
    name VARCHAR
);
```

### PRIMARY KEY

A primary key uniquely identifies each row. No duplicates, no NULLs allowed.

```sql
CREATE TABLE employees (
    id        INTEGER PRIMARY KEY,
    name      VARCHAR NOT NULL,   -- NOT NULL means this field is required
    salary    DOUBLE DEFAULT 0.0  -- DEFAULT sets value when none is given
);
```

### DROP TABLE

Permanently deletes a table and all its data.

```sql
DROP TABLE employees;

-- Safer version — won't error if table doesn't exist:
DROP TABLE IF EXISTS employees;
```

### SHOW TABLES / DESCRIBE

```sql
SHOW TABLES;           -- list all tables in current database
DESCRIBE employees;    -- show columns and types of a table
```

---

## Inserting Data

### INSERT INTO

Add one or more rows to a table.

```sql
-- Single row
INSERT INTO employees (id, name, department, salary, hire_date)
VALUES (1, 'Alice', 'Engineering', 95000, '2021-03-15');

-- Multiple rows at once
INSERT INTO employees VALUES
    (2, 'Bob',   'Marketing',   72000, '2020-07-01'),
    (3, 'Carol', 'Engineering', 110000, '2019-01-20'),
    (4, 'Dave',  'HR',          65000, '2022-11-01');
```

---

## Querying Data — SELECT

`SELECT` is the most used command. It retrieves data.

```sql
-- Get all columns
SELECT * FROM employees;

-- Get specific columns
SELECT name, salary FROM employees;

-- Rename a column in the output (alias)
SELECT name, salary AS annual_pay FROM employees;

-- Do math inline
SELECT name, salary, salary * 1.1 AS salary_with_raise FROM employees;

-- Remove duplicate values
SELECT DISTINCT department FROM employees;
```

**Mental model:** `SELECT` = "give me", `FROM` = "from this table".

---

## Filtering — WHERE

`WHERE` narrows down which rows you see.

```sql
-- Exact match
SELECT * FROM employees WHERE department = 'Engineering';

-- Comparison operators: =  !=  <  >  <=  >=
SELECT * FROM employees WHERE salary > 80000;

-- Multiple conditions with AND / OR
SELECT * FROM employees WHERE department = 'Engineering' AND salary > 90000;
SELECT * FROM employees WHERE department = 'HR' OR salary < 70000;

-- Range (inclusive)
SELECT * FROM employees WHERE salary BETWEEN 70000 AND 100000;

-- Match a list of values
SELECT * FROM employees WHERE department IN ('Engineering', 'Marketing');

-- NOT IN — exclude values
SELECT * FROM employees WHERE department NOT IN ('HR');

-- Pattern matching with LIKE
-- % = any number of characters, _ = exactly one character
SELECT * FROM employees WHERE name LIKE 'A%';    -- starts with A
SELECT * FROM employees WHERE name LIKE '%ob';   -- ends with ob
SELECT * FROM employees WHERE name LIKE '_a%';   -- second letter is a
```

---

## Sorting — ORDER BY

`ORDER BY` sorts your results.

```sql
-- Ascending (default, smallest first)
SELECT * FROM employees ORDER BY salary;

-- Descending (largest first)
SELECT * FROM employees ORDER BY salary DESC;

-- Sort by multiple columns
SELECT * FROM employees ORDER BY department ASC, salary DESC;

-- Sort by column position (2nd column)
SELECT name, salary FROM employees ORDER BY 2 DESC;
```

---

## Limiting Results — LIMIT & OFFSET

`LIMIT` caps how many rows are returned. `OFFSET` skips rows (useful for pagination).

```sql
-- Top 3 highest paid employees
SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3;

-- Skip first 2 rows, get next 3 (page 2 of results)
SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3 OFFSET 2;
```

---

## Aggregations — GROUP BY

Aggregate functions collapse many rows into a single summary value.

| Function | What it does |
|----------|-------------|
| `COUNT(*)` | Count rows |
| `COUNT(col)` | Count non-NULL values in column |
| `SUM(col)` | Add up all values |
| `AVG(col)` | Average of values |
| `MIN(col)` | Smallest value |
| `MAX(col)` | Largest value |

```sql
-- Total number of employees
SELECT COUNT(*) FROM employees;

-- Average salary across everyone
SELECT AVG(salary) AS avg_salary FROM employees;

-- Count and average salary per department
SELECT
    department,
    COUNT(*) AS headcount,
    AVG(salary) AS avg_salary,
    MAX(salary) AS top_salary
FROM employees
GROUP BY department;
```

**Rule:** When using `GROUP BY`, every column in `SELECT` must either be in `GROUP BY` or inside an aggregate function.

---

## Filtering Groups — HAVING

`HAVING` is like `WHERE` but for groups (after aggregation).

```sql
-- Only show departments with more than 1 employee
SELECT department, COUNT(*) AS headcount
FROM employees
GROUP BY department
HAVING COUNT(*) > 1;

-- Departments where average salary exceeds 80k
SELECT department, AVG(salary) AS avg_sal
FROM employees
GROUP BY department
HAVING AVG(salary) > 80000;
```

**When to use what:**
- `WHERE` → filter individual rows BEFORE grouping
- `HAVING` → filter groups AFTER aggregation

---

## Joining Tables — JOIN

Joins combine rows from two tables based on a related column.

### Setup for examples

```sql
CREATE TABLE departments (
    dept_name VARCHAR PRIMARY KEY,
    location  VARCHAR,
    budget    DOUBLE
);

INSERT INTO departments VALUES
    ('Engineering', 'Berlin',    500000),
    ('Marketing',   'Frankfurt', 200000),
    ('HR',          'Munich',    150000),
    ('Finance',     'Hamburg',   300000);  -- No employees in Finance yet
```

### INNER JOIN

Returns only rows where there's a match in BOTH tables.

```sql
SELECT e.name, e.salary, d.location
FROM employees e
INNER JOIN departments d ON e.department = d.dept_name;
-- Finance won't appear (no employees), nor will employees with no department
```

### LEFT JOIN (LEFT OUTER JOIN)

Returns ALL rows from the left table, and matching rows from the right. Unmatched right rows become NULL.

```sql
SELECT e.name, d.location
FROM employees e
LEFT JOIN departments d ON e.department = d.dept_name;
-- All employees shown; if no matching department, location = NULL
```

### RIGHT JOIN

Opposite of LEFT JOIN — all rows from the right table are kept.

```sql
SELECT e.name, d.dept_name, d.location
FROM employees e
RIGHT JOIN departments d ON e.department = d.dept_name;
-- All departments shown, including Finance with NULL employee name
```

### FULL JOIN (FULL OUTER JOIN)

Returns everything from both sides. NULLs fill in where there's no match.

```sql
SELECT e.name, d.dept_name
FROM employees e
FULL JOIN departments d ON e.department = d.dept_name;
```

### CROSS JOIN

Every row from table A combined with every row from table B. Rarely used but powerful.

```sql
SELECT e.name, d.dept_name
FROM employees e
CROSS JOIN departments d;
-- 4 employees × 4 departments = 16 rows
```

**Cheat sheet:**

```
INNER JOIN  → only matching rows
LEFT JOIN   → all left + matching right (NULLs for no match)
RIGHT JOIN  → all right + matching left (NULLs for no match)
FULL JOIN   → everything from both sides
```

---

## Subqueries

A subquery is a query nested inside another query, wrapped in `()`.

```sql
-- Find employees who earn more than the average salary
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Find departments that have at least one employee
SELECT dept_name FROM departments
WHERE dept_name IN (SELECT DISTINCT department FROM employees);
```

Subqueries can go in `WHERE`, `FROM`, or `SELECT` clauses.

---

## Common Table Expressions — WITH (CTE)

CTEs are named, temporary results you define at the top of your query. They make complex queries readable.

```sql
-- Step 1: Define the CTE
WITH high_earners AS (
    SELECT name, salary, department
    FROM employees
    WHERE salary > 80000
)
-- Step 2: Use it like a regular table
SELECT department, COUNT(*) AS count, AVG(salary) AS avg_sal
FROM high_earners
GROUP BY department;
```

You can chain multiple CTEs:

```sql
WITH
dept_stats AS (
    SELECT department, AVG(salary) AS avg_sal
    FROM employees
    GROUP BY department
),
rich_depts AS (
    SELECT department FROM dept_stats WHERE avg_sal > 85000
)
SELECT e.name, e.salary
FROM employees e
JOIN rich_depts r ON e.department = r.department;
```

**Use CTEs when:** your query has multiple logical steps, or when you'd otherwise repeat a subquery.

---

## Window Functions

Window functions compute values across a "window" of rows related to the current row — without collapsing rows like `GROUP BY` does.

```sql
-- Rank employees by salary within their department
SELECT
    name,
    department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;

-- Running total of salaries
SELECT
    name,
    salary,
    SUM(salary) OVER (ORDER BY hire_date) AS cumulative_salary
FROM employees;

-- Each employee's salary vs department average
SELECT
    name,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS dept_avg,
    salary - AVG(salary) OVER (PARTITION BY department) AS diff_from_avg
FROM employees;
```

### Common window functions

| Function | What it does |
|----------|-------------|
| `ROW_NUMBER()` | Unique row number (1, 2, 3...) |
| `RANK()` | Rank with gaps on ties (1, 1, 3) |
| `DENSE_RANK()` | Rank without gaps (1, 1, 2) |
| `LAG(col, n)` | Value from n rows before current |
| `LEAD(col, n)` | Value from n rows after current |
| `SUM() OVER` | Running/cumulative sum |
| `AVG() OVER` | Rolling average |
| `FIRST_VALUE()` | First value in the window |
| `LAST_VALUE()` | Last value in the window |

**Syntax pattern:**
```sql
FUNCTION() OVER (
    PARTITION BY column   -- group by (optional)
    ORDER BY column       -- sort within group
)
```

---

## Updating & Deleting Data

### UPDATE

Modify existing rows.

```sql
-- Give Engineering a 10% raise
UPDATE employees
SET salary = salary * 1.10
WHERE department = 'Engineering';

-- Update multiple columns at once
UPDATE employees
SET salary = 75000, department = 'Marketing'
WHERE name = 'Dave';
```

**Always include a `WHERE` clause** — without it, you update every single row.

### DELETE

Remove rows from a table.

```sql
-- Delete a specific employee
DELETE FROM employees WHERE id = 4;

-- Delete all HR employees
DELETE FROM employees WHERE department = 'HR';

-- Delete all rows (keeps table structure)
DELETE FROM employees;

-- Even faster full wipe:
TRUNCATE employees;
```

---

## Altering Tables

### ALTER TABLE

Modify an existing table's structure.

```sql
-- Add a new column
ALTER TABLE employees ADD COLUMN email VARCHAR;

-- Drop a column
ALTER TABLE employees DROP COLUMN email;

-- Rename a column
ALTER TABLE employees RENAME COLUMN salary TO annual_salary;

-- Change a column's type
ALTER TABLE employees ALTER COLUMN annual_salary TYPE INTEGER;
```

---

## DuckDB Superpowers — Reading Files Directly

DuckDB can query files without importing them. This is one of its biggest strengths.

### CSV Files

```sql
-- Read a CSV file directly
SELECT * FROM read_csv_auto('sales_data.csv');

-- Query it like a table
SELECT product, SUM(amount)
FROM read_csv_auto('sales_data.csv')
GROUP BY product;

-- Load CSV into a table
CREATE TABLE sales AS SELECT * FROM read_csv_auto('sales_data.csv');
```

### Parquet Files

```sql
SELECT * FROM read_parquet('data.parquet');

-- Glob patterns — read multiple files at once
SELECT * FROM read_parquet('data/*.parquet');
```

### JSON Files

```sql
SELECT * FROM read_json_auto('events.json');
```

### From a URL (HTTP)

```sql
SELECT * FROM read_csv_auto('https://example.com/data.csv');
```

---

## String Functions

```sql
SELECT
    UPPER('hello'),                    -- 'HELLO'
    LOWER('WORLD'),                    -- 'world'
    LENGTH('Alice'),                   -- 5
    TRIM('  hello  '),                 -- 'hello'
    LTRIM('  hello'),                  -- 'hello'
    RTRIM('hello  '),                  -- 'hello'
    SUBSTRING('Frankfurt', 1, 5),      -- 'Frank'  (1-indexed)
    REPLACE('hello world', 'world', 'DuckDB'), -- 'hello DuckDB'
    CONCAT('Hello', ' ', 'World'),     -- 'Hello World'
    'Hello' || ' ' || 'World',        -- 'Hello World' (|| = concatenation)
    CONTAINS('Frankfurt', 'frank'),    -- false (case-sensitive)
    STARTS_WITH('Frankfurt', 'Frank'), -- true
    ENDS_WITH('Frankfurt', 'furt'),    -- true
    SPLIT_PART('a,b,c', ',', 2);      -- 'b'
```

---

## Date & Time Functions

```sql
SELECT
    CURRENT_DATE,                          -- today's date
    CURRENT_TIMESTAMP,                     -- now (date + time)
    DATE '2024-01-15',                     -- date literal
    EXTRACT(YEAR FROM DATE '2024-03-10'),  -- 2024
    EXTRACT(MONTH FROM DATE '2024-03-10'), -- 3
    EXTRACT(DAY FROM DATE '2024-03-10'),   -- 10
    DATEDIFF('day', DATE '2024-01-01', DATE '2024-03-10'),  -- days between
    DATE '2024-01-15' + INTERVAL '30 days',  -- add 30 days
    DATE_TRUNC('month', DATE '2024-03-15'),  -- '2024-03-01'
    STRFTIME(CURRENT_DATE, '%Y-%m');         -- '2026-03'
```

---

## Conditional Logic — CASE WHEN

`CASE WHEN` is SQL's if/else.

```sql
-- Simple label based on salary band
SELECT
    name,
    salary,
    CASE
        WHEN salary >= 100000 THEN 'Senior'
        WHEN salary >= 80000  THEN 'Mid-level'
        ELSE 'Junior'
    END AS seniority_band
FROM employees;

-- Conditional aggregation (count only Engineering employees)
SELECT
    COUNT(CASE WHEN department = 'Engineering' THEN 1 END) AS eng_count,
    COUNT(*) AS total_count
FROM employees;
```

---

## NULL Handling

`NULL` means "no value". It behaves differently from zero or empty string.

```sql
-- IS NULL / IS NOT NULL
SELECT * FROM employees WHERE email IS NULL;
SELECT * FROM employees WHERE email IS NOT NULL;

-- COALESCE: return first non-NULL value
SELECT name, COALESCE(email, 'no-email@company.com') AS contact
FROM employees;

-- NULLIF: return NULL if two values are equal (avoids divide-by-zero)
SELECT salary / NULLIF(hours_worked, 0) AS hourly_rate FROM employees;

-- IFNULL: like COALESCE but only two arguments
SELECT IFNULL(email, 'unknown') FROM employees;
```

**Key rule:** `NULL = NULL` is NOT true in SQL — use `IS NULL` not `= NULL`.

---

## Set Operations — UNION, INTERSECT, EXCEPT

Combine results from two queries. Both queries must have the same number of columns and compatible types.

```sql
-- UNION: combine results, remove duplicates
SELECT name FROM employees WHERE department = 'Engineering'
UNION
SELECT name FROM employees WHERE salary > 100000;

-- UNION ALL: combine results, keep duplicates (faster)
SELECT department FROM employees
UNION ALL
SELECT dept_name FROM departments;

-- INTERSECT: only rows that appear in BOTH results
SELECT department FROM employees
INTERSECT
SELECT dept_name FROM departments;

-- EXCEPT: rows in first result but NOT in second
SELECT dept_name FROM departments
EXCEPT
SELECT DISTINCT department FROM employees;
-- Returns departments that have no employees
```

---

## Useful DuckDB-Specific Commands

```sql
-- Show all tables
SHOW TABLES;

-- Show table schema
DESCRIBE employees;
-- or
PRAGMA table_info('employees');

-- Quick data overview (like df.describe() in pandas)
SUMMARIZE employees;

-- Export query result to CSV
COPY (SELECT * FROM employees) TO 'output.csv' (HEADER, DELIMITER ',');

-- Export to Parquet
COPY employees TO 'employees.parquet' (FORMAT PARQUET);

-- Export to JSON
COPY employees TO 'employees.json' (FORMAT JSON);

-- Install and load extensions (e.g. for Excel support)
INSTALL spatial;
LOAD spatial;

-- Enable progress bar for long queries
PRAGMA enable_progress_bar;

-- Check DuckDB version
SELECT version();
```

---

## Quick Reference Card

```
CREATE TABLE   → define a new table
DROP TABLE     → delete a table
INSERT INTO    → add rows
SELECT         → query/retrieve data
WHERE          → filter rows
ORDER BY       → sort results
LIMIT          → cap number of rows
GROUP BY       → aggregate into groups
HAVING         → filter groups
JOIN           → combine tables
UNION          → merge query results
UPDATE         → modify existing rows
DELETE         → remove rows
WITH (CTE)     → named temp query result
CASE WHEN      → if/else logic
COALESCE       → handle NULLs
```

### Query Execution Order (what SQL does internally)

Even though you write `SELECT` first, SQL processes clauses in this order:

```
1. FROM / JOIN       ← which tables?
2. WHERE             ← filter rows
3. GROUP BY          ← make groups
4. HAVING            ← filter groups
5. SELECT            ← pick columns / compute
6. ORDER BY          ← sort
7. LIMIT / OFFSET    ← trim output
```

Understanding this helps debug errors like "column not found in WHERE" when referencing an alias defined in SELECT.

---

*Generated for DuckDB. Most standard SQL applies to PostgreSQL, SQLite, and others with minor differences.*
