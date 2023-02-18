from fastapi import FastAPI
from database import db
import classes

app = FastAPI()
db2=db()


# PRINT TABLE INFORMATION IN GOOD FORM TO USER
def print_tables(col_names,col_values):
    if type(col_values)==str:
        print(col_values)
    else:
        print('-'*100)     
    for data in col_values:
        for count,col_name in enumerate(col_names):
            print(f"{col_name}: {data[count]}") 
        print('-'*100)

#get Emp informations who are working in department
def get_info_Did():
    while True:
        
        dep_id=input("please enter Department Number to exit press e: ").strip()
        if dep_id.lower()== 'e':       
            return False
        else:
            col_names,col_values=get_e_d_id(dep_id)
            if type(col_values)==str:
                print(col_values+' to exit press e')    
            else:
                print_tables(col_names,col_values) 
                print(f"You can wath the results also on web browser using this url: http://127.0.0.1:8000/emps/emp_d_id/{dep_id} ")   

@app.get("/emps/emp_d_id/{dep_id}")
def get_e_d_id(dep_id):
    if not dep_id.isdigit():
        col_names=""
        col_values="you enter not valid value you can enter only integer values"
        return col_names,col_values
    else:
    # Query search in the database 
        get_case=1
        col_names,col_values = db2.get_emp(dep_id,get_case)
        return col_names,col_values


#get Emp informations who owner this email
def get_info_Email():

    while True:
        email= input("Please enter the email you would like to know whose owner you can press E to exit : ").strip().lower()
        if email== 'e':
            return False
        else:
            col_names,col_values=get_e_email(email)
            if type(col_values)==str:
                print(col_values+' to exit press e')    
            else:
                print_tables(col_names,col_values)                
                print(f"You can wath the results also on web browser using this url: http://127.0.0.1:8000/emps/emp_email/{email} ")   
        
@app.get("/emps/emp_email/{email}")
def get_e_email(email:str):
    result=classes.CHECK.check_email(email)
    if result == None:
       col_names= ""
       col_values=("please enter a valid email address")
       return col_names,col_values
 
    else:
        get_case=2
        col_names,col_values = db2.get_emp(email,get_case)
        return col_names,col_values

#get Employee table informations
@app.get("/emps/emp_table")
def get_info_emp():
    get_case=3
    table='emp1'
    col_names,col_values = db2.get_emp(table,get_case)
    if type(col_values)==str:
        print(col_values)   
        print(f"You can see the results also on web browser using this url: http://127.0.0.1:8000/emps/emp_table") 
        return col_values
    else:
        print_tables(col_names,col_values)   
        print(f"You can see the results also on web browser using this url: http://127.0.0.1:8000/emps/emp_table")
        return col_names,col_values

#get Department table informations
@app.get("/emps/dep_table")
def get_info_dep():
    get_case=3
    table='dep1'
    col_names,col_values = db2.get_emp(table,get_case)
    if type(col_values)==str:
        print(col_values)   
        print(f"You can see the results also on web browser using this url: http://127.0.0.1:8000/emps/dep_table") 
        return col_values
    else:
        print_tables(col_names,col_values)   
        print(f"You can see the results also on web browser using this url: http://127.0.0.1:8000/emps/dep_table")
        return col_names,col_values

# Add new Department in Department table
def insert_dep():
    while True:
        dep_name=input(" Please enter new depatment name to add To Exit press e: ").strip().lower()
        if dep_name.lower()== 'e':
            return False 
        result=add_dep(dep_name)
        if result=="Dep is exist":
             print("You can't enter Department is exist in database : ")
           
        elif result=='You entered a special char':
             print("You can't enter spaces between words or write special character you can use '_' only: ")   
        else:
              print("Your Department is added :")   
              print(f"You can add department also on thunder client using POST and this url: http://127.0.0.1:8000/emps/add/dep_table/{dep_name} ")

@app.post("/emps/add/dep_table/{dep_name}")
def add_dep(dep_name):
    dep_name= dep_name.strip().lower()
    dep_name=classes.CHECK.check_special_char(dep_name)
    if (dep_name)!= False: 
        table='dep1'
        value=db2.add_dep(dep_name,table)
        return value
    else:
        return 'You entered a special char'    

