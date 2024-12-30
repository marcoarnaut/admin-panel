
class Employee:
    """Employee basic class"""

    # Class varibles

    employees = []
    emp_count = 0

    # Init employee

    def __init__(self, name: str, salary: int | float, age: int, skills: list) -> None:
        self.name: str = name
        self.salary: int | float = salary
        self.age: int = age
        self.skills: list = skills
        Employee.emp_count += 1

    # Get Info

    def count(self) -> int:
        return Employee.emp_count
    
    def get_info(self) -> dict:
        return {"Name" : self.name, "Salary" : self.salary, "Age" : self.age, "Skills" : self.skills}
    
    def __str__(self) -> str:
        return f"Name: {self.name} | Salary: {self.salary} | Age: {self.age} | Skills: {self.skills}"

    # Set info

    def set_salary(self, new_salary: int | float) -> None:
        self.salary: int | float = new_salary
        # Employee.print_info()

    def set_skills(self, new_skills: list) -> None:
        self.skills: list = new_skills
        # Employee.print_info()
    
    def set_age(self, new_age: int) -> None:
        self.age: int = new_age
        # Employee.print_info()

    # Del employee

    def remove(self) -> None:
        Employee.employees.remove(self)
        Employee.emp_count -= 1

    def reset() -> None:
        Employee.employees = []
        Employee.emp_count = 0
    
    # Add employee

    def add(name: str, salary: int | float, age: int, skills: list) -> None:
        for emp in Employee.employees:
            if emp.get_info()["Name"] == name:
                raise ValueError("Такое имя уже занято!")
        Employee.employees.append(Employee(name=name, salary=salary, age=age, skills=skills))

    # Create employee list
   
    def add_from(data) -> None:
        for user_info in data:
                for employee in range(len(Employee.employees)):
                    if user_info["Name"] == Employee.employees[employee].get_info()["Name"]:
                        return
                Employee.employees.append(Employee(name=user_info["Name"], salary=user_info["Salary"], age=user_info["Age"], skills=user_info["Skills"]))

def add_from(staff_list: list) -> None | str :
    """Добавление сотрудника используя список"""
    if isinstance(staff_list, list) and len(staff_list) > 0:
        for i in range(len(staff_list)):
            if (isinstance(staff_list[i], dict)) == False:
                return "Дан список неправильного формата, используйте: \n[{'Name':'','Salary':'','Age':'','Skills':''}, {'Name':'','Salary':'','Age':'','Skills':''}, {'Name':'','Salary':'','Age':'','Skills':''}]"
        try:
            Employee.add_from(staff_list) # Добавляем информацию о сотрудниках в таблицу
        except:
            Employee.add_from([])

def add_emp(name: str, salary: int | float, age: int, skills: list) -> None | str :
    """Добавление сотрудника вручную"""
    try:
        Employee.add(name, salary, age, skills) # Добавляем сотрудника
    except:
        return "Даны неподходящие аргументы!"
    
def info() -> None | str :
    """Вывод информации о сотрудниках в консоль"""
    try:
        print(f"Staff count: {Employee.count(Employee)}")
        if len(Employee.employees) > 0:
            for employee in range(len(Employee.employees)):
                print(f"{employee+1}. Name: {Employee.employees[employee].get_info()["Name"]}",
                    f"Salary: {Employee.employees[employee].get_info()["Salary"]}",
                    f"Age: {Employee.employees[employee].get_info()["Age"]}",
                    f"Skills: {str(Employee.employees[employee].get_info()["Skills"]).replace("[", "").replace("]", "")}",
                    sep=" | ")
    except:
        return "Произошла ошибка во время загрузки данных!"

def remove_emp(name: str) -> None | str :
    """Удаляет сотрудника по имени"""
    try:
        if len(Employee.employees) > 0:
            for employee in range(len(Employee.employees)):
                if Employee.employees[employee].get_info()["Name"] == name:
                    Employee.remove(Employee.employees[employee])
    except:
        return "Произошла ошибка во время удаления!"


