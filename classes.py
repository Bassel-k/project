from pydantic import BaseModel
import re

class Employee(BaseModel):
     
    FIRST_NAME :str  =None                    
    LAST_NAME :str =None
    AGE :int  =None
    SALARY :int =None
    EMAIL :str =None
    DEPARTMENT_ID :int =None

class Salary(BaseModel):
    PERCENTAGE: float =None 
    MIN_SALARY: int =None 
    MAX_SALARY:int =None 




class CHECK():

    def check_alpha(value):
        if value.lower() =='e':
            return 'exit'
        if value.isalpha():
            return True


    def check_int(value):
        if value =='e':
            return 'exit'
        if value.isdigit():
            return True
    
   


    def check_float(value):
        try:
            value=float(value)
            if value > 0:
                return True
        except ValueError:    
            return False
    
    def check_email(value):
    #results from findall if email have same formal search have list of email content else return empty list
        if value =='e':
            return 'exit'
        search=re.findall(r"^[A-Za-z0-9\.\-\_]+@[A-Za-z0-9]+\.[A-Za-z]{2,6}$",value)
        if search ==[]:
            return None
        else:
            return value
# To search in every char if there is non alpha or num or '_' return false if true return words
    def check_special_char(words):
        valid = True
        for char in words:
            if not char.isalnum() and char !='_':
                valid = False
                break
        if valid == True:
            
            return words 
        else:
            return False 
        


