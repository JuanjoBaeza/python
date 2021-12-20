def employee_details(ID):
    switcher = {
        "1004": "Employee Name: MD. Mehrab",
        "1009": "Employee Name: Mita Rahman",  
        "1010": "Employee Name: Sakib Al Hasan",
    }
    return switcher.get(ID, "nothing")

ID = input("Enter the employee ID: ")

print(employee_details(ID))