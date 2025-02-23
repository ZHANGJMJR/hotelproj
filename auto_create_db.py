from mysql_database_manager import MySQLDatabaseManager

# 创建 MySQLDatabaseManager 实例，传入你的 MySQL 配置
db_manager = MySQLDatabaseManager(
    host="localhost",        # MySQL 主机
    user="root",             # MySQL 用户名
    password="123456" # MySQL 密码
)

# 执行数据库管理操作
db_manager.manage_database(sql_file_path="create_table.sql")
