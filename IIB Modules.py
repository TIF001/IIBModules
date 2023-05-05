from tkinter import *
from tkinter.ttk import *
from dataclasses import dataclass
import csv
from pathlib import Path

BASEWIDTH = 10  # The width used by the 4th year module buttons

# The colour palette of the GUI
blue = "#4B0092"
lightBlue = "#56b4e9"
green = "#009e73"


@dataclass
class module:  # 4th year modules
    code: str
    name: str
    set: str
    prerequisites: list[str]
    useful: list[str]
    assessment: str  # Exam, coursework or both
    selectable: bool = True


@dataclass
class area:  # Engineering areas
    name: str
    rule: str
    modules: str
    qualified: bool = False


def importer():
    # Reads the three csv files

    scriptPath = Path(__file__, '..').resolve()  # Store the address of this file, later used for relative addressing

    with open(scriptPath.joinpath("ModuleList.csv"), encoding="utf-8-sig", newline='') as csvfile:  # Read the modules
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[3] == "None":  # Assumed modules
                row[3] = ""
            else:
                row[3] = row[3].split(sep=", ")

            if row[4] == "None":  # Useful modules
                row[4] = ""
            else:
                row[4] = row[4].split(sep=", ")

            modules.append(module(row[0], row[1], row[2], row[3], row[4], row[5]))

    with open(scriptPath.joinpath('Areas.csv'), encoding="utf-8-sig", newline='') as csvfile:  # Read the areas
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            areas.append(area(row[0], row[1], row[2:]))

    global thirdYearModules
    with open(scriptPath.joinpath('thirdYearModules.csv'), encoding="utf-8-sig", newline='') as csvfile:  # Read the third year modules
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            thirdYearModules = row