# Add new Employee in Employee table
def insert_emp():
    emp=classes.Employee()
    while True:    
        while True:
            emp.FIRST_NAME=input(" Please enter new employee First Name consists of only alphabet characters to add To Exit press e: ").strip().lower()
            if classes.CHECK.check_alpha(emp.FIRST_NAME)== 'exit':
                 return False
            if classes.CHECK.check_alpha(emp.FIRST_NAME):
                 break
        while True:    
            emp.LAST_NAME=input(" Please enter new employee Last Name consists of only alphabet characters to add To Exit press e: ").strip().lower()
            if classes.CHECK.check_alpha(emp.LAST_NAME)== 'exit':
                 return False
            if classes.CHECK.check_alpha(emp.LAST_NAME):
                 break
        while True:        
            emp.AGE=input(" Please enter new employee Age consists of only Integer Number to add To Exit press e: ").strip().lower()
            if classes.CHECK.check_int(emp.AGE)== 'exit':
               return False
            if classes.CHECK.check_int(emp.AGE):
                emp.AGE=int(emp.AGE)
                if  emp.AGE>17 and emp.AGE<66:
                    break
                else:
                     print("please enter suatiable Age between 18 and 65")
        while True:    
            emp.SALARY=input(" Please enter new employee Salary consists of only Integer Number to add To Exit press e: ").strip().lower()
            if classes.CHECK.check_int(emp.SALARY)== 'exit':
               return False
            if classes.CHECK.check_int(emp.SALARY):
                break  
        while True:
            emp.EMAIL=input(" Please enter new employee Email to add To Exit press e: ").strip().lower()
            emp.EMAIL=classes.CHECK.check_email(emp.EMAIL)
            if emp.EMAIL== 'exit':
               return False
            elif emp.EMAIL != None:
                break
        while True:    
            emp.DEPARTMENT_ID=input(" Please enter new employee Department ID consists of only Integer Number to add To Exit press e: ").strip().lower()
            if classes.CHECK.check_int(emp.DEPARTMENT_ID)== 'exit':
               return False
            if classes.CHECK.check_int(emp.DEPARTMENT_ID):
                break
            
        result=add_emp(emp)        
        if result=="EMP is exist":
             print("You can't enter EMPLOYEE is exist in database : ")
           
        elif result== f"YOU CAN'T ADD PERSON TO DEPARTMENT NOT EXIST":
             print("You can't add Employee to Department not exists: ")   
        else:
              print("Your Employee is added :")   
              print(f"You can see the results also on thunder client using POST and this url: http://127.0.0.1:8000/emps/add/emp_table/ ")

# Exammple to write in json
# {
# "FIRST_NAME": " ",
# "LAST_NAME": " ",
# "AGE": ,
# "SALARY": ,
# "EMAIL": " ",
# "DEPARTMENT_ID": 
# }

@app.post("/emps/add/emp_table/")
def add_emp(emp:classes.Employee):
        if not emp.FIRST_NAME  or not emp.LAST_NAME or not emp.AGE or not emp.SALARY or not emp.EMAIL or not emp.DEPARTMENT_ID  :
            return("your variables only FIRST_NAME,LAST_NAME,AGE,SALARY,EMAIL,DEPARTMENT_ID")
        emp.FIRST_NAME=emp.FIRST_NAME.strip().lower()
        emp.LAST_NAME=emp.LAST_NAME.strip().lower()
        emp.EMAIL=emp.EMAIL.strip().lower()
        if not classes.CHECK.check_alpha(emp.FIRST_NAME):
            return {"FIRST_NAME contain only alpha"}
        if not classes.CHECK.check_alpha(emp.LAST_NAME):
            return {"LAST_NAME contain only alpha"}
        if  emp.AGE<18 or emp.AGE>65 :
            return {"AGE contain only int and age between 18 to 65"}
        if not classes.CHECK.check_email(emp.EMAIL):
            return {"Email contain only email form"}      
        
        table='emp1'
        value=db2.add_emp(emp,table)
        return value
    

