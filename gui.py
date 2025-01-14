import os
import tkinter as tk  # standard widgets (Label, Button, etc.)
from tkinter import ttk  # for Combobox widget
from tkinter.messagebox import askokcancel, showinfo  # infoboxes
from tkinter.filedialog import askopenfilename, askdirectory  # select files or folders
import webbrowser  # open files or URLs from string-type directories
import sediment_transport as sed


class SediApp(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("Sedi App")
        #self.master.iconbitmap("Exercise-gui/graphs/icon.ico")
        ww = 628  # width
        wh = 382  # height
        # screen position
        wx = (self.master.winfo_screenwidth() - ww) / 2
        wy = (self.master.winfo_screenheight() - wh) / 2
        # assign geometry
        self.master.geometry("%dx%d+%d+%d" % (ww, wh, wx, wy))
        self.padx = 5
        self.pady = 5
        self.grain_file = "SELECT"
        self.grain_info = None  # will be a sed.GrainReader object when the user defined grains.csv
        self.hec_file = "SELECT"
        self.out_folder = "SELECT"
        # grain file button
        tk.Button(master, text="Select grain csv file", width=30,
                  command=lambda: self.set_grain_file()).grid(column=0, row=0,
                                                              padx=self.padx, pady=self.pady,
                                                              sticky=tk.W)

        # hec file button
        tk.Button(master, text="Select HEC-RAS data workbook", width=30,
                  command=lambda: self.set_hec_file()).grid(column=0, row=2,
                                                            padx=self.padx, pady=self.pady,
                                                            sticky=tk.W)

        # output folder button
        tk.Button(master, text="Select output folder", width=30,
                  command=lambda: self.select_out_directory()).grid(column=0, row=4,
                                                                    padx=self.padx, pady=self.pady,
                                                                    sticky=tk.W)
        self.b_run = tk.Button(master, bg="white", text="Compute", width=30,
                               command=lambda: self.run_program())
        self.b_run.grid(sticky=tk.W, row=7, column=0, padx=self.padx, pady=self.pady)
        self.grain_label = tk.Label(master, text="Grain file (csv): " + self.grain_file)
        self.grain_label.grid(column=0, columnspan=3, row=1, padx=self.padx, pady=self.pady, sticky=tk.W)
        self.hec_label = tk.Label(master, text="HEC-RAS data file (xlsx): " + self.hec_file)
        self.hec_label.grid(column=0, columnspan=3, row=3, padx=self.padx, pady=self.pady, sticky=tk.W)
        self.out_label = tk.Label(master, text="Output folder: " + self.out_folder)
        self.out_label.grid(column=0, columnspan=3, row=5, padx=self.padx, pady=self.pady, sticky=tk.W)
        self.run_label = tk.Label(master, fg="forest green", text="")
        self.run_label.grid(column=0, columnspan=3, row=8, padx=self.padx, pady=self.pady, sticky=tk.W)
        # Label for Combobox
        tk.Label(master, text="Select characteristic grain size:").grid(column=0, row=6, padx=self.padx, pady=self.pady, sticky=tk.W)
        # Combobox
        self.cbx_D_char = ttk.Combobox(master, width=5)
        self.cbx_D_char.grid(column=1, row=6, padx=self.padx, pady=self.pady, sticky=tk.W)
        self.cbx_D_char['state'] = 'disabled'
        self.cbx_D_char['values'] = [""]

    def select_file(self, description, file_type):
        return askopenfilename(filetypes=[(description, file_type)],
                               initialdir=os.path.abspath(""),
                               title="Select a %s file" % file_type,
                               parent=self)

    def set_grain_file(self):
        self.grain_file = self.select_file("grain file", "csv")
        try:
            self.grain_info = sed.GrainReader(self.grain_file)
        except OSError:
            showinfo("ERROR", "Could not open %s." % self.grain_file)
            self.grain_file = "SELECT"
            return -1

        # update grain label
        self.grain_label.config(text="Grain file (csv): " + self.grain_file)

        # update and enable combobox
        self.cbx_D_char['state'] = 'readonly'
        self.cbx_D_char['values'] = list(self.grain_info.size_classes.index)
        self.cbx_D_char.set('D84')

    def set_hec_file(self):
        self.hec_file = self.select_file("HEC-RAS output file", "xlsx")
        # update hec label
        self.hec_label.config(text="HEC-RAS output file (xlsx): " + self.hec_file)

    def select_out_directory(self):
        self.out_folder = askdirectory()
        # update output folder label
        self.out_label.config(text="Output folder: " + self.out_folder)

    def valid_selections(self):
        if "SELECT" in self.grain_file:
            showinfo("ERROR", "Select grain size file.")
            return False
        if "SELECT" in self.hec_file:
            showinfo("ERROR", "Select HEC-RAS output file.")
            return False
        if "SELECT" in self.out_folder:
            showinfo("ERROR", "Select output folder.")
            return False
        return True

    def run_program(self):
        # ensure that user selected all necessary inputs
        if not self.valid_selections():
            return -1

        # get selected characteristic grain size
        try:
            D_char = float(self.grain_info.size_classes["size"][str(self.cbx_D_char.get())])
        except ValueError:
            showinfo("ERROR", "The selected characteristic grain size is not correctly defined in the csv file (float?).")
            return -1
        if askokcancel("Start calculation?", "Click OK to start the calculation."):
            sed.main(D_char, self.hec_file, self.out_folder)
            self.b_run.config(fg="forest green")
            self.run_label.config(text="Success: Created %s" % str(self.out_folder + "/bed_load_mpm.xlsx"))
            webbrowser.open(self.out_folder + "/bed_load_mpm.xlsx")


if __name__ == '__main__':
    SediApp().mainloop()