def initializeStatic():
    # Create and place the non-button GUI elements

    window.title("IIB Modules")
    window.state("zoomed")  # Start with the window maximised

    # Set the relative width and height of the columns
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)
    window.grid_columnconfigure(3, weight=4)
    window.grid_columnconfigure(4, weight=4)
    window.grid_columnconfigure(5, weight=4)

    for i in range(24):
        window.grid_rowconfigure(i, weight=1)

    # Set the design of the button variants
    style = Style()
    style.theme_use("default")

    style.map("SelectedAndHighlighted.TButton",
              background=[("active", green), ("!active", green)],
              foreground=[("active", blue), ("!active", blue)])

    style.map("Selected.TButton",
              background=[("active", green), ("!active", green)])

    style.map("Highlighted.TButton",
              foreground=[("disabled", lightBlue), ("active", blue), ("!active", blue), ])

    # Reset button
    resetButton = Button(window, text="Reset", command=lambda: reset())
    resetButton.grid(column=5, row=23, sticky=NSEW, padx=(1, 5), pady=1)

    # Module info box
    moduleCodeLabel = Label(window, text="Module code:")
    moduleCodeLabel.grid(column=2, row=17, sticky=NSEW, padx=5, pady=1)
    moduleCodeDynamic.grid(column=3, row=17, sticky=NSEW, padx=5, pady=1)

    moduleTitleLabel = Label(window, text="Module title:")
    moduleTitleLabel.grid(column=2, row=18, sticky=NSEW, padx=5, pady=1)
    moduleTitleDynamic.grid(column=3, row=18, sticky=NSEW, padx=5, pady=1)

    moduleSetLabel = Label(window, text="Set:")
    moduleSetLabel.grid(column=2, row=19, sticky=NSEW, padx=5, pady=1)
    moduleSetDynamic.grid(column=3, row=19, sticky=NSEW, padx=5, pady=1)

    moduleAssumedLabel = Label(window, text="Assumed prerequisites:")
    moduleAssumedLabel.grid(column=2, row=20, sticky=NSEW, padx=5, pady=1)
    moduleAssumedDynamic.grid(column=3, row=20, sticky=NSEW, padx=5, pady=1)

    moduleUsefulLabel = Label(window, text="Useful prerequisites:")
    moduleUsefulLabel.grid(column=2, row=21, sticky=NSEW, padx=5, pady=1)
    moduleUsefulDynamic.grid(column=3, row=21, sticky=NSEW, padx=5, pady=1)

    moduleAssessmentLabel = Label(window, text="Form of assessment:")
    moduleAssessmentLabel.grid(column=2, row=22, sticky=NSEW, padx=5, pady=1)
    moduleAssessmentDynamic.grid(column=3, row=22, sticky=NSEW, padx=5, pady=1)

    # Qualifying rule display
    rule.grid(row=6, column=4, columnspan=2, rowspan=2, sticky=NSEW)

    # Summary box
    selectedCodesLabel = Label(window, text="Selected modules:")
    selectedCodesLabel.grid(column=4, row=18, sticky=NSEW, padx=(5, 1), pady=1)
    selectedCodesDynamic.grid(column=5, row=18, sticky=NSEW)

    michelmasModulesLabel = Label(window, text="Mich modules:")
    michelmasModulesLabel.grid(column=4, row=19, sticky=NSEW, padx=(5, 1), pady=1)
    michelmasModulesDynamic.grid(column=5, row=19, sticky=NSEW, padx=(1, 5), pady=1)

    lentModulesLabel = Label(window, text="Lent modules:")
    lentModulesLabel.grid(column=4, row=20, sticky=NSEW, padx=(5, 1), pady=1)
    lentModulesDynamic.grid(column=5, row=20, sticky=NSEW, padx=(1, 5), pady=1)

    usefulMissingLabel = Label(window, text="Useful  prerequisites not taken:")
    usefulMissingLabel.grid(column=4, row=21, sticky=NSEW, padx=(5, 1), pady=1)
    usefulMissingDynamic.grid(column=5, row=21, sticky=NSEW, padx=(1, 5), pady=1)

    numberOfExamsLabel = Label(window, text="Number of exams:")
    numberOfExamsLabel.grid(column=4, row=22, sticky=NSEW, padx=(5, 1), pady=1)
    numberOfExamsDynamic.grid(column=5, row=22, sticky=NSEW, padx=(1, 5), pady=1)

    # Top row
    Label(window, text="Third year modules taken", anchor=CENTER).grid(column=0, row=0, columnspan=2, sticky=NSEW, padx=5, pady=1)
    Label(window, text="Group", anchor=CENTER).grid(column=2, row=0, sticky=NSEW, padx=5, pady=1)
    Label(window, text="Fourth year modules (hover over the module to see more info)", anchor=CENTER).grid(column=3, row=0, sticky=NSEW, padx=5, pady=1)
    Label(window, text="Engineering areas (click to highlight relevant modules)", anchor=CENTER).grid(column=4, row=0, columnspan=2, sticky=NSEW, padx=5, pady=1)
    Label(window, text="Summary", anchor=CENTER).grid(column=4, row=17, columnspan=2, sticky=NSEW, padx=5, pady=1)


def reset():
    # Set the states back to the starting state
    global selectedGroup
    global selectedArea

    thirdYearSelected.clear()
    selectedGroup = "A"
    selected.clear()
    selectedCodes.clear()
    selectedArea = area("", "", [])

    refresh()


def initialize3rdyearModules():
    # Create and place the buttons for the third year modules

    row = 1  # position of first button
    column = 0
    for m in thirdYearModules:
        window.thirdYearButtons.append(Button(window, text=m, command=lambda m=m: onthirdButtonPress(m)))
        window.thirdYearButtons[-1].grid(column=column, row=row, sticky=NSEW, pady=1, padx=(1+(-column+1)*5, 1+column*5))
        row += column
        column = (column+1) % 2  # Alternate between 0 and 1


