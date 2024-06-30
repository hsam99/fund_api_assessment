import click
import mysql
from mysql.connector import errorcode


@click.command('create-schema')
@click.option('--user', required=True, help='MySQL username.')
@click.option('--password', required=True, help='MySQL password.')
@click.option('--host', default='127.0.0.1', help='MySQL host.')
@click.option('--port', default=3306, help='MySQL port.')
def main(user, password, host, port):
    """Create the `funds` table in `fund_db` database in MySQL server."""
    # Database connection configuration.
    config = {
        'user': user,
        'password': password,
        'host': host,
        'port': port,
        'raise_on_warnings': True
    }
    conn = None

    # Connect to the MySQL database server.
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        print("Successfully connected to the database.")

        # If the database already exists then the script will capture the error and exits.
        cursor.execute("CREATE DATABASE fund_db")
        cursor.execute("USE fund_db")

        # SQL command to create the table.
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS funds (
            id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            manager_name VARCHAR(255) NOT NULL,
            description TEXT,
            nav DOUBLE NOT NULL,
            date DATE NOT NULL,
            performance DOUBLE NOT NULL
        );
        """

        # Execute the SQL command to create the table
        cursor.execute(create_table_sql)
        print("Table 'funds' created successfully")

        # Commit the changes
        conn.commit()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        # Close the connection
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed")


if __name__ == '__main__':
    main()
    