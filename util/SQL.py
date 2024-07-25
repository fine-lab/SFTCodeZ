import sqlite3
import re
class SQLExecutor:
    def __init__(self, df, table_name):
        # 清理列名
        df = self.clean_column_names(df)
        # 创建数据库连接
        self.conn = sqlite3.connect('example.db')
        # 将清理后的 DataFrame 写入数据库
        df.to_sql(table_name, self.conn, if_exists='replace', index=False)
        # 初始化 SQL 字典
        self.agg_sql_dict = {0: "", 1: "AVG", 2: "MAX", 3: "MIN", 4: "COUNT", 5: "SUM"}
        self.op_sql_dict = {0: ">", 1: "<", 2: "=", 3: "!="}
        self.conn_sql_dict = {0: "", 1: "AND", 2: "OR"}
        # 保存清洗后的列名以用于构建 SQL 查询
        self.columns = list(df.columns)

    def clean_column_names(self, df):
        """Cleans special characters from DataFrame column names."""
        df.columns = [re.sub(r'[^\w\s]', '', col).replace(' ', '_') for col in df.columns]
        return df

    def build_query(self, table_name, query_params):
        # 解析选择的列和聚合函数
        select_clauses = []
        for sel, agg in zip(query_params['sel'], query_params['agg']):
            col_name = self.columns[sel]
            agg_func = self.agg_sql_dict[agg]
            select_clause = f"{agg_func}(`{col_name}`)" if agg_func else col_name
            select_clauses.append(f"{select_clause}")
        select_part = ", ".join(select_clauses)

        # 解析条件
        where_clauses = []
        for cond in query_params['conds']:
            col_name = self.columns[cond[0]]
            op = self.op_sql_dict[cond[1]]
            val = repr(cond[2])
            where_clause = f"`{col_name}` {op} {val}"
            where_clauses.append(where_clause)

        # 构建 SQL 的 WHERE 部分
        conn_op = self.conn_sql_dict[query_params['cond_conn_op']]
        where_part = f" {conn_op} ".join(where_clauses) if where_clauses else ""

        # 最终的 SQL 查询
        sql = f"SELECT {select_part} FROM {table_name} WHERE {where_part}"
        return sql

    def execute_query(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()