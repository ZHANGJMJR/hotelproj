import mysql.connector
from datetime import datetime
from mysql.connector import Error


class MySQLDatabaseManager:
    def __init__(self, host, user, password,port=3306):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def connect_to_mysql(self):
        """建立与 MySQL 数据库的连接"""
        try:
            return mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database="mysql"  # 连接到 MySQL 系统数据库
            )
        except Error as e:
            print(f"Error: {e}")
            return None

    def database_exists(self, cursor, database_name):
        """检查数据库是否存在"""
        cursor.execute(f"SHOW DATABASES LIKE '{database_name}';")
        result = cursor.fetchone()
        return result is not None

    def create_database(self, cursor, database_name):
        """创建新数据库，并指定字符集和排序规则"""
        try:
            create_db_query = f"""
            CREATE DATABASE `{database_name}` 
            CHARACTER SET utf8 
            COLLATE utf8_general_ci;
            """
            cursor.execute(create_db_query)
            print(f"数据库 `{database_name}` 已创建。")
        except Error as e:
            print(f"Error: {e}")

    def execute_sql_from_file(self, cursor, file_path):
        """从 SQL 文件中读取并执行 SQL 语句"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                sql = file.read()
                # 分割多条 SQL 语句并逐个执行
                for statement in sql.split(';'):
                    statement = statement.strip()
                    if statement:
                        cursor.execute(statement)
                print(f"从文件 `{file_path}` 执行 SQL 成功。")
        except Error as e:
            print(f"Error: {e}")
        except FileNotFoundError:
            print(f"文件 `{file_path}` 未找到。")

    def manage_database(self, sql_file_path):
        """主方法：检查数据库是否存在，如果不存在则创建"""
        # 获取当前日期作为数据库名称
        date_str = datetime.now().strftime("hotel_%Y%m%d")  # 格式：YYYY_MM_DD

        # 连接到 MySQL
        conn = self.connect_to_mysql()
        if conn is None:
            return

        cursor = conn.cursor()

        # 检查数据库是否已存在
        if self.database_exists(cursor, date_str):
            print(f"数据库 `{date_str}` 已存在。")
            cursor.close()
            conn.close()  # 关闭连接并跳过后续操作
            return  # 数据库存在时，直接退出函数，跳过后续创建

        # 如果数据库不存在，继续执行创建数据库和表操作
        self.create_database(cursor, date_str)

        # 使用新创建的数据库（或已经存在的数据库）
        cursor.execute(f"USE `{date_str}`;")

        # 从文件中执行 SQL 创建表
        self.execute_sql_from_file(cursor, sql_file_path)

        # 提交并关闭连接
        conn.commit()
        cursor.close()
        conn.close()
        print("操作完成，数据库和表处理成功。")