#update salary to all employees between 2 salraies
def update_emp():
    salary=classes.Salary()
    while True:
        salary.PERCENTAGE=input("please enter percentage Number to add to all Employee salaries to exit press e: ").strip().lower()
        if classes.CHECK.check_float(salary.PERCENTAGE)== 'exit':
            return False
        if classes.CHECK.check_float(salary.PERCENTAGE):
            salary.PERCENTAGE=float(salary.PERCENTAGE)
            break
    while True:
        salary.MIN_SALARY=input("Please enter the minimum Salary you would like to add a new percentage to . to exit press e: ").strip().lower()
        if classes.CHECK.check_int(salary.MIN_SALARY)== 'exit':
            return False
        if classes.CHECK.check_int(salary.MIN_SALARY):
            salary.MIN_SALARY=int(salary.MIN_SALARY)
            break
    while True:
        salary.MAX_SALARY=input("Please enter the Max Salary you would like to add a new percentage to . to exit press e: ").strip().lower()
        if classes.CHECK.check_int(salary.MAX_SALARY)== 'exit':
            return False
        if classes.CHECK.check_int(salary.MAX_SALARY):
            salary.MAX_SALARY=int(salary.MAX_SALARY)
            if salary.MAX_SALARY >= salary.MIN_SALARY:
                break 
            else:
                print("MAX SALARY SHOULD EQUAL OR MORE THAN MIN SALARY")
                

    col_values=update_salary(salary)
    print(f"{col_values} You can see the results on thunder using put using this url: http://127.0.0.1:8000/emps/update/emp_percentage/")

# update example
# {
#    "PERCENTAGE":5 ,
#     "MIN_SALARY": 5,
#     "MAX_SALARY": 5
# }

@app.put("/emps/update/emp_percentage/")
def update_salary(salary:classes.Salary):

    if not salary.PERCENTAGE or not salary.MIN_SALARY or not salary.MAX_SALARY:
        return("your variables only PERCENTAGE,MIN_SALARY,MAX_SALARY")
    if salary.MIN_SALARY > salary.MAX_SALARY:
        return {"max salary should equal or greater than min salary "}
    else:
         col_values = db2.update_emp(salary)
         return col_values  
                
# delete employee we have name,last_name and email
def delete_emp():
    emp=classes.Employee()
    while True:
        emp.FIRST_NAME=input(" Please enter employee First Name you want delete To Exit press e: ").strip().lower()
        if classes.CHECK.check_alpha(emp.FIRST_NAME)== 'exit':
                 return False
        if classes.CHECK.check_alpha(emp.FIRST_NAME):
                 break 
    while True:
        emp.LAST_NAME=input(" Please enter employee Last Name you want delete To Exit press e: ").strip().lower()
        if classes.CHECK.check_alpha(emp.LAST_NAME)== 'exit':
                 return False
        if classes.CHECK.check_alpha(emp.LAST_NAME):
                 break 
    while True:
            emp.EMAIL=input(" Please enter new employee Email to add To Exit press e: ").strip().lower()
            emp.EMAIL=classes.CHECK.check_email(emp.EMAIL)
            if emp.EMAIL== 'exit':
               return False
            elif emp.EMAIL != None:
                break    
        
    result=del_emp(emp)

    print(f"{result} You can DELETE on thunder using delete using this url: http://127.0.0.1:8000/emps/delete/emp_table/")
   
            
# Exammple to DELETE 
# {
# "FIRST_NAME": " ",
# "LAST_NAME": " ",
# "EMAIL": " "
# }

@app.delete("/emps/delete/emp_table/")
def del_emp(emp:classes.Employee):
    if not emp.FIRST_NAME or not emp.LAST_NAME or not emp.EMAIL:
        return("your variables only FIRST_NAME,LAST_NAME,EMAIL")
    emp.FIRST_NAME=emp.FIRST_NAME.strip().lower()
    emp.LAST_NAME=emp.LAST_NAME.strip().lower()
    emp.EMAIL=emp.EMAIL.strip().lower()
    if not classes.CHECK.check_alpha(emp.FIRST_NAME):
        return {"FIRST_NAME contain only alpha"}
    if not classes.CHECK.check_alpha(emp.LAST_NAME):
        return {"LAST_NAME contain only alpha"}
    if not classes.CHECK.check_email(emp.EMAIL):
        return {"Email contain only email form"}
     
    table='emp1'
    value=db2.del_emp(emp,table)
    return value
    



