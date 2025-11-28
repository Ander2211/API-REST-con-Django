try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception:
    # If PyMySQL isn't installed, mysqlclient may be used instead.
    pass
