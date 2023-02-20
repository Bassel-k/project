def users(username,password):
        from database import db
        
        data= db.users(user_name,password)
        if data is True:
         main()
        else:
         print("your user name or password is not correct")     



def main():

    from database import db
    import os
    import api
    print("Welcome to our app")
    print("-"*100)
            



    while True:
        conn = (input("Do you want to initialize the database first to work with our app?(Y/N)" )).upper()

        if conn == "Y":
            
            #check if a file is exist
            if os.path.isfile("emp.db"):
                print("-" * 100)
                print("The database has already been initialized")
            else:
                #create the instance and call create database method
                ci= db()
                ci.create_database()
            
            while True:
                print("-" * 100)
                print("Please select one of the available options.")
                i=1
                option={1: "Select employees information for those who work in department.",
                        2: "Select employee information for the person with this email.",
                        3: "Select employees information.",
                        4: "Select departments information.",
                        5: "Add new department.",
                        6: "Add new employee.",
                        7: "Update employees salary.",
                        8: "Delete employee you have name,last_name and email.",
                        9: "exit."}
                
                for nu,massage in option.items():
                    print(f"{nu}.  {massage}")
                choice =(input("Enter the number of your choice: "))
                if choice in ["1","2","3","4","5","6","7","8","9"]:  
                    choice =int(choice)   
                
                match (choice):
                    case 1:
                        api.get_info_Did()
                    case 2:
                        api.get_info_Email()              
                    case 3:
                        api.get_info_emp()              
                    case 4:
                        api.get_info_dep()
                    case 5:
                        api.insert_dep()
                    case 6:
                        api.insert_emp()
                    case 7:
                        api.update_emp()
                    case 8:
                        api.delete_emp()
                    case 9:
                        exit()    
                    case _:
                        print("Please enter a valid choice")
            
        elif conn != 'E':
            print(F"Invalid choice, please try again, to exit press E.")
        else:
            exit()
if __name__ == "__main__":
    
    user_name=input("PLEASE ENTER YOUR USER NAME: ")
    password=input("PLEASE ENTER YOUR PASSWORD: ")
    users(user_name,password)
