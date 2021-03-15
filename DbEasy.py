#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
import _sqlite3


def search_in_database(search_key, column_name, table_name, cell_name="*", database_name="userdata.db"):
    """
    :param search_key: anything
    :param column_name: str
    :param table_name: str
    :param cell_name: str
    :param database_name: str
    :return: tuple(list)
    """
    connection = _sqlite3.connect(database_name)
    temp = connection.execute(f"SELECT {cell_name} FROM {table_name} WHERE "
                              f"{column_name} = '{str(search_key)}'").fetchall()
    connection.close()
    if len(temp) != 0:
        return temp
    else:
        return None  # NF stands for not founded.


def insert_into_database(values, table_name, database_name="userdata.db"):
    """
    :param values: list
    :param table_name:
    :param database_name:
    :return:
    """
    connection = _sqlite3.connect(database_name)
    command = f"INSERT INTO {table_name} VALUES ("
    for value in values:
        if value is None:
            command += "NULL"
        elif isinstance(value, str):
            command += f"'{value}'"
        else:
            command += str(value)
        command += ", "
    command = command[0:-2] + ")"
    connection.execute(command)
    connection.commit()

    # Close the connection.
    connection.close()


def update_existing_in_database(key, key_column, values, columns, table_name, database_name="userdata.db"):
    """
    :param key:
    :param key_column:
    :param values: list
    :param columns: list
    :param table_name:
    :param database_name:
    :return:
    """
    length = len(values)
    if length == len(columns) and length != 0:
        connection = _sqlite3.connect(database_name)
        temp = f"UPDATE  {table_name} SET "
        for i in range(length):
            if isinstance(values[i], str):
                if i == length - 1:
                    if isinstance(key, str):
                        temp += f"{columns[i]} = '{values[i]}' WHERE {key_column} = '{key}';"
                    else:
                        temp += f"{columns[i]} = '{values[i]}' WHERE {key_column} = {key};"
                else:
                    temp += f"{columns[i]} = '{values[i]}', "
            elif values[i] is None:
                if i == length - 1:
                    if isinstance(key, str):
                        temp += f"{columns[i]} = NULL WHERE {key_column} = '{key}';"
                    else:
                        temp += f"{columns[i]} = NULL WHERE {key_column} = {key};"
                else:
                    temp += f"{columns[i]} = NULL, "
            else:
                if i == length - 1:
                    if isinstance(key, str):
                        temp += f"{columns[i]} = {values[i]} WHERE {key_column} = '{key}';"
                    else:
                        temp += f"{columns[i]} = {values[i]} WHERE {key_column} = {key};"
                else:
                    temp += f"{columns[i]} = {values[i]}, "
        cur = connection.cursor()
        cur.execute(temp)
        connection.commit()

        # Close the connection.
        cur.close()
        connection.close()
        return True

    else:
        return False


def delete_records_in_database(primary_key, key_column, table_name, database_name="userdata.db"):
    """
    :param primary_key: int
    :param key_column:
    :param table_name:
    :param database_name:
    :return: None
    """
    connection = _sqlite3.connect(database_name)
    temp = f"DELETE FROM {table_name} WHERE {key_column} = {primary_key}"
    connection.execute(temp)
    connection.commit()
    connection.close()
    return None


if __name__ == "__main__":
    print(search_in_database("1", "UserName", "UserInformation"))