def onthirdButtonPress(m):
    if m in thirdYearSelected:
        thirdYearSelected.remove(m)
    else:
        thirdYearSelected.append(m)

    refresh()


def initializeGroups():

    groups = set()
    for m in modules:
        groups.add(m.code[1])

    groups = list(groups)
    groups.sort()

    row = 1  # location of first button
    for g in groups:
        window.groupButtons.append(Button(window, text=g, command=lambda g=g: ongroupButtonPress(g)))
        window.groupButtons[-1].grid(column=2, row=row, sticky=NSEW, pady=1, padx=5)
        row += 1

    # Select the topmost group
    global selectedGroup
    selectedGroup = groups[0]


def ongroupButtonPress(g):
    global selectedGroup
    selectedGroup = g

    refresh()


def initializeButtons():
    # Creates and places the modules that should be shown

    # Select the modules that should be shown
    ingroup = []
    for m in modules:
        if m.code[1] == selectedGroup:
            ingroup.append(m)

    # Remove the previous set of buttons
    for b in window.fourthYearButtons:
        b.destroy()
    window.fourthYearButtons.clear()

    row = 1
    for m in ingroup:
        window.fourthYearButtons.append(Button(window, text=m.code+" "+m.name, command=lambda m=m: onfourthButtonPress(m), width=7*BASEWIDTH))
        window.fourthYearButtons[-1].grid(column=3, row=row, sticky=NSEW, pady=1, padx=5)
        window.fourthYearButtons[-1].bind("<Enter>", lambda e, mod=m: onEnter(e, mod))  # Used to implement the hover function
        window.fourthYearButtons[-1].bind("<Leave>", onLeave)

        row += 1

        # The modules not available should be greyed out
        if m.selectable is False:
            window.fourthYearButtons[-1].state(["disabled"])


def onEnter(e, m):

    # Fill the module info box
    moduleCodeDynamic.config(text=m.code)
    moduleTitleDynamic.config(text=m.name)
    moduleSetDynamic.config(text=m.set)
    moduleAssumedDynamic.config(text=", ".join(m.prerequisites))
    moduleUsefulDynamic.config(text=", ".join(m.useful))

    if m.assessment == "E+C":
        assessment = "Exam and Coursework"
    elif m.assessment == "E":
        assessment = "Exam"
    else:
        assessment = "Coursework"

    moduleAssessmentDynamic.config(text=assessment)


def onLeave(e):
    # Clear the module info box

    moduleCodeDynamic.config(text="")
    moduleTitleDynamic.config(text="")
    moduleSetDynamic.config(text="")
    moduleAssumedDynamic.config(text="")
    moduleUsefulDynamic.config(text="")
    moduleAssessmentDynamic.config(text="")


def onfourthButtonPress(m):

    if m in selected:
        selected.remove(m)
        selectedCodes.remove(m.code)
    else:
        selected.append(m)
        selectedCodes.append(m.code)

    refresh()


def initializeAreas():

    # Location of the first area button
    column = 4
    row = 1

    for a in areas:  # Create a button for each area
        window.areaButtons.append(Button(window, text=a.name, command=lambda a=a: onareaButtonPress(a)))

        if column == 4:  # Increased padding on the outside
            padx = (5, 1)
        elif column == 5:
            padx = (1, 5)
        window.areaButtons[-1].grid(column=column, row=row, sticky=NSEW, pady=1, padx=padx)
        column += 1
        if column == 6:
            column = 4
            row += 1


def onareaButtonPress(a):
    global selectedArea
    if a != selectedArea:
        selectedArea = a
    else:
        selectedArea = area("", "", [])

    refresh()


