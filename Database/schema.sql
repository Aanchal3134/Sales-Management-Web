

-- Users Table
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL, -- Note: Passwords should be hashed before storing
    role TEXT CHECK(role IN ('Sales Representative', 'Manager', 'Product Team', 'Marketing Team', 'Executive Lead')) NOT NULL
);

-- Products Table
CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);

-- Sales Table
CREATE TABLE Sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    region_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total_price REAL NOT NULL,
    sale_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (region_id) REFERENCES Regions(region_id)
);

-- Regions Table
CREATE TABLE Regions (
    region_id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_name TEXT NOT NULL UNIQUE
);

-- Teams Table
-- Teams Table
CREATE TABLE Teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL,
    manager_id INTEGER NOT NULL,
    FOREIGN KEY (manager_id) REFERENCES Users(user_id)
);

-- Trigger to Update Product Stock After a Sale
CREATE TRIGGER update_stock AFTER INSERT ON Sales
BEGIN
    UPDATE Products
    SET stock = stock - NEW.quantity
    WHERE product_id = NEW.product_id;
END;

-- Indexes for Faster Queries
CREATE INDEX idx_users_email ON Users(email);
CREATE INDEX idx_products_name ON Products(product_name);
CREATE INDEX idx_sales_region_id ON Sales(region_id);

-- Sample Data
-- Inserting Users (Passwords should be hashed before insertion)
INSERT INTO Users (username, email, password, role)
VALUES
('John Doe', 'johndoe@example.com', '$2b$12$e.BCR9Ro.1Hb9w/UPEkU2uBxdCkH.T3h17YLy4l09/u9.BcClEbKu', 'Sales Representative'), -- Example bcrypt hash for 'password123'
('Jane Smith', 'janesmith@example.com', '$2b$12$e.BCR9Ro.1Hb9w/UPEkU2uBxdCkH.T3h17YLy4l09/u9.BcClEbKu', 'Manager');

-- Inserting Products
INSERT INTO Products (product_name, category, price, stock)
VALUES
('Product A', 'Electronics', 100.00, 50),
('Product B', 'Clothing', 20.00, 200);

-- Inserting Regions
INSERT INTO Regions (region_name)
VALUES
('Singapore'),
('South Asia'),
('Australia');

-- Inserting Sales Data
INSERT INTO Sales (product_id, user_id, region_id, quantity, total_price)
VALUES
(1, 1, 1, 2, 200.00), -- 2 units of Product A sold by John Doe in Singapore
(2, 1, 2, 5, 100.00), -- 5 units of Product B sold by John Doe in South Asia
(1, 1, 3, 4, 400.00); -- 7 units of product A sold by John Doe in Aus

-- Inserting Teams
INSERT INTO Teams (team_name, manager_id)
VALUES
('Team Alpha', 2); -- Managed by Jane Smith



-- add more teams 
INSERT INTO Teams (team_name, manager_id)
VALUES
('Marketing Team', 2), -- Managed by Jane Smith
('Sales Team', 1), -- Managed by John Doe
('Account Team', 2), -- Managed by Jane Smith
('Product Team', 1); -- Managed by John Doe



-- add more users
-- Inserting Additional Users
INSERT INTO Users (username, email, password, role)
VALUES
('Alice Johnson', 'alice.johnson@example.com', '$2b$12$e.BCR9Ro.1Hb9w/UPEkU2uBxdCkH.T3h17YLy4l09/u9.BcClEbKu', 'Marketing Team'), -- Password: password123
('Bob Williams', 'bob.williams@example.com', '$2b$12$e.BCR9Ro.1Hb9w/UPEkU2uBxdCkH.T3h17YLy4l09/u9.BcClEbKu', 'Sales Representative'), -- Password: password123
('Cathy Brown', 'cathy.brown@example.com', '$2b$12$e.BCR9Ro.1Hb9w/UPEkU2uBxdCkH.T3h17YLy4l09/u9.BcClEbKu', 'Product Team'), -- Password: password123
('David Wilson', 'david.wilson@example.com', '$2b$12$e.BCR9Ro.1Hb9w/UPEkU2uBxdCkH.T3h17YLy4l09/u9.BcClEbKu', 'Executive Lead'), -- Password: password123
('Eve Davis', 'eve.davis@example.com', '$2b$12$e.BCR9Ro.1Hb9w/UPEkU2uBxdCkH.T3h17YLy4l09/u9.BcClEbKu', 'Manager'), -- Password: password123
('Frank Thomas', 'frank.thomas@example.com', '$2b$12$e.BCR9Ro.1Hb9w/UPEkU2uBxdCkH.T3h17YLy4l09/u9.BcClEbKu', 'Marketing Team'), -- Password: password123
('Grace Lee', 'grace.lee@example.com', '$2b$12$e.BCR9Ro.1Hb9w/UPEkU2uBxdCkH.T3h17YLy4l09/u9.BcClEbKu', 'Product Team'), -- Password: password123
('Hank Green', 'hank.green@example.com', '$2b$12$e.BCR9Ro.1Hb9w/UPEkU2uBxdCkH.T3h17YLy4l09/u9.BcClEbKu', 'Sales Representative'); -- Password: password123


-- 2 Managers: Jane Smith, Eve Davis
-- 4 Sales Representatives: John Doe, Bob Williams, Hank Green, [Placeholder if needed]
-- 2 Marketing Team Members: Alice Johnson, Frank Thomas
-- 2 Product Team Members: Cathy Brown, Grace Lee
-- 1 Executive Lead: David Wilson


SELECT * FROM Users;