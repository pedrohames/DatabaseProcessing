from data_objects import Customer, Store, Relationship, CustomerErrors, CustomerAndStore
import sys
import numpy as np


class StoresCreator(Store):
    """
    A class to deal with Store creating.
    """

    @staticmethod
    def create_store(cnpj) -> int:
        """
        Creates a store and save it into database
        :param cnpj: CNPJ of store
        :return cnpj with only numbers
        """
        if cnpj in Store.created_stores:
            return cnpj
        else:
            return Store(cnpj, sync_db=True).cnpj


class RelationshipCreator(Relationship):
    """
    A class to deal with Relationship creating.
    """
    @staticmethod
    def create_relationship(summary):
        if summary in Relationship.created_relationships_ids.keys():
            return Relationship.created_relationships_ids[summary]
        else:
            relationship = Relationship(summary)
        return relationship.db_id


class DataHandler:
    """
    Class to perform some general data processing
    split_size = Size of the bulk INSERTs
    """

    split_size = 1000

    @staticmethod
    def data_split(data_list) -> list:
        """
        Splits a big list into n lists of DataHandler.split_size.
        :param data_list: List to be splited.
        :return: Return a list with the new smaller lists from spliting.
        """
        data_list_len = len(data_list)
        divider = np.ceil(data_list_len/DataHandler.split_size)
        new_arrays = np.array_split(data_list, divider)
        new_lists = []
        for array in new_arrays:
            new_lists.append(list(array))
        return new_lists

    @staticmethod
    def txt_file_read(path: str) -> list:
        """
        Reads a text file and return its content.
        :param path: File path

        :returns List of file lines
        """
        with open(path, 'r') as f:
            return f.readlines()

    @staticmethod
    def customer_creator(database_lines) -> None:
        """
        Static method to start the data processing.
        Deals with Customers, Stores, relationships, and general data processing.
        :param database_lines: Lines from text database.
        """
        customers = []
        cs_and_stores = []

        # Creates Relationships available and inserts them into databases.
        for relationship in Relationship.relationships_available:
            RelationshipCreator.create_relationship(relationship)
        no_header_database = database_lines[1:]

        # Creates data objects, data verification is done here down below.
        for data in no_header_database:
            try:
                cs = Customer(data.split())  # Creates a customer object.
                customers.append(cs)  # Adds the Customer created into a list.

                # Deals with last stores
                if cs.last_store != 'NULL':  # Creates an relationship object if last_store is not NULL
                    last_store_rl_id = Relationship.created_relationships_ids[Relationship.relationships_available[0]]
                    # Adds the relationship created into a list
                    cs_and_stores.append(CustomerAndStore(cs.cpf, cs.last_store, last_store_rl_id))

                # Deals with main stores
                if cs.main_store != 'NULL':  # Creates an relationship object if main_store is not NULL
                    main_store_rl_id = Relationship.created_relationships_ids[Relationship.relationships_available[1]]
                    # Adds the relationship created into a list
                    cs_and_stores.append(CustomerAndStore(cs.cpf, cs.main_store, main_store_rl_id))

            # Error handling
            except ConnectionError:
                sys.exit('Unable to communicate with DATABASE')
            except ValueError as exc:
                CustomerErrors.error_insert(data, str(exc.args[0]))

        # Spliting Customers and Relationships to bulk INSERT
        cs_bulks = DataHandler.data_split(customers)
        cs_and_st_bulks = DataHandler.data_split(cs_and_stores)

        # INSERTing customers into Database
        for cs_bulk in cs_bulks:
            Customer.bulk_insert(cs_bulk)

        # INSERTing customers' relationships into Database
        for cs_and_st_bulk in cs_and_st_bulks:
            CustomerAndStore.bulk_insert(cs_and_st_bulk)
