CREATE TABLE IF NOT EXISTS phonebook (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL
);

CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE (
    id INT,
    username VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.username, p.phone
    FROM phonebook p
    WHERE p.username ILIKE '%' || pattern || '%'
       OR p.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, offs INT)
RETURNS TABLE (
    id INT,
    username VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.username, p.phone
    FROM phonebook p
    ORDER BY p.id
    LIMIT lim OFFSET offs;
END;
$$ LANGUAGE plpgsql;