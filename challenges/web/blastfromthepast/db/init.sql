CREATE DATABASE IF NOT EXISTS secureblocks;
USE secureblocks;

CREATE TABLE users 
(username VARCHAR(255), password VARCHAR(255), diamonds INT(64));

INSERT INTO users (username,password,diamonds) 
VALUES 
('admin','D0NT_M1N3_4T_N1GHT_57183812570812',9999999);