from ctypes import alignment
from datetime import datetime
from pydoc import text
from tkinter import *
import tkinter
from tkinter.ttk import Treeview, Combobox
from turtle import title
from ttkwidgets import autocomplete
import regex as re
import pandas as pd
import datetime as dt


pattern = r"%\d{8}"
filename_for_the_day = "ICF_ATTENDANCE_" + dt.date.today().strftime("%m_%d_%Y") + ".csv"
print(filename_for_the_day)


def getId(extracted_id):
    id = entry_id.get()

    if re.search(pattern, id) or (len(id) == 8 and id.isnumeric):
        if len(id) != 8:
            extracted_id = re.search(pattern, id).group(0).lstrip("%")
        else:
            extracted_id = id
    if extracted_id:
        found, name, email, phone = searchInDB(extracted_id)
        root.after(5000, lambda: label_output.config(text=""))
        if found:
            label_output["text"] = "Hello " + name
            make_attendance_sheet(extracted_id, name, email, phone)
        else:
            label_output["text"] = "ID not found. Try adding new student below."
            root.after(5000, lambda: label_output.config(text=""))
    else:
        label_output["text"] = "Invalid ID"
        root.after(5000, lambda: label_output.config(text=""))
    entry_id.delete(0, "end")


def duplicatePresent(extracted_id):
    present = 0
    try:
        with open(filename_for_the_day, "r") as file:
            lines = file.readlines()
            for line in lines:
                if extracted_id == line.split(",")[0]:
                    present = 1
                    break
            file.close()
    except:
        pass
    return present


def make_attendance_sheet(extracted_id, name, email, phone):
    if not duplicatePresent(extracted_id):
        l = 0
        try:
            with open(filename_for_the_day, "r") as file:
                l = len(file.readlines())
                file.close()
        except:
            pass
        with open(filename_for_the_day, "a+") as file:
            if not l:
                file.write("id,name,email,phone_number,")
            file.write(
                "\n"
                + str(extracted_id)
                + ","
                + str(name)
                + ","
                + str(email)
                + ","
                + str(phone)
                + ","
            )
            file.close()
        updateTree()
    else:
        label_output["text"] = name + " has already signed in"
        root.after(5000, lambda: label_output.config(text=""))


def updateTree():
    try:
        with open(filename_for_the_day, "r") as file:
            lines = file.readlines()
            file.close()
        tree.delete(*tree.get_children())
        for idx, line in enumerate(lines[::-1][:-1]):
            if line == "\n":
                continue
            tree.insert(
                "",
                "end",
                values=(
                    str(len(lines) - idx - 1),
                    line.rstrip("\n").split(",")[0],
                    line.rstrip("\n").split(",")[1],
                    line.rstrip("\n").split(",")[2],
                    line.rstrip("\n").split(",")[3],
                ),
            )

    except:
        pass


def searchInDB(id):
    students = pd.read_csv("dummy_db.csv")
    for row_num in range(len(students)):
        if not pd.isna(students.loc[row_num][0]):
            if int(students.loc[row_num][0]) == int(id):
                return (
                    1,
                    students.loc[row_num][1],
                    students.loc[row_num][4],
                    students.loc[row_num][3],
                )

    return (0, None, None, None)


def addNewStudent(id, name, country, email, phone, major, graduation_year):

    with open("dummy_db.csv", "a+") as file:
        file.write(
            "\n"
            + str(id)
            + ","
            + str(name)
            + ","
            + str(country)
            + ","
            + str(phone)
            + ","
            + str(email)
            + ","
            + str(major)
            + ","
            + str(graduation_year)
        )
    file.close()
    make_attendance_sheet(id, name, email, phone)
    label_output["text"] = "Hello " + name
    root.after(5000, lambda: label_output.config(text=""))
    new_student_id.delete(0, "end")
    new_student_name.delete(0, "end")
    new_student_country.delete(0, "end")
    new_student_phone.delete(0, "end")
    new_student_email.delete(0, "end")
    new_student_graduation_year.delete(0, "end")
    choose_major.set("")


