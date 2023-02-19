import tkinter as tk 
from tkinter import *
from tkinter import filedialog, messagebox
import pandas as pd
import webbrowser
import pyperclip
import subprocess
import sys
import os


# Functions to control the CSV to UWP ready file
    
def remove_columns():
    global df
    # Define the columns to keep and the new column names
    columns_to_keep = ["First Name", "Surname", "Member Number", "Address - Home - Line 1",
                       "Address - Home - Line 2", "Address - Home - Line 3",
                       "Address - Home - Line 4", "Address - Home PC", "Employer Name",
                       "Employer", "Workplace Name", "Workplace", "Region",
                       "Job Description ", "Email Address", "Allow Email", "Allow Phone",
                       "Allow SMS", "Home phone", "Mobile phone", "TPS Flag"]
    new_column_names = {"First Name": "FirstName", "Surname": "LastName", "Member Number": "MembershipNumber",
                        "Address - Home - Line 1": "HomeAddress1", "Address - Home - Line 2": "HomeAddress2",
                        "Address - Home - Line 3": "HomeAddress3", "Address - Home - Line 4": "HomeAddress4",
                        "Address - Home PC": "HomeAddressPostcode", "Employer Name": "EmployerName",
                        "Employer": "EmployerCode", "Workplace Name": "WorkplaceName", "Workplace": "WorkplaceCode",
                        "Region": "Region", "Job Description ": "JobTitle", "Email Address": "EmailAddress",
                        "Allow Email": "AllowEmail", "Allow Phone": "AllowPhone", "Allow SMS": "AllowSms",
                        "Home phone": "HomePhone", "Mobile phone": "MobilePhone", "TPS Flag": "TPS"}
    # Remove all other columns and rename the remaining ones
    df = df[columns_to_keep]
    df = df.rename(columns=new_column_names)

def select_file():
    global df
    # Open a file dialog
    filepath = filedialog.askopenfilename()
    # Read the selected file into a DataFrame
    try:
        df = pd.read_csv(filepath)
    except pd.errors.EmptyDataError:
        # Handle missing headers
        response = messagebox.askyesno(
            "Missing Headers", "File is missing headers. Do you want to continue?")
        if response:
            df = pd.read_csv(filepath, header=None)
        else:
            return
    if 'Member Number' in df.columns:
        # Remove unwanted columns
        remove_columns()
    else:
        response = messagebox.askokcancel(
            "Error", "The file selected does not contain the column 'Member Number'. Do you want to continue?")
        if response:
            remove_columns()
        else:
            return
    # Open a file dialog to select a save location
    filepath = filedialog.asksaveasfilename(defaultextension=".csv")
    # Save the DataFrame to the selected location
    df.to_csv(filepath, index=False)
    # Inform the user which file has been selected
    messagebox.showinfo("File Selected", f"The file '{filepath}' has been converted and saved.")
    

###  Functions to control the dividing a CSV file via the Workplace Column
def workplacedivide():
    # Prompt the user to select the input file
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])

    # Load the file into a pandas dataframe
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        raise ValueError("File type not supported")

    # Get the unique values in the "workplace_name" column
    unique_codes = df["Workplace Name"].unique()

    # Ask the user where to save the new files
    save_path = filedialog.askdirectory()

    # Iterate through the unique code names and create a new dataframe
    # for each one that contains all rows with that code name
    for code in unique_codes:
        code_df = df[df["Workplace Name"] == code]
        # Save the new dataframe in a file with the unique code name as the file name
        file_name = f"{code}.xlsx" if file_path.endswith('.xlsx') else f"{code}.csv"
        code_df.to_excel(os.path.join(save_path, file_name), index=False) if file_path.endswith('.xlsx') else code_df.to_csv(os.path.join(save_path, file_name), index=False)
  
   
   
        
def SMS_only():
     # Prompt the user to select the input file
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])

    # Load the file into a pandas dataframe
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        raise ValueError("File type not supported")
    
    # Add any "Home phone" rows starting with "07" or "7" to "Mobile phone"
    df.loc[df["Home phone"].notna() & df["Home phone"].str.startswith(("07", "7")), "Mobile phone"] = df["Home phone"]
    
    # Keep rows where "Allow SMS" is "Y"
    df = df.loc[df["Allow SMS"] == "Y"]

    # Remove empty rows from the "Mobile phone" column
    df = df.dropna(subset=["Mobile phone"])

    # Keep only the "Allow SMS" and "Mobile phone" columns
    df = df[["Member Number", "First Name", "Surname","Allow SMS", "Mobile phone"]]

    # Prompt the user to select where to save the modified file
    save_path = filedialog.asksaveasfilename(defaultextension=".csv")

    # Save the modified dataframe to the selected file path
    df.to_csv(save_path, index=False)

    # Open the saved file
    os.system(f'open "{save_path}"')

    # Print a message to indicate the file has been saved and opened
    print(f"File saved and opened: {save_path}")


def open_urlbuilder():
    subprocess.call(["python", "urlbuilder.py"])
    pass

root = tk.Tk()

# Application Settings
root.geometry("500x330")
root.title("Unite Ballot Toolbox")



# create a menu bar
menu_bar = tk.Menu(root)
# create a links menu
links_menu = tk.Menu(menu_bar, tearoff=0)
links_menu.add_command(label="Login", command=lambda: webbrowser.open_new("https://surveys.unitetheunion.org"))
links_menu.add_command(label="New Core Jotform", command=lambda: webbrowser.open_new("https://surveys.unitetheunion.org/form-templates/standalone/ur/core-form"))
# add the links menu to the menu bar
menu_bar.add_cascade(label="Jotform", menu=links_menu)
# associate the menu bar with the root window
root.config(menu=menu_bar)




# GUI START
label = tk.Label(root, text="Tools")
label.grid(column=0, row=2, sticky="w", padx=5, pady=5)

urlbuilderbutton = tk.Button(root, text="URL Builder", command=open_urlbuilder)
urlbuilderbutton.grid(column=0, row=3, sticky="w", padx=5, pady=5)


# CSV Labels
csv_label = tk.Label(root, text="CSV Tools")
csv_label.grid(column=0, row=4, sticky="w", padx=5, pady=5)

# CSV Tools = CSV 2 Unite Wrangling Platfomr
uwp_to_csv = tk.Button(root, text="CSV 2 UWP", command=select_file)
uwp_to_csv.grid(column=0, row=5, sticky="w", padx=5, pady=5)

# CSV Tools = CSV 2 SMS List
sms_to_csv = tk.Button(root, text="CSV 2 SMS List", command=SMS_only)
sms_to_csv.grid(column=1, row=5, sticky="w", padx=5, pady=5)

# CSV Tools = CSV 2 Unite Wrangling Platfomr
csv_to_workplacedivide = tk.Button(root, text="CSV 2 SMS List", command=workplacedivide)
csv_to_workplacedivide.grid(column=2, row=5, sticky="w", padx=5, pady=5)




root.mainloop()
