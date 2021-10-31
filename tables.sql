DROP TABLE IF EXISTS customers_and_stores;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS stores;
DROP TABLE IF EXISTS customers_errors;
DROP TABLE IF EXISTS relationships;


CREATE TABLE relationships(
    relationship_id INT GENERATED ALWAYS AS IDENTITY,
    summary VARCHAR UNIQUE NOT NULL,
    PRIMARY KEY (relationship_id)
);

CREATE TABLE stores(
    cnpj BIGINT UNIQUE NOT NULL,
    PRIMARY KEY (cnpj)
);

CREATE TABLE customers(
    cpf BIGINT UNIQUE NOT NULL,
    private BOOLEAN,
    uncompleted BOOLEAN,
    last_pucharse_date DATE,
    last_ticket_value NUMERIC,
    avg_ticket_value NUMERIC,
    PRIMARY KEY (cpf)
);
CREATE TABLE customers_errors(
    customer_errors_id INT GENERATED ALWAYS AS IDENTITY,
    data VARCHAR,
    system_error VARCHAR,
    PRIMARY KEY (customer_errors_id)
);

CREATE TABLE customers_and_stores(
    relationship_id BIGINT NOT NULL,
    cnpj BIGINT NOT NULL,
    cpf BIGINT NOT NULL,
    PRIMARY KEY (relationship_id, cnpj, cpf),
    CONSTRAINT fk_relationship
        FOREIGN KEY(relationship_id)
            REFERENCES relationships(relationship_id)
                ON DELETE SET NULL,
    CONSTRAINT fk_store
        FOREIGN KEY(cnpj)
            REFERENCES stores(cnpj)
                ON DELETE SET NULL,
    CONSTRAINT fk_customer
        FOREIGN KEY(cpf)
            REFERENCES customers(cpf)
                ON DELETE SET NULL
);