def checkSelectability():
    # Checks the selectability of the modules based on the rules set by the department

    takenSets = set()  # The sets from which a module has been taken
    for m in selected:
        takenSets.add(m.set)
    takenSets = list(takenSets)

    for m in modules:

        m.selectable = True  # Assume it is selectable

        # total number of modules
        if len(selected) == 8 and m not in selected:
            m.selectable = False

        # check sets
        if m not in selected and m.set in takenSets:
            m.selectable = False

        # third year prerequisites
        for prereq in m.prerequisites:
            if prereq not in thirdYearSelected:
                m.selectable = False
                if m in selected:
                    selected.remove(m)
                    selectedCodes.remove(m.code)

        # not allowed to take the same module twice
        if m.code in thirdYearSelected:
            m.selectable = False
            if m in selected:
                selected.remove(m)
                selectedCodes.remove(m.code)

    # not more than 3 of the following: (E, I1, M1-3, M23, D16)
    restrictedModules = ["4E1", "4E3", "4E5", "4E6", "4E11", "4E12", "4I1", "4I2", "4I3", "4M23", "4D16"]
    numberOfRestricted = 0

    for m in selectedCodes:  # Count the restricted already taken
        if m in restrictedModules:
            numberOfRestricted += 1

    if numberOfRestricted == 3:  # If at the limit disable the others
        for m in modules:
            if m.code in restrictedModules and m not in selected:
                m.selectable = False

    # Two E modules in total across the two years
    EsNeeded = 2

    for m in thirdYearSelected:
        if m[1] == "E" or m == "4D16":
            EsNeeded -= 1

    for m in selectedCodes:
        if m[1] == "E" or m == "4D16" or m == "4I1":
            EsNeeded -= 1

    if len(selected) >= 8-EsNeeded:  # At this point Es must be taken to create valid selection
        for m in modules:
            if m.code[1] != "E" and m.code != "4D16" and m.code != "4I1" and m not in selected:
                m.selectable = False


def checkQualifications():

    for a in areas:
        modulesDone = 0  # Count of relevant modules done
        a.qualified = False  # Assume nit qualified

        if a.name == "Aerospace and Aerothermal Engineering":
            coreModules = ["4A2", "4A3", "4A4", "4A7", "4A9", "4A10", "4A12", "4A13", "4A15"]
            coreModulesDone = 0
            companionModules = ["4B13", "4B23", "4B24", "4C2", "4C4", "4C5", "4C6", "4C7", "4C9", "4F1", "4F2", "4F3", "4M24"]
            companionModulesDone = 0

            for m in coreModules:  # Counts core modules
                if m in selectedCodes:
                    coreModulesDone += 1

            for m in companionModules:  # Counts companion modules
                if m in selectedCodes:
                    companionModulesDone += 1

            if coreModulesDone >= 4 or (coreModulesDone >= 3 and companionModulesDone >= 2):
                a.qualified = True

        elif a.name == "Bioengineering":
            gmodules = ["4G1", "4G3", "4G6", "4G7", "4G9", "4G10", "4I14"]
            gmodulesDone = 0

            for m in a.modules:  # Counts relevant modules
                if m in selectedCodes:
                    modulesDone += 1

            for m in gmodules:  # Counts G modules
                if m in selectedCodes:
                    gmodulesDone += 1

            if modulesDone >= 4 and gmodulesDone >= 2:
                a.qualified = True

        else:
            if a.name == "Electrical and Information Sciences":
                limit = 6
            else:
                limit = 4

            for m in a.modules:
                if m in selectedCodes:
                    modulesDone += 1

            if modulesDone >= limit:
                a.qualified = True