def set(name: str, option: str = "Salary", new_value: int | list = None) -> None | str :
    """Изменяет зарплату/возраст/навыки сотрудника по имени"""
    try:
        if new_value != None:
            if len(Employee.employees) > 0:
                for employee in range(len(Employee.employees)):
                    if Employee.employees[employee].get_info()["Name"] == name:
                        match option:
                            case "Salary":
                                Employee.set_salary(Employee.employees[employee], new_value)
                            case "Age":
                                Employee.set_age(Employee.employees[employee], new_value)
                            case "Skills":
                                Employee.set_skills(Employee.employees[employee], new_value)
    except:
        return "Произошла ошибка!"

def get_list() -> None | list | str:
    """Возвращает форматированные данные о сотрудниках"""
    try:
        st_list = []
        if len(Employee.employees) > 0:
            for employee in range(len(Employee.employees)):
                st_list.append(Employee.employees[employee].get_info()) 
            return st_list
    except:
        return "Произошла ошибка во время попытки форматирования данных!"

def reset_list() -> None | str:
    """Удаляет всех сотрудников"""
    try:
        Employee.reset()
    except:
        return "Произошла ошибка во время удаления сотрудников"

def search_with(option: str, *args: str | int) -> list | str:
    """Поиск подходящих сотрудников по атрибутам"""
    try:
        if option == "Salary":
            if len(args) == 2 and type(args[0]) == str and type(args[1]) == int:
                if len(Employee.employees) > 0:
                    staff_with = []
                    for employee in range(len(Employee.employees)):
                        if args[0] == ">":
                            if Employee.employees[employee].get_info()["Salary"] > args[1]:
                                staff_with.append(Employee.employees[employee].get_info()["Name"])
                        if args[0] == "<":
                            if Employee.employees[employee].get_info()["Salary"] < args[1]:
                                staff_with.append(Employee.employees[employee].get_info()["Name"])
                        if args[0] == "==":
                            if Employee.employees[employee].get_info()["Salary"] == args[1]:
                                staff_with.append(Employee.employees[employee].get_info()["Name"])
                        if args[0] == "!=":
                            if Employee.employees[employee].get_info()["Salary"] != args[1]:
                                staff_with.append(Employee.employees[employee].get_info()["Name"])
                    return staff_with
                        
            else:
                return "Аргументы указаны неправильно!"
        elif option == "Age":
            if len(args) == 2 and type(args[0]) == str and type(args[1]) == int:
                if len(Employee.employees) > 0:
                    staff_with = []
                    for employee in range(len(Employee.employees)):
                        if args[0] == ">":
                            if Employee.employees[employee].get_info()["Age"] > args[1]:
                                staff_with.append(Employee.employees[employee].get_info()["Name"])
                        if args[0] == "<":
                            if Employee.employees[employee].get_info()["Age"] < args[1]:
                                staff_with.append(Employee.employees[employee].get_info()["Name"])
                        if args[0] == "==":
                            if Employee.employees[employee].get_info()["Age"] == args[1]:
                                staff_with.append(Employee.employees[employee].get_info()["Name"])
                        if args[0] == "!=":
                            if Employee.employees[employee].get_info()["Age"] != args[1]:
                                staff_with.append(Employee.employees[employee].get_info()["Name"])
                    return staff_with
            else:
                return "Аргументы указаны неправильно!"
        elif option == "Skills":
            if len(args) > 0:
                if len(Employee.employees) > 0:
                    staff_with = []
                    conditions = list(args)
                    for employee in range(len(Employee.employees)):
                        according = []
                        for condition in range(len(conditions)):
                            if conditions[condition] in Employee.employees[employee].get_info()["Skills"]:
                                according.append(True)
                            else:
                                according.append(False)
                        if False not in according:
                            staff_with.append(Employee.employees[employee].get_info()["Name"])
                    return staff_with
            else:
                return "Аргументы указаны неправильно!"
        elif option not in ["Salary","Age","Skills"]:
            return "Аргументы указаны неправильно!"
    except:
        return "Возникла ошибка с поиском подходящих сотрудников!"
    