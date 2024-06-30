"""Script to migrate data from JSON to MySQL."""
from datetime import datetime

import click
import mysql
from mysql.connector import errorcode

from funds_api.database import DATA_FILE, JsonDb


def _check_date_format(date_str, date_format='%Y-%m-%d'):
    """Checks a fund's date format."""
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def _validate_data(fund: dict):
    """Validates whether the data in the local database matches the MySQL schema."""
    columns = {'id', 'name', 'manager_name', 'description', 'nav', 'date', 'performance'}

    if not set(fund.keys()) == columns:
        raise ValueError(f'Fund data {fund} does not match the database columns')

    if not isinstance(fund['id'], int):
        raise ValueError(f'{fund} `id` must be int')

    if not isinstance(fund['name'], str) or len(fund['name']) > 255:
        raise ValueError(f'{fund} `name` must be string and no longer than 255 characters')

    if not isinstance(fund['manager_name'], str) or len(fund['manager_name']) > 255:
        raise ValueError(f'{fund} `manager_name` must be string and no longer than 255 characters')

    if not isinstance(fund['description'], str):
        raise ValueError(f'{fund} `description` must be string')

    if not isinstance(fund['nav'], (float, int)):
        raise ValueError(f'{fund} `nav` must be a number')

    if not isinstance(fund['date'], str) or not _check_date_format(fund['date']):
        raise ValueError(f'{fund} `date` must be a string and follow the format yyyy-mm-dd')

    if not isinstance(fund['performance'], (float, int)):
        raise ValueError(f'{fund} `performance` must be a number')


@click.command('migrate-database')
@click.option('--user', required=True, help='MySQL username.')
@click.option('--password', required=True, help='MySQL password.')
@click.option('--host', default='127.0.0.1', help='MySQL host.')
@click.option('--port', default=3306, help='MySQL port.')
def main(user, password, host, port):
    """Insert data from local database to MySQL server."""
    # Read local database data.
    local_database = JsonDb()
    local_database.connect(DATA_FILE)
    data = local_database.get_all()

    conn = None
    config = {
        'user': user,
        'password': password,
        'host': host,
        'port': port,
        'database': 'fund_db',
        'raise_on_warnings': True
    }
    insert_count = 0

    try:
        # Connects to MySQL server.
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        insert_sql = """
        INSERT INTO funds (id, name, manager_name, description, nav, date, performance)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        for fund in data:
            try:
                _validate_data(fund)
            except ValueError as exc:
                print(f'{exc}, entry not inserted')
                continue
            try:
                cursor.execute(insert_sql, (
                    fund['id'],
                    fund['name'],
                    fund['manager_name'],
                    fund['description'],
                    fund['nav'],
                    fund['date'],
                    fund['performance']
                ))
            except mysql.connector.errors.IntegrityError as exc:
                print(str(exc))
            else:
                insert_count += 1
        
        conn.commit()
        print(f"Inserted {insert_count} records.")
    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed")


if __name__ == "__main__":
    main()
