from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
from methods import Employee
from methods import add_from, add_emp, info, remove_emp, set, get_list, reset_list, search_with
import json
import os
from collections import Counter


mainpath = "\\".join((os.path.abspath(sys.argv[0])).split("\\")[:-1])

if not os.path.isdir("saves"):
    os.mkdir("saves")

datapath = os.getcwd()

def load_data(file_name: str) -> list | None:
    try:
        file_name = f"{datapath}/saves/{file_name}"
        with open(file_name, "r") as f:
            if file_name.split(".")[1] == "json":
                data = json.load(f)
                return data
            elif file_name.split(".")[1] == "txt":
                data = f.read()
                return eval(data)
    except Exception as e:
        warn = QMessageBox()
        warn.setWindowTitle("Warning")
        warn.setText(f"Unknown error with loading data occured, please set valid file name! (Open file again)\nException:\n{e}")
        warn.setIcon(QMessageBox.Warning)
        warn.exec_()

def save_data(file_name: str, st_list: list) -> None:
    try:
        file_name = f"{datapath}/saves/{file_name}"
        with open(file_name, "w") as f:
            # json.dumps(get_list())
            if file_name.split(".")[1] == "json":
                json.dump(st_list, f)
            elif file_name.split(".")[1] == "txt":
                f.write(str(st_list))
    except Exception as e:
        warn = QMessageBox()
        warn.setWindowTitle("Warning")
        warn.setText(f"Unknown error with saving data occured, please set valid file name! (Save file again)\nException:\n{e}")
        warn.setIcon(QMessageBox.Warning)
        warn.exec_()
        
def addToClipBoard(string: str) -> None:
    """Copy to clipboard with OS"""
    command = 'echo ' + string.strip() + '| clip'
    os.system(command)

def counterSubset(list1, list2):
        c1, c2 = Counter(list1), Counter(list2)
        for k, n in c1.items():
            if n > c2[k]:
                return False
        return True
 