if __name__ == "__main__":
    root = Tk()
    root.title("Attendance for ICF")
    # root.iconphoto(False, tk.PhotoImage(file=''))
    extracted_id = ""
    root.geometry("1050x500")
    label_tag = Label(root, text="Enter student ID -")
    entry_id = Entry(root)
    entry_id.focus()
    button_submit = Button(root, text="Submit", command=lambda: getId(extracted_id))
    label_output = Label(root, anchor="w")
    tree = Treeview(root, columns=("No.", "Id", "Name", "Email", "Phone"), height=200)

    tree.column("No.", width=50, anchor="center")
    tree.column("Id", width=90, anchor="center")
    tree.column("Name", width=200, anchor="center")
    tree.column("Email", width=200, anchor="center")
    tree.column("Phone", width=100, anchor="center")
    tree.column("#0", width=0)

    tree.heading("No.", text="No.")
    tree.heading("Id", text="Id")
    tree.heading("Name", text="Name")
    tree.heading("Email", text="Email")
    tree.heading("Phone", text="Phone")

    updateTree()

    new_id_tag = Label(root, text="Enter ID:")
    new_student_id = Entry(root)

    new_name_tag = Label(root, text="Enter name:")
    new_student_name = Entry(root)

    new_country_tag = Label(root, text="Enter country:")
    new_student_country = Entry(root)

    new_email_tag = Label(root, text="Enter email:")
    new_student_email = Entry(root)

    new_phone_tag = Label(root, text="Enter phone:")
    new_student_phone = Entry(root)

    new_graduation_year_tag = Label(root, text="Grad year:")
    new_student_graduation_year = Entry(root)

    new_major_tag = Label(root, text="Choose major:")
    new_student_major = tkinter.StringVar()

    majors = [
        "ACTUARIAL MATHEMATICS AND QUANTITATIVE RISK - M.S.",
        "ANALYTICS MBA",
        "APPLIED MATHEMATICS - M.S.",
        "BIOENGINEERING - M.S.",
        "BIOMEDICAL ENGINEERING - M.ENG.",
        "BIOMEDICAL ENGINEERING - PH.D.",
        "BUILT ENVIRONMENT - PH.D.",
        "BUSINESS INTELLIGENCE & ANALYTICS",
        "CHEMICAL BIOLOGY - M.S.",
        "CHEMICAL BIOLOGY - PH.D.",
        "CHEMICAL ENGINEERING - M.ENG.",
        "CHEMICAL ENGINEERING - PH.D.",
        "CHEMISTRY - M.S.",
        "CHEMISTRY - PH.D.",
        "CIVIL ENGINEERING - M.ENG. - ENGR.",
        "CIVIL ENGINEERING - PH.D.",
        "COMPUTER ENGINEERING - M.S. - M.ENG. - ENGR.",
        "COMPUTER ENGINEERING - PH.D.",
        "COMPUTER SCIENCE - M.S. - ENGR.",
        "COMPUTER SCIENCE - PH.D.",
        "CONSTRUCTION ENGINEERING AND MANAGEMENT - M.ENG.",
        "CONSTRUCTION MANAGEMENT - M.S.",
        "CYBERSECURITY - M.S.",
        "DATA SCIENCE - M.S.",
        "ELECTRICAL ENGINEERING - M.S. - M.ENG. - ENGR.",
        "ELECTRICAL ENGINEERING - PH.D.",
        "ENGINEERING MANAGEMENT - M.ENG.",
        "ENGINEERING MANAGEMENT - PH.D.",
        "ENGINEERING PHYSICS - M.ENG.",
        "ENTERPRISE PROJECT MANAGEMENT",
        "ENVIRONMENTAL ENGINEERING - M.ENG.",
        "ENVIRONMENTAL ENGINEERING - PH.D.",
        "EXECUTIVE MBA (EMBA)",
        "FINANCE",
        "FINANCIAL ANALYTICS",
        "FINANCIAL ENGINEERING",
        "INFORMATION SYSTEMS",
        "MACHINE LEARNING - M.S.",
        "MANAGEMENT",
        "MATERIALS SCIENCE & ENGINEERING - M.S. - M.ENG.",
        "MATERIALS SCIENCE & ENGINEERING - PH.D.",
        "MATHEMATICS - M.S.",
        "MATHEMATICS - PH.D.",
        "MECHANICAL ENGINEERING - M.ENG. - ENGR.",
        "MECHANICAL ENGINEERING - PH.D.",
        "MEDIA & BROADCAST ENGINEERING - M.S.",
        "NETWORK & COMMUNICATION MANAGEMENT & SERVICES",
        "OCEAN ENGINEERING - M.ENG.",
        "OCEAN ENGINEERING - PH.D.",
        "PHARMACEUTICAL MANUFACTURING; ENGINEERING - M.S.",
        "PHYSICS - M.S.",
        "PHYSICS - PH.D.",
        "ROBOTICS - M.ENG.",
        "SOCIO-TECHNICAL SYSTEMS - PH.D.",
        "SOFTWARE ENGINEERING - M.S.",
        "SPACE SYSTEMS ENGINEERING - M.ENG.",
        "STEVENS MBA",
        "SUSTAINABILITY MANAGEMENT - M.S.APPLIED ARTIFICIAL INTELLIGENCE - M.S. - M.ENG.",
        "SYSTEMS ANALYTICS - M.ENG.",
        "SYSTEMS ENGINEERING - M.ENG.",
        "SYSTEMS ENGINEERING - PH.D.",
        "TECHNOLOGY MANAGEMENT",
    ]
    choose_major = autocomplete.AutocompleteCombobox(
        textvariable=new_student_major, completevalues=majors
    )

    new_student_submit = Button(
        root,
        text="Add New",
        command=lambda: addNewStudent(
            new_student_id.get(),
            new_student_name.get(),
            new_student_country.get(),
            new_student_email.get(),
            new_student_phone.get(),
            new_student_major.get(),
            new_student_graduation_year.get(),
        ),
    )
    label_tag.place(height=20, width=100, x=60, y=10)
    entry_id.place(height=20, width=200, x=170, y=10)

    label_output.place(height=20, width=300, x=380, y=10)
    button_submit.place(height=30, width=70, x=170, y=35)

    new_id_tag.place(height=20, width=75, x=10, y=90)
    new_student_id.place(height=20, width=300, x=90, y=90)

    new_name_tag.place(height=20, width=75, x=10, y=120)
    new_student_name.place(height=20, width=300, x=90, y=120)

    new_country_tag.place(height=20, width=75, x=10, y=150)
    new_student_country.place(height=20, width=300, x=90, y=150)

    new_phone_tag.place(height=20, width=75, x=10, y=180)
    new_student_phone.place(height=20, width=300, x=90, y=180)

    new_email_tag.place(height=20, width=75, x=10, y=210)
    new_student_email.place(height=20, width=300, x=90, y=210)

    new_graduation_year_tag.place(height=20, width=75, x=10, y=240)
    new_student_graduation_year.place(height=20, width=300, x=90, y=240)

    new_major_tag.place(height=20, width=75, x=10, y=270)
    choose_major.place(height=20, width=300, x=90, y=270)

    new_student_submit.place(height=20, width=100, x=90, y=320)

    tree.place(height=410, width=650, x=400, y=90)

    verscrlbar = tkinter.Scrollbar(root, orient="vertical", command=tree.yview)
    verscrlbar.pack(side="right", fill="x")
    tree.configure(xscrollcommand=verscrlbar.set)

    root.bind("<Return>", lambda e: getId(extracted_id))
    root.mainloop()
