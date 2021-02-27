#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
import _sqlite3


def search_in_database(search_key, column_name, table_name, database_name="userdata.db"):
    """
    :param search_key: anything
    :parameter objectName: user_defined_object
    :parameter searchkey: Any
    :parameter database_name: string
    :parameter table_name: string
    :parameter column_name: String
    :return result: list
    """
    connection = _sqlite3.connect(database_name)
    temp = connection.execute(f"SELECT * FROM {table_name} WHERE {column_name} = '{str(search_key)}'").fetchall()
    connection.close()
    if len(temp) != 0:
        return temp
    else:
        return ["NF"]  # NF stands for not founded.


def insert_into_database(values, table_name, database_name="userdata.db"):
    """
    :param values: list
    :param table_name:
    :param database_name:
    :return:
    """
    connection = _sqlite3.connect(database_name)
    connection.execute(f"INSERT INTO {table_name} VALUES ({str(values)[1:-1]})")
    connection.commit()

    # Close the connection.
    connection.close()


if __name__ == "__main__":
    insert_into_database([2, "exist", "random"], "Login")