class UI(QMainWindow):

    # Class varibles

    file = ""
    formats = [".json", ".txt"]
    int_operations = [">", "<", "==", "!=", ">=", "<="]
    MainListRow_ID = -1
    MainListRow_CONTENT = ""
    SearchListRow_ID = -1
    SearchListRow_CONTENT = ""
    SearchResults = []
    skill_names = ["Python", "Kotlin", "Ruby", "Erlang", "PHP", "Objective-C", "TypeScript", "Java", "C++", "Scala", "NodeJS", "Lua", "Fortran", "JS", "Swift", "Bash", "Rust", "C#", "SQL", "GO"]

    # Init UI

    def __init__(self):
        super(UI, self).__init__()

        # Load template
        uic.loadUi(f"{mainpath}/main.ui", self)

        # Window settings
        self.setWindowTitle("Admin Panel")
        self.setFixedSize(720, 700)
        
        # ListWidget Events
        self.listWidget.currentRowChanged.connect(self.MainListSelectionChanged)
        self.listWidget_2.currentRowChanged.connect(self.SearchListSelectionChanged)

        # menubar "file"
        self.actionSave.triggered.connect(self.save)
        self.actionSave_and_Exit.triggered.connect(self.savenexit)
        self.actionOpen.triggered.connect(self.load)
        self.actionExit_File.triggered.connect(self.exit_file)
        self.actionExit.triggered.connect(self.exit)
        self.actionSave_as.triggered.connect(self.save_filename_form)

        # menubar "Select"
        self.actionCopy_to_Clipboard.triggered.connect(self.copy)
        self.actionAdd.triggered.connect(self.add_employee_form)
        self.actionRemove.triggered.connect(self.remove_by_index)
        self.actionSet_Salary.triggered.connect(self.set_salary_form)
        self.actionSet_Age.triggered.connect(self.set_age_form)
        self.actionSet_Skills.triggered.connect(self.set_skills_form)

        # menubar "Search"
        self.actionWith_Salary.triggered.connect(self.find_with_salary_form)
        self.actionWith_Age.triggered.connect(self.find_with_age_form)
        self.actionWith_Skills.triggered.connect(self.find_with_skills_form)
        self.actionWith_Name.triggered.connect(self.find_with_name_form)

        # menubar "View"
        self.actionSort_by_Name.triggered.connect(self.sortbyname)
        self.actionSort_by_Salary.triggered.connect(self.sortbysalary)
        self.actionSort_by_Age.triggered.connect(self.sortbyage)
        self.actionSort_by_Skills.triggered.connect(self.sortbyskills)
        self.actionreverse.triggered.connect(self.reverselist)

        # css
        self.setStyleSheet("""
            QListWidget{
                background:#ffffff
            }
            QListWidget::hover{
                background: #d1d1d1
            }
        """)

    # Name
    def sortbyname(self: object) -> None:
        """Sorts list by alphabet"""
    
    # Salary
    def sortbysalary(self: object) -> None:
        """Sorts list by salary"""
        Employee.employees = sorted(Employee.employees, key=lambda x: x.salary)
        self.reload()
        
    # Age
    def sortbyage(self: object) -> None:
        """Sorts list by age"""
        Employee.employees = sorted(Employee.employees, key=lambda x: x.age)
        self.reload()
        
    # Count of skills
    def sortbyskills(self: object) -> None:
        """Sort list by count of skills"""
        Employee.employees = sorted(Employee.employees, key=lambda x: len(x.skills))
        self.reload()
    
    # reverse
    def reverselist(self: object) -> None:
        """Reverses employee sheet"""
        Employee.employees = list(reversed(Employee.employees))
        self.reload()

    # with salary
    def find_with_salary_form(self: object) -> None:
        """Shows search with salary form"""
        self.withsalary = QDialog()
        self.withsalary.setWindowTitle("With Salary")
        self.withsalary.setFixedSize(200, 100)
        self.withsalary.textbox = QLineEdit(self.withsalary)
        self.withsalary.textbox.move(75, 35)
        self.withsalary.textbox.resize(100, 30)
        self.withsalary.label = QLabel(self.withsalary)
        self.withsalary.label.move(50, 0)
        self.withsalary.label.resize(100, 30)
        self.withsalary.label.setText("Enter target:")
        self.withsalary.label.setStyleSheet("font-weight: bold;")
        self.withsalary.combox = QComboBox(self.withsalary)
        self.withsalary.combox.move(25, 35)
        self.withsalary.combox.resize(50, 30)
        self.withsalary.combox.addItems(self.int_operations)
        self.withsalary.but = QPushButton(self.withsalary)
        self.withsalary.but.move(60, 75)
        self.withsalary.but.resize(75, 30)
        self.withsalary.but.setText("Confirm")
        self.withsalary.but.setStyleSheet("font-weight: bold;")
        self.withsalary.but.clicked.connect(self.find_with_salary)
        self.withsalary.exec_()
        
    def find_with_salary(self: object) -> None:
        """Finds result of search with salary"""
        try:
            self.SearchResults = []
            inputed = eval(self.withsalary.textbox.text())
            oper = self.int_operations[self.withsalary.combox.currentIndex()]
            self.withsalary.close()
            if type(inputed) in [int, float]:
                result = []
                match oper:
                    case ">":
                        for employee in range(len(Employee.employees)):
                            if Employee.employees[employee].salary > inputed:
                                result.append(Employee.employees[employee])
                    case "<":
                        for employee in range(len(Employee.employees)):
                            if Employee.employees[employee].salary < inputed:
                                result.append(Employee.employees[employee])
                    case "==":
                        for employee in range(len(Employee.employees)):
                            if Employee.employees[employee].salary == inputed:
                                result.append(Employee.employees[employee])
                    case "!=":
                        for employee in range(len(Employee.employees)):
                            if Employee.employees[employee].salary != inputed:
                                result.append(Employee.employees[employee])
                    case ">=":
                        for employee in range(len(Employee.employees)):
                            if Employee.employees[employee].salary >= inputed:
                                result.append(Employee.employees[employee])
                    case "<=":
                        for employee in range(len(Employee.employees)):
                            if Employee.employees[employee].salary <= inputed:
                                result.append(Employee.employees[employee])
                self.SearchResults = result
                self.search_results_viewer()
                self.reload()
            else:
                warn = QMessageBox()
                warn.setWindowTitle("Warning")
                warn.setText("Salary must be int or float!")
                warn.setIcon(QMessageBox.Warning)
                warn.exec_()  
        except Exception as e:
            warn = QMessageBox()
            warn.setWindowTitle("Warning")
            warn.setText(f"Unknown error occured!\nException:\n{e}")
            warn.setIcon(QMessageBox.Warning)
            warn.exec_()

    # with age
    def find_with_age_form(self: object) -> None:
        """Shows search with age form"""
        self.withage = QDialog()
        self.withage.setWindowTitle("With Age")
        self.withage.setFixedSize(200, 100)
        self.withage.textbox = QLineEdit(self.withage)
        self.withage.textbox.move(75, 35)
        self.withage.textbox.resize(100, 30)
        self.withage.label = QLabel(self.withage)
        self.withage.label.move(50, 0)
        self.withage.label.resize(100, 30)
        self.withage.label.setText("Enter target:")
        self.withage.label.setStyleSheet("font-weight: bold;")
        self.withage.combox = QComboBox(self.withage)
        self.withage.combox.move(25, 35)
        self.withage.combox.resize(50, 30)
        self.withage.combox.addItems(self.int_operations)
        self.withage.but = QPushButton(self.withage)
        self.withage.but.move(60, 75)
        self.withage.but.resize(75, 30)
        self.withage.but.setText("Confirm")
        self.withage.but.setStyleSheet("font-weight: bold;")
        self.withage.but.clicked.connect(self.find_with_age)
        self.withage.exec_()
    
    def find_with_age(self: object) -> None:
        """Finds result of search with age"""
        try:
            self.SearchResults = []
            inputed = eval(self.withage.textbox.text())
            oper = self.int_operations[self.withage.combox.currentIndex()]
            self.withage.close()
            if type(inputed) in [int, float]:
                result = []
                match oper:
                    case ">":
                        for employee in range(len(Employee.employees)):
                            if Employee.employees[employee].age > inputed:
                                result.append(Employee.employees[employee])
                    case "<":
                        for employee in range(len(Employee.employees)):
                            if Employee.employees[employee].age < inputed:
                                result.append(Employee.employees[employee])
                    case "==":
                        for employee in range(len(Employee.employees)):
                            if Employee.employees[employee].age == inputed:
                                result.append(Employee.employees[employee])
                    case "!=":
                        for employee in range(len(Employee.employees)):
                            if Employee.employees[employee].age != inputed:
                                result.append(Employee.employees[employee])
                    case ">=":
                        for employee in range(len(Employee.employees)):
                            if Employee.employees[employee].age >= inputed:
                                result.append(Employee.employees[employee])
                    case "<=":
                        for employee in range(len(Employee.employees)):
                            if Employee.employees[employee].age <= inputed:
                                result.append(Employee.employees[employee])
                self.SearchResults = result
                self.search_results_viewer()
                self.reload()
            else:
                warn = QMessageBox()
                warn.setWindowTitle("Warning")
                warn.setText("Salary must be int or float!")
                warn.setIcon(QMessageBox.Warning)
                warn.exec_()  
        except Exception as e:
            warn = QMessageBox()
            warn.setWindowTitle("Warning")
            warn.setText(f"Unknown error occured!\nException:\n{e}")
            warn.setIcon(QMessageBox.Warning)
            warn.exec_()

    # with skills
    def find_with_skills_form(self: object) -> None:
        """Shows search with skills form"""

        # load template
        self.withskills = uic.loadUi(f"{mainpath}/findskillsselector.ui")

        # dialog settings
        self.withskills.setWindowTitle("Search with Skills")
        self.withskills.setFixedSize(460, 170)

         # confirm button
        self.withskills.but = QPushButton(self.withskills)
        self.withskills.but.move(190, 130)
        self.withskills.but.resize(80, 30)
        self.withskills.but.setText("Confirm")
        self.withskills.but.setStyleSheet("font-weight: bold;")
        self.withskills.but.clicked.connect(self.find_with_skills)

        # show
        self.withskills.show()

    def find_with_skills(self: object) -> None:
        """Finds result of search with skills"""
        try:
            self.SearchResults = []
            skills  = []
            cb = self.withskills.frame_2.findChildren(QCheckBox)
            for res in range(len(cb)):
                if bool(cb[res].isChecked()) == True:
                    skills.append(self.skill_names[res])
            result = []
            for employee in range(len(Employee.employees)):
                if counterSubset(skills, Employee.employees[employee].skills):
                    result.append(Employee.employees[employee])
            self.withskills.close()
            self.SearchResults = result
            self.search_results_viewer()
        except Exception as e:
            warn = QMessageBox()
            warn.setWindowTitle("Warning")
            warn.setText(f"Unknown error with get data from form occured! (Pass form again)\nException:\n{e}")
            warn.setIcon(QMessageBox.Warning)
            warn.exec_()
  
    # with name
    def find_with_name_form(self: object) -> None:
        """Shows search with name form"""
        self.withname = QDialog()
        self.withname.setWindowTitle("With Name")
        self.withname.setFixedSize(200, 100)
        self.withname.textbox = QLineEdit(self.withname)
        self.withname.textbox.move(40, 35)
        self.withname.textbox.resize(120, 30)
        self.withname.label = QLabel(self.withname)
        self.withname.label.move(40, 0)
        self.withname.label.resize(120, 30)
        self.withname.label.setText("Enter Target:")
        self.withname.label.setStyleSheet("font-weight: bold;")
        self.withname.but = QPushButton(self.withname)
        self.withname.but.move(60, 75)
        self.withname.but.resize(75, 30)
        self.withname.but.setText("Confirm")
        self.withname.but.setStyleSheet("font-weight: bold;")
        self.withname.but.clicked.connect(self.find_with_name)
        self.withname.exec_()

    def find_with_name(self: object) -> None:
        """Finds result of search with name"""
        try:
            self.SearchResults = []
            inputed = str(self.withname.textbox.text()).lower()
            if inputed != "":
                result = []
                self.withname.close()
                target_len = len(inputed)
                bool_res = [True if x == inputed else False for x in [x[:target_len] for x in [x.name.lower() for x in Employee.employees]]]
                for index in range(len(bool_res)):
                    if bool_res[index] == True:
                        result.append(Employee.employees[index])
                self.SearchResults = result
                self.search_results_viewer()
            else:
                warn = QMessageBox()
                warn.setWindowTitle("Warning")
                warn.setText("You need to enter name!")
                warn.setIcon(QMessageBox.Warning)
                warn.exec_()  
        except Exception as e:
            warn = QMessageBox()
            warn.setWindowTitle("Warning")
            warn.setText(f"Unknown error with get data from form occured! (Pass form again)\nException:\n{e}")
            warn.setIcon(QMessageBox.Warning)
            warn.exec_()

    # view results of search
    def search_results_viewer(self: object) -> None:
        """Views results of search in list below \"With Conditions:\""""
        self.listWidget_2.clear()
        res = self.SearchResults
        if len(res) > 0:
            for employee in range(len(res)):
                self.listWidget_2.addItem(f"{employee+1}. Name: {res[employee].name} | Salary: {res[employee].salary} | Age: {res[employee].age} | Skills: {str(res[employee].skills).replace("[", "").replace("]", "")}")
    
    # set salary
    def set_salary_form(self: object) -> None:
        """Sets salary for selected employee"""
        self.setsalaryform = QDialog()
        self.setsalaryform.setWindowTitle("Set Salary")
        self.setsalaryform.setFixedSize(200, 100)
        self.setsalaryform.textbox = QLineEdit(self.setsalaryform)
        self.setsalaryform.textbox.move(40, 35)
        self.setsalaryform.textbox.resize(120, 30)
        self.setsalaryform.label = QLabel(self.setsalaryform)
        self.setsalaryform.label.move(40, 0)
        self.setsalaryform.label.resize(120, 30)
        self.setsalaryform.label.setText("Enter New Salary:")
        self.setsalaryform.label.setStyleSheet("font-weight: bold;")
        self.setsalaryform.but = QPushButton(self.setsalaryform)
        self.setsalaryform.but.move(60, 75)
        self.setsalaryform.but.resize(75, 30)
        self.setsalaryform.but.setText("Confirm")
        self.setsalaryform.but.setStyleSheet("font-weight: bold;")
        self.setsalaryform.but.clicked.connect(self.set_salary)
        self.setsalaryform.exec_()

    def set_salary(self: object) -> None:
        try:
            inputed = eval(self.setsalaryform.textbox.text())
            self.setsalaryform.close()
            if type(inputed) in [int, float]:
                new_salary = inputed
                if self.MainListRow_ID != -1:
                    idx = self.MainListRow_ID
                    selected_emp_name = Employee.employees[idx].name
                else:
                    idx = self.SearchListRow_ID
                    selected_emp_name = self.SearchResults[idx].name
                set(selected_emp_name, "Salary", new_salary)
                self.SearchResults = []
                self.search_results_viewer()
                self.reload()
            else:
                warn = QMessageBox()
                warn.setWindowTitle("Warning")
                warn.setText("Salary must be int or float!")
                warn.setIcon(QMessageBox.Warning)
                warn.exec_()  
        except Exception as e:
            warn = QMessageBox()
            warn.setWindowTitle("Warning")
            warn.setText(f"Unknown error occured!\nException:\n{e}")
            warn.setIcon(QMessageBox.Warning)
            warn.exec_()

    # set age
    def set_age_form(self: object) -> None:
        """Sets age for selected employee"""
        self.setageform = QDialog()
        self.setageform.setWindowTitle("Set Age")
        self.setageform.setFixedSize(200, 100)
        self.setageform.textbox = QLineEdit(self.setageform)
        self.setageform.textbox.move(40, 35)
        self.setageform.textbox.resize(120, 30)
        self.setageform.label = QLabel(self.setageform)
        self.setageform.label.move(40, 0)
        self.setageform.label.resize(120, 30)
        self.setageform.label.setText("Enter New Age:")
        self.setageform.label.setStyleSheet("font-weight: bold;")
        self.setageform.but = QPushButton(self.setageform)
        self.setageform.but.move(60, 75)
        self.setageform.but.resize(75, 30)
        self.setageform.but.setText("Confirm")
        self.setageform.but.setStyleSheet("font-weight: bold;")
        self.setageform.but.clicked.connect(self.set_age)
        self.setageform.exec_()

    def set_age(self:object) -> None:
        try:
            inputed = eval(self.setageform.textbox.text())
            self.setageform.close()
            if type(inputed) in [int, float]:
                new_age = inputed
                if self.MainListRow_ID != -1:
                    idx = self.MainListRow_ID
                    selected_emp_name = Employee.employees[idx].name
                else:
                    idx = self.SearchListRow_ID
                    selected_emp_name = self.SearchResults[idx].name
                set(selected_emp_name, "Age", new_age)
                self.SearchResults = []
                self.search_results_viewer()
                self.reload()
            else:
                warn = QMessageBox()
                warn.setWindowTitle("Warning")
                warn.setText("Salary must be int!")
                warn.setIcon(QMessageBox.Warning)
                warn.exec_()  
        except Exception as e:
            warn = QMessageBox()
            warn.setWindowTitle("Warning")
            warn.setText(f"Unknown error occured!\nException:\n{e}")
            warn.setIcon(QMessageBox.Warning)
            warn.exec_()

    # set skills
    def set_skills_form(self: object) -> None:
        """Sets selected skills for selected employee"""

        # load template
        self.setskillsform = uic.loadUi(f"{mainpath}/setskillsselector.ui")

        # dialog settings
        self.setskillsform.setWindowTitle("Set Skills Form")
        self.setskillsform.setFixedSize(460, 170)

        # confirm button
        self.setskillsform.but = QPushButton(self.setskillsform)
        self.setskillsform.but.move(190, 130)
        self.setskillsform.but.resize(80, 30)
        self.setskillsform.but.setText("Confirm")
        self.setskillsform.but.setStyleSheet("font-weight: bold;")
        self.setskillsform.but.clicked.connect(self.set_skills)

        # show
        self.setskillsform.show()

    def set_skills(self: object) -> None:
        """Set new skills to employee"""
        try:
            if self.MainListRow_ID != -1:
                    idx = self.MainListRow_ID
                    selected_emp_name = Employee.employees[idx].name
            else:
                    idx = self.SearchListRow_ID
                    selected_emp_name = self.SearchResults[idx].name
            skills  = []
            cb = self.setskillsform.frame_2.findChildren(QCheckBox)
            for res in range(len(cb)):
                if bool(cb[res].isChecked()) == True:
                    skills.append(self.skill_names[res])
            set(selected_emp_name, "Skills", skills)
            self.setskillsform.close()
            self.SearchResults = []
            self.search_results_viewer()
            self.reload()
        except Exception as e:
            warn = QMessageBox()
            warn.setWindowTitle("Warning")
            warn.setText(f"Unknown error with get data from form occured! (Pass form again)\nException:\n{e}")
            warn.setIcon(QMessageBox.Warning)
            warn.exec_()

    # operations with employees
    def add_employee_form(self: object) -> None:
        """Form with input fields for add employee to list"""

        # load template
        self.addform = uic.loadUi(f"{mainpath}/addform.ui")

        # dialog settings
        self.addform.setWindowTitle("Add Employee Form")
        self.addform.setFixedSize(500, 350)
        self.addform.spinBox_3.setMaximum(1000000)
        self.addform.spinBox_4.setMaximum(10000)

        # button connects
        self.addform.pushButton_3.clicked.connect(self.add_emp_from_form)
        self.addform.pushButton_2.clicked.connect(self.cancel_add_emp)

        self.addform.show()

    def remove_by_index(self: object) -> None:
        """Removes selected employee"""
        try:
            if self.MainListRow_ID != -1:
                    idx = self.MainListRow_ID
                    selected_emp_name = Employee.employees[idx].name
            else:
                    idx = self.SearchListRow_ID
                    selected_emp_name = self.SearchResults[idx].name
            remove_emp(selected_emp_name)
            self.MainListRow_ID = -1
            self.SearchResults = []
            self.search_results_viewer()
            self.reload()
        except Exception as e:
            warn = QMessageBox()
            warn.setWindowTitle("Warning")
            warn.setText(f"Unknown error with get selected row occured, probably you need to select any row!\nException:\n{e}")
            warn.setIcon(QMessageBox.Warning)
            warn.exec_()

    def cancel_add_emp(self: object) -> None:
        """Cancels adding employee"""
        self.addform.close()
        self.reload()

    def get_add_form_data(self: object) -> list:
        """Gets data from add employee form"""
        try:
            name = str(self.addform.lineEdit_2.text())
            salary = int(self.addform.spinBox_3.value())
            age = int(self.addform.spinBox_4.value())
            skills  = []
            cb = self.addform.frame_2.findChildren(QCheckBox)
            for res in range(len(cb)):
                if bool(cb[res].isChecked()) == True:
                    skills.append(self.skill_names[res])
            return [name, salary, age, skills]
        except Exception as e:
            warn = QMessageBox()
            warn.setWindowTitle("Warning")
            warn.setText(f"Unknown error with get data from form occured, please input valid! (Pass form again)\nException:\n{e}")
            warn.setIcon(QMessageBox.Warning)
            warn.exec_()
    
    def add_emp_from_form(self: object) -> None:
        data = self.get_add_form_data()
        name = data[0]
        salary = data[1]
        age = data[2]
        skills = data[3]
        add_emp(str(name), int(salary), int(age), skills)
        self.reload()
        self.addform.close()

    def save_filename_form(self: object) -> None:
        """Form with input field for save file"""
        self.saveasform = QDialog()
        self.saveasform.setWindowTitle("Save As")
        self.saveasform.setFixedSize(200, 100)
        self.saveasform.textbox = QLineEdit(self.saveasform)
        self.saveasform.textbox.move(25, 35)
        self.saveasform.textbox.resize(100, 30)
        self.saveasform.label = QLabel(self.saveasform)
        self.saveasform.label.move(50, 0)
        self.saveasform.label.resize(100, 30)
        self.saveasform.label.setText("Enter File Name:")
        self.saveasform.label.setStyleSheet("font-weight: bold;")
        self.saveasform.combox = QComboBox(self.saveasform)
        self.saveasform.combox.move(125, 35)
        self.saveasform.combox.resize(50, 30)
        self.saveasform.combox.addItems(self.formats)
        self.saveasform.but = QPushButton(self.saveasform)
        self.saveasform.but.move(60, 75)
        self.saveasform.but.resize(75, 30)
        self.saveasform.but.setText("Confirm")
        self.saveasform.but.setStyleSheet("font-weight: bold;")
        self.saveasform.but.clicked.connect(self.save_as)
        self.saveasform.exec_()

    def save_as(self: object) -> None:
        """Function which saves list in file"""
        inputed = f"{self.saveasform.textbox.text()}{self.formats[self.saveasform.combox.currentIndex()]}"
        if inputed != None:
            self.saveasform.close()
            if get_list() != None:
                save_data(inputed, get_list())
                self.reload()
            else:
                warn = QMessageBox()
                warn.setWindowTitle("Warning")
                warn.setText("Error, list is empty! (Add information to list)")
                warn.setIcon(QMessageBox.Warning)
                warn.exec_()
        else:
            warn = QMessageBox()
            warn.setWindowTitle("Warning")
            warn.setText("Unknown error with saving data occured, please set valid file name! (Save information again)")
            warn.setIcon(QMessageBox.Warning)
            warn.exec_()

    def MainListSelectionChanged(self: object) -> None:
        """Main List's Selection change processor"""
        try:
            self.listWidget_2.clearSelection()
            self.SearchListRow_ID = -1
            self.SearchListRow_CONTENT = ""

            self.MainListRow_ID = int(self.listWidget.currentRow())

            emp_num = int(self.MainListRow_ID)+1
            emp_name = Employee.employees[int(self.MainListRow_ID)].name
            emp_salary = Employee.employees[int(self.MainListRow_ID)].salary
            emp_age = Employee.employees[int(self.MainListRow_ID)].age
            emp_skills = str(Employee.employees[int(self.MainListRow_ID)].skills).replace("[", "").replace("]", "")
            
            
            self.MainListRow_CONTENT = f"{emp_num}. Name: {emp_name} | Salary: {emp_salary} | Age: {emp_age} | Skills: {emp_skills}"
        except:...
    def SearchListSelectionChanged(self: object) -> None:
        """Search List's Selection change processor"""
        try:
            self.listWidget.clearSelection()
            self.MainListRow_ID = -1
            self.MainListRow_CONTENT = ""

            self.SearchListRow_ID = int(self.listWidget_2.currentRow())

            emp = self.SearchResults[self.SearchListRow_ID]

            self.SearchListRow_CONTENT = f"{(self.SearchListRow_ID+1)}. Name: {emp.name} | Salary: {emp.salary} | Age: {emp.age} | Skills: {emp.skills}"
        except:...

    def copy(self: object) -> None:
        """OS copy selected"""
        try:
            if self.MainListRow_ID != -1:
                addToClipBoard(str(self.MainListRow_CONTENT).replace("|", "/"))
            elif self.SearchListRow_ID != -1:
                addToClipBoard(str(self.SearchListRow_CONTENT).replace("|", "/"))
        except:...

    def exit_file(self: object) -> None:
        """Resets file and data"""
        self.file = ""
        reset_list()
        self.SearchResults = []
        self.search_results_viewer()
        self.reload()

    def open_filename_form(self: object) -> None:
        """Form with input field for open file"""
        self.openform = QDialog()
        self.openform.setWindowTitle("Open file")
        self.openform.setFixedSize(200, 100)
        self.openform.textbox = QLineEdit(self.openform)
        self.openform.textbox.move(25, 35)
        self.openform.textbox.resize(100, 30)
        self.openform.label = QLabel(self.openform)
        self.openform.label.move(50, 0)
        self.openform.label.resize(100, 30)
        self.openform.label.setText("Enter File Name:")
        self.openform.label.setStyleSheet("font-weight: bold;")
        self.openform.combox = QComboBox(self.openform)
        self.openform.combox.move(125, 35)
        self.openform.combox.resize(50, 30)
        self.openform.combox.addItems(self.formats)
        self.openform.but = QPushButton(self.openform)
        self.openform.but.move(60, 75)
        self.openform.but.resize(75, 30)
        self.openform.but.setText("Confirm")
        self.openform.but.setStyleSheet("font-weight: bold;")
        self.openform.but.clicked.connect(self.setfilename)
        self.openform.exec_()

    def load(self: object) -> None:
        """load data from selected file"""
        if self.file == "":
            # add_from(load_data())
            self.open_filename_form()
        else:
            try:
                add_from(load_data(self.file))
                self.SearchResults = []
                self.search_results_viewer()
                self.reload()
            except Exception as e:
                warn = QMessageBox()
                warn.setWindowTitle("Warning")
                warn.setText(f"Unknown error with loading data occured, please set valid file name! (Open file again)\nException:\n{e}")
                warn.setIcon(QMessageBox.Warning)
                warn.exec_()
                self.file = ""

    def setfilename(self: object) -> None:
        """Selects file"""
        inputed = f"{self.openform.textbox.text()}{self.formats[self.openform.combox.currentIndex()]}"
        if inputed != None:
            self.file = inputed
            self.openform.close()
            self.load()
            self.reload()
        else:
            warn = QMessageBox()
            warn.setWindowTitle("Warning")
            warn.setText("Unknown error with saving data occured, please set valid file name! (Open file again)")
            warn.setIcon(QMessageBox.Warning)
            warn.exec_()
            self.file = ""
        
    def save(self: object) -> None:
        """Save data in selected file"""
        if self.file != "":
            if get_list() != None:
                save_data(self.file, get_list())
                self.reload()
        else:
            warn = QMessageBox()
            warn.setWindowTitle("Warning")
            warn.setText("Unknown error with saving data occured, please re-set file name! (Open file again)")
            warn.setIcon(QMessageBox.Warning)
            warn.exec_()
            self.file = ""

    def savenexit(self: object) -> None:
        """Selects data in selected file and exit"""
        if self.file != "":
            if get_list() != None:
                save_data(self.file, get_list())
                self.reload()
                window.close()
        else:
            warn = QMessageBox()
            warn.setWindowTitle("Warning")
            warn.setText("Unknown error with saving data occured, please re-set file name! (Open file again or use \"Save as\")")
            warn.setIcon(QMessageBox.Warning)
            warn.exec_()
            self.file = ""
    
    def exit(self: object) -> None:
        """Exit without save"""
        window.close()

    def reload(self: object) -> None: 
        """refreshes data in WindgetList"""
        self.listWidget.clear()
        if len(Employee.employees) > 0:
            for employee in range(len(Employee.employees)):
                info_emp = str(f"{employee+1}. Name: {Employee.employees[employee].name} | Salary: {Employee.employees[employee].salary} | Age: {Employee.employees[employee].age} | Skills: {str(Employee.employees[employee].skills).replace("[", "").replace("]", "")}")
                self.listWidget.addItem(info_emp
                )

if __name__ == '__main__': 
    app = QApplication(sys.argv) 
    window = UI() 
    window.show() 
    sys.exit(app.exec_()) 