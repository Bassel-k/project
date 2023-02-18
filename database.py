import sqlite3
import pandas as pd
import classes
class db:
  

    def __call_db(self, query):
        self.conn = sqlite3.connect("emp.db")
        self.cur = self.conn.cursor()
        res = self.cur.execute(query)
        data = res.fetchall()
        self.cur.close()
        self.conn.commit()
        self.conn.close()
        return data
    
    def get_emp(self,case,case_id:int):
        # find table column name to print them with data
        if case== 'dep1':
            emps1=self.__call_db(f"PRAGMA table_info('{case}')")
            col_names = [row[1] for row in emps1]
        else:
            emps1=self.__call_db(f"PRAGMA table_info('emp1')")
            col_names = [row[1] for row in emps1]
        # find all employees work in this department
        if case_id==1:
            query= f"SELECT * FROM emp1 WHERE DEPARTMENT_ID = '{case}'"
            col_values=self.__call_db(query)
            if len(col_values)== 0:
                 col_values =(f"your department id {case} is not found")
                 return 'You can try with another value',col_values
            else:
                 return col_names,col_values
        # find employee have this email
        if case_id==2:
            query= f"SELECT * FROM emp1 WHERE EMAIL = '{case}'"
            col_values=self.__call_db(query)
            if len(col_values)== 0:
                 col_values =(f"your Email {case} is not found")
                 return 'You can try with another value',col_values
            else:
                 return col_names,col_values
        # return all information about this table
        elif case_id==3:
            query= f"SELECT * FROM {case}"
            col_values=self.__call_db(query)
            if len(col_values)== 0:
                 col_values =(f"your table {case} is empty to exit press e")
                 return col_names,col_values
            else:
                 return col_names,col_values
    # add new department first search if department  not exist add to db else return you can't add 
    def add_dep(self,dep_name,table):
        query=f"SELECT '{dep_name}' FROM '{table}' WHERE DEPARTMENT_NAME='{dep_name}'"
        result=self.__call_db(query)
        if len(result)== 0:
            query1=f"INSERT INTO '{table}'(DEPARTMENT_NAME) VALUES('{dep_name}')"    
            self.__call_db(query1)
            return 'Add success'    
        else:
            return 'Dep is exist'
    # add new employee first search if employee is not exist and department id in department table add to db else return you can't add 
    def add_emp(self,emp:classes.Employee,table):
        
        query=f'''SELECT 'FIRST_NAME','LAST_NAME','EMAIL' FROM '{table}'
                 WHERE FIRST_NAME='{emp.FIRST_NAME}' AND LAST_NAME='{emp.LAST_NAME}' AND
                        EMAIL='{emp.EMAIL}'
                    '''
        result=self.__call_db(query)
        query1=f'''SELECT 'DEPARTMENT_ID' FROM dep1
                 WHERE DEPARTMENT_ID='{emp.DEPARTMENT_ID}'
                    '''
        result1=self.__call_db(query1)
        if len(result1)==0:
            return f"YOU CAN'T ADD PERSON TO DEPARTMENT NOT EXIST"

        if len(result)== 0:
            query2=f'''INSERT INTO '{table}'(FIRST_NAME,LAST_NAME,AGE,SALARY,EMAIL,DEPARTMENT_id) 
            VALUES('{emp.FIRST_NAME}','{emp.LAST_NAME}','{emp.AGE}','{emp.SALARY}','{emp.EMAIL}','{emp.DEPARTMENT_ID}') 
            '''
            self.__call_db(query2)
            return 'Add success'    
        else:
            return 'EMP is exist'
    # update salary to all employess between 2 salaries    
    def update_emp(self,salary:classes.Salary):
        query=f"UPDATE emp1 SET SALARY = ROUND(SALARY+(SALARY*{salary.PERCENTAGE}/100)) WHERE SALARY BETWEEN {salary.MIN_SALARY} AND {salary.MAX_SALARY}"
        result=self.__call_db(query)
        if not self.cur.rowcount>0:
            return F"{self.cur.rowcount} values updated"
        else:
            return F"{self.cur.rowcount} values updated "
    #delete employee from db if the employee exist
    def del_emp(self,emp:classes.Employee,table):
        query=f'''SELECT 'FIRST_NAME','LAST_NAME','EMAIL' FROM '{table}'
                WHERE FIRST_NAME='{emp.FIRST_NAME}' AND LAST_NAME='{emp.LAST_NAME}' AND
                    EMAIL='{emp.EMAIL}'
                '''
        result=self.__call_db(query)
        
        if len(result)> 0:
            query1=f''' DELETE FROM '{table}' WHERE FIRST_NAME='{emp.FIRST_NAME}' AND LAST_NAME='{emp.LAST_NAME}' AND
                    EMAIL='{emp.EMAIL}'
                    '''   
            self.__call_db(query1)
            return 'DELETE SUCCESS'    
        else:
            return 'PERSON IS NOT EXIST TO DELETE'

    # create the database and import data from xlsx file to the table
    def create_database(self):
        self.conn = sqlite3.connect("emp.db")
        # read the Excel file
        df = pd.read_excel("Emp.xlsx",sheet_name='Sheet1')
        df1 = pd.read_excel("Emp.xlsx",sheet_name='Sheet2')
        
        table1 = ['ID','FIRST_NAME', 'LAST_NAME', 'AGE', 'SALARY','EMAIL','DEPARTMENT_ID']
        df_table1 = df[table1]
        table2 = ['DEPARTMENT_ID', 'DEPARTMENT_NAME']
        df_table2 = df1[table2]
        
        # insert the data into tables
        df_table1.to_sql("emp2",self.conn, if_exists="replace", index=False)
        df_table2.to_sql("dep2",self.conn, if_exists="replace", index=False)  
        self.conn.commit()
        self.conn.close()

        query="""CREATE TABLE IF NOT EXISTS dep1 (
                            DEPARTMENT_ID INTEGER PRIMARY KEY,
                            DEPARTMENT_NAME TEXT )
                           """
        self.__call_db(query)
        query="INSERT INTO dep1 SELECT * FROM dep2;"
        self.__call_db(query)
        query="DROP TABLE dep2;"
        self.__call_db(query)
        query="""CREATE TABLE IF NOT EXISTS emp1 (
                            ID INTEGER PRIMARY KEY,
                            FIRST_NAME TEXT,
                            LAST_NAME TEXT,
                            AGE INTEGER,
                            SALARY INTEGER,
                            EMAIL TEXT,
                            DEPARTMENT_ID INTEGER,
                            CONSTRAINT fk_dep1
                            FOREIGN KEY (DEPARTMENT_ID)
                            REFERENCES dep1(DEPARTMENT_ID)
                            ON DELETE CASCADE )                             
                             """
        self.__call_db(query)              
        query="INSERT INTO emp1 SELECT * FROM emp2;"
        self.__call_db(query)
        query="DROP TABLE emp2;"
        self.__call_db(query)

    #check user_name and password     
    def users(user_name,password):
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        res = cur.execute(f"select * from users where USER_NAME='{user_name}' AND PASSWORD='{password}'")
        data = res.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        if len(data)>0:
            return True
        else:
            return False    

    
     