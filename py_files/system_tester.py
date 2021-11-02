from DB import DB


class SystemTester:

    querys = {
        'Customers_count': 'SELECT COUNT(cpf) FROM Customers;',
        'Stores_count': 'SELECT COUNT(cnpj) FROM Stores;',
        'Customers_Stores_relationships_count': 'SELECT COUNT(relationship_id) FROM customers_and_stores;',
        'Errors_count': 'SELECT COUNT(customer_errors_id) FROM customers_errors;'
    }

    @staticmethod
    def count_test():
        db = DB()
        cs_count = db.execute_query(SystemTester.querys['Customers_count'], fetch=True)
        st_count = db.execute_query(SystemTester.querys['Stores_count'], fetch=True)
        csst_count = db.execute_query(SystemTester.querys['Customers_Stores_relationships_count'], fetch=True)
        err_count = db.execute_query(SystemTester.querys['Errors_count'], fetch=True)

        print('Test results:')
        print(f'\tCustomers created: {cs_count[0][0]}')
        print(f'\tStores created: {st_count[0][0]}')
        print(f'\tCustomers and Stores relationships created: {csst_count[0][0]}')
        print(f'\tErrors created: {err_count[0][0]}')