def refresh():
    # Updates the GUI at every state change

    # Third year modules
    for i in range(len(window.thirdYearButtons)):
        if window.thirdYearButtons[i]["text"] in thirdYearSelected:
            window.thirdYearButtons[i].config(style="Selected.TButton")
        else:
            window.thirdYearButtons[i].config(style="TButton")

    # Groups
    for i in range(len(window.groupButtons)):
        if window.groupButtons[i]["text"] == selectedGroup:
            window.groupButtons[i].config(style="Selected.TButton")
        else:
            window.groupButtons[i].config(style="TButton")

    # Fourth year modules
    checkSelectability()
    initializeButtons()

    for i in range(len(window.fourthYearButtons)):

        # colour in the selected buttons
        code = window.fourthYearButtons[i]["text"][:4]
        if code[3] == " ":
            code = code[:3]  # This is disgusting

        if code in selectedCodes and code in selectedArea.modules:
            window.fourthYearButtons[i].config(style="SelectedAndHighlighted.TButton")
        elif code in selectedCodes:
            window.fourthYearButtons[i].config(style="Selected.TButton")
        elif code in selectedArea.modules:
            window.fourthYearButtons[i].config(style="Highlighted.TButton")
        else:
            window.fourthYearButtons[i].config(style="TButton")

    checkQualifications()

    # Engineering areas
    qualified = []
    for a in areas:
        if a.qualified:
            qualified.append(a.name)

    for i in range(len(window.areaButtons)):
        if window.areaButtons[i]["text"] in qualified and window.areaButtons[i]["text"] == selectedArea.name:
            window.areaButtons[i].config(style="SelectedAndHighlighted.TButton")
        elif window.areaButtons[i]["text"] in qualified:
            window.areaButtons[i].config(style="Selected.TButton")
        elif window.areaButtons[i]["text"] == selectedArea.name:
            window.areaButtons[i].config(style="Highlighted.TButton")
        else:
            window.areaButtons[i].config(style="TButton")

    rule.config(text=selectedArea.rule, aspect=800)  # Display the selected rule

    # Summary box

    # Chosen modules
    selectedCodesDynamic.config(text=", ".join(selectedCodes))

    # mich/lent modules
    mich = 0
    lent = 0

    for m in selected:
        if m.set[0] == "M":
            mich += 1
        else:
            lent += 1

    michelmasModulesDynamic.config(text=mich)
    lentModulesDynamic.config(text=lent)

    # useful modules not taken
    allUsefuls = set()
    missingUsefuls = []
    for m in selected:
        if m.useful != "":
            for useful in m.useful:
                allUsefuls.add(useful)

    allUsefuls = list(allUsefuls)

    for u in allUsefuls:
        if u not in thirdYearSelected and u not in selectedCodes:
            missingUsefuls.append(u)

    usefulMissingDynamic.config(text=", ".join(missingUsefuls))

    # Number of exams
    exams = 0

    for m in selected:
        if "E" in m.assessment:
            exams += 1

    numberOfExamsDynamic.config(text=exams)


# To store the imported data
modules = list()
areas = list()
thirdYearModules = list()

# Variables to store the current state
selected = list()  # The 4th year modules that are selected
selectedCodes = list()  # The codes of the selected 4th year modules
thirdYearSelected = list()  # The 3rd year modules selected (codes only)
selectedGroup = ""  # The currently shown group
selectedArea = area("", "", [])  # The current engineering area

importer()  # Read the two module and the area csv files


window = Tk()

# Variables to store the buttons
window.thirdYearButtons = []
window.groupButtons = []
window.fourthYearButtons = []
window.areaButtons = []

# Module info box
moduleCodeDynamic = Label(window)
moduleTitleDynamic = Label(window)
moduleSetDynamic = Label(window)
moduleAssumedDynamic = Label(window)
moduleUsefulDynamic = Label(window)
moduleAssessmentDynamic = Label(window)

# Summary box
selectedCodesDynamic = Label(window)
michelmasModulesDynamic = Label(window)
lentModulesDynamic = Label(window)
usefulMissingDynamic = Label(window)
numberOfExamsDynamic = Label(window)

# Engineering area qulifying rule
rule = Message(window)

# Create the GUI
initializeStatic()
initialize3rdyearModules()
initializeGroups()
initializeAreas()

refresh()  # Required to apply the initial constraints and create the 4th year buttons

window.mainloop()
