from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn.model_selection import train_test_split
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyInstaller.utils.hooks import collect_submodules
hiddenimports = collect_submodules('sklearn')

# inialisasi  GUI pada tkinter
root = tk.Tk()

root.geometry("500x500")  # menentuka  dimensi root (lebar window)
root.pack_propagate(False)
root.resizable(0, 0)
tk.messagebox.showinfo(
    "Informasi", "Pastikan data memiliki kolom 'UnixTimeStamp' dan 'price'")

# Frame data
frame1 = tk.LabelFrame(root, text="Data Ethereum")
frame1.place(height=250, width=500)

# Frame untuk membuka file
file_frame = tk.LabelFrame(root, text="Pilih File")
file_frame.place(height=100, width=400, rely=0.65, relx=0)

# Tombol
button1 = tk.Button(file_frame, text="Cari File",
                    command=lambda: File_dialog())
button1.place(rely=0.65, relx=0.50)

button2 = tk.Button(file_frame, text="Buka File",
                    command=lambda: Load_excel_data())
button2.place(rely=0.65, relx=0.30)

#  file/file path text
label_file = ttk.Label(file_frame, text="No File Selected")
label_file.place(rely=0, relx=0)


tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1)
treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview)
treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview)
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
treescrollx.pack(side="bottom", fill="x")
treescrolly.pack(side="right", fill="y")


def File_dialog():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("xlsx files", "*.xlsx"), ("All Files", "*.*")))
    label_file["text"] = filename
    return None


def Load_excel_data():
    file_path = label_file["text"]
    try:
        excel_filename = r"{}".format(file_path)
        if excel_filename[-4:] == ".csv":
            df = pd.read_csv(excel_filename)
            x = df.loc[:, 'UnixTimeStamp'].values
            y = df.loc[:, 'Price'].values
            print(df.describe())

            x_train, x_test, y_train, y_test =\
                train_test_split(x, y, test_size=0.2, random_state=0)
            x_train = x_train.reshape(-1, 1)
            regressor = LinearRegression()
            regressor.fit(x_train, y_train)

            print('Coefficients: ', regressor.coef_)
            print('Intercept: ', regressor.intercept_)

            m = regressor.coef_ / regressor.intercept_

            if (m == 0):
                print("ethreum tidak liqud  tidak disarankan melakukan transaksi")

            if (m < 0):
                tk.messagebox.showinfo(
                    "Rekomendasi", "harga ethreum turun lakukan transaksi pembelian")
                print("harga ethreum turun lakukan transaksi pembelian")

            if (m > 0):
                tk.messagebox.showinfo(
                    "Rekomendasi", "harga ethreum naik lakukan transaksi penjualan")
                print("harga ethreum naik lakukan transaksi penjualan")
            plt.scatter(x_train, y_train)
            plt.plot(x_train, regressor.predict(x_train), color='red')
            plt.title("perdiksi ehtreum")
            plt.xlabel("Waktu")
            plt.ylabel("harga")
            plt.show()

        else:
            df = pd.read_excel(excel_filename)

    except ValueError:
        tk.messagebox.showerror(
            "Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information", f"No such file as {file_path}")
        return None

    clear_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column)

    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        tv1.insert("", "end", values=row)
    return None


def clear_data():
    tv1.delete(*tv1.get_children())
    return None


root.mainloop()
