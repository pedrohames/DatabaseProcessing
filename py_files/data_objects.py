from DB import DB
from cpf_cnpj_verifier import cpf_check, cnpj_check


class Store:
    """
    Store class
    created_stores_id: dict that contains the IDs of all Stores created available to all layers of software.
    """
    created_stores = []

    def __init__(self, cnpj: str, sync_db=True):
        """
        Creates a store object
        :param cnpj: Store unique identifier
        :param sync_db: If true, saves it into Database, if False doesn't save.
        """
        possible_cnpj = cnpj_check(cnpj)  # check if cnpj is valid.
        if possible_cnpj:
            self.cnpj = possible_cnpj
        else:
            raise ValueError(f'NULL CNPJ [{cnpj}].')
        if sync_db:
            if self.cnpj not in Store.created_stores:  # Checks in class cache if it is already at databases.
                self.insert_db()
                Store.created_stores.append(self.cnpj)  # Add new store at class cache.

    def insert_db(self) -> None:
        """
        Get its own ID at database
        :return: its ID
        """
        db = DB()
        query = f"""
                INSERT INTO stores(cnpj) 
                VALUES ({self.cnpj});
                """
        db.execute_query(query, commit=True, fetch=False)


class Customer:
    """
    Customers class
    number_of_elements: represents how many columns there are in the customers table
    """

    number_of_elements = 8

    def __init__(self, elements: list, db_sync=False):
        """
        Creates a customer object
        :param elements: List of strings with all the elements necessary to create a customer, SEQUENCE MATTERS.
        E.g.: elements = ['989.106.540-58','1', '0', '2017-08-25', '139,98', '123,66',
                          '79.379.491/0001-83', '79.379.491/0008-50']

        """
        if len(elements) != Customer.number_of_elements:
            raise ValueError(f'List size should be {Customer.number_of_elements},'
                             f' not {len(elements)}\n{str(elements)}')
        possible_cpf = cpf_check(elements[0])
        if possible_cpf:
            self.cpf = possible_cpf
        else:
            raise ValueError(f'Invalid CPF: [{elements[0]}]')
        self.private = bool(int(elements[1]))
        self.uncompleted = bool(int(elements[2]))
        self.last_pucharse_date = f"'{elements[3]}'" if elements[3] != 'NULL' else 'NULL'
        self.last_ticket_value = elements[4].replace(',', '.')
        self.avg_ticket_value = elements[5].replace(',', '.')
        self.main_store = Store(elements[6]).cnpj if elements[6] != 'NULL' else 'NULL'
        self.last_store = Store(elements[7]).cnpj if elements[7] != 'NULL' else 'NULL'
        if db_sync:
            self.insert_db()

    def insert_db(self) -> None:
        """
        INSERTs itself on database.
        :return: ID created
        """
        db = DB()
        query = f"""
                INSERT INTO customers(cpf, private, uncompleted, last_pucharse_date, 
                                      last_ticket_value, avg_ticket_value)
                VALUES ({self.cpf}, {self.private}, {self.uncompleted}, {self.last_pucharse_date},
                        {self.last_ticket_value}, {self.avg_ticket_value});
                """
        db.execute_query(query, commit=True)

    @staticmethod
    def bulk_insert(customers: list) -> None:
        """
        Static method able to perform bulk INSERTs
        :param customers: list of Customer to be inserted
        """
        db = DB()

        # Creating Multi-value INSERT query below.
        query = """INSERT INTO customers(cpf, private, uncompleted, last_pucharse_date, 
                                              last_ticket_value, avg_ticket_value)
                   VALUES"""
        if len(customers) > 1:
            for cs in customers[:-1]:
                values = f"""({cs.cpf}, {cs.private}, {cs.uncompleted}, {cs.last_pucharse_date}, 
                {cs.last_ticket_value}, {cs.avg_ticket_value}),"""
                query += values
        last_cs = customers[-1]
        query += f"""({last_cs.cpf}, {last_cs.private}, {last_cs.uncompleted}, {last_cs.last_pucharse_date}, 
            {last_cs.last_ticket_value}, {last_cs.avg_ticket_value});"""

        # Executing query
        db.execute_query(query, commit=True)


class CustomerErrors:
    """
    Simple class to deal and store with customers errors
    """
    @staticmethod
    def error_insert(data, error) -> None:
        """
        Insert error log into database
        :param data: data that generate the error
        :param error: System backtrace
        """
        db = DB()
        query = f"""
                INSERT INTO customers_errors(data, system_error)
                VALUES ('{str(data)}', '{str(error)}');        
                """
        db.execute_query(query)


class Relationship:
    """
    Class represents the kind of relationships
    relationships_ids: dict that keeps in memory all the IDs, keys are based on summary.
    relationships_available list with all relationships a Customer can have with a Store.

    """
    created_relationships_ids = {}
    relationships_available = ['Main Store', 'Last Pucharse']

    def __init__(self, summary: str) -> None:
        """
        Instances a new relationship and insert it into the database.
        :param summary: Little description of the relationship
        """
        db = DB()
        self.summary = summary
        query = f"""
                    INSERT INTO relationships(summary)
                    VALUES('{summary}')
                    RETURNING relationship_id;
                    """
        self.db_id = int(db.execute_query(query, commit=True, fetch=True)[0][0])
        Relationship.created_relationships_ids[self.summary] = self.db_id


class CustomerAndStore:
    """
    Class that represents the relationships between Customers and Stores.
    """

    def __init__(self, customer: int, store: int, relationship: int):
        """
        :param customer: customer_id
        :param store: store_id
        :param relationship: relationship_id
        """
        self.cpf = customer
        self.cnpj = store
        self.relationship_id = relationship

    def insert_db(self) -> None:
        """
        Insert itself into database
        """
        query = f"""
                INSERT INTO customers_and_stores(relationship_id, cnpj, cpf)
                VALUES({self.relationship_id}, {self.cnpj}, {self.cpf});
                """
        db = DB()
        db.execute_query(query, commit=True)

    @staticmethod
    def bulk_insert(customer_and_store_list) -> None:
        """
        Static method able to perform bulk INSERTs
        :param customer_and_store_list: list of customer_and_store_list to be inserted
        """

        # Creating Multi-value INSERT query below.
        query = "INSERT INTO customers_and_stores(relationship_id, cnpj, cpf) VALUES"
        db = DB()
        if len(customer_and_store_list) > 1:
            for rl in customer_and_store_list[:-1]:
                values = f'({rl.relationship_id}, {rl.cnpj}, {rl.cpf}),'
                query += values
        last_rl = customer_and_store_list[-1]
        query += f'({last_rl.relationship_id}, {last_rl.cnpj}, {last_rl.cpf});'

        # Executing query
        db.execute_query(query, commit=True)
