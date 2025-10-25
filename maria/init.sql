CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  email VARCHAR(100) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email) VALUES 
('momo', 'momo@example.com'),
('lolo', 'lolo@gmail.com'),
('meriem', 'meriem@gmail.com'),
('nour', 'nour@gmail.com');



