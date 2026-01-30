# Script to open and read a .dpt file using QDPTconverter
import os
import numpy as np
from csv import writer
import tkinter as tk
from tkinter import filedialog


class DPTConverter:
    '''class to read and convert .dpt files'''
    def __init__(self, dpt_file, output_dir):
        self.dpt_file = dpt_file
        self.output_dir = output_dir

    def convert(self) -> np.ndarray:
        '''parse .dpt file and return data as numpy array'''
        if not os.path.isfile(self.dpt_file):
            raise FileNotFoundError(f"File not found: {self.dpt_file}")

        if not os.path.isdir(self.output_dir):
            raise NotADirectoryError(f"Directory not found: {self.output_dir}")

        for delim in [',', '\t', ' ']:
            try:
                data = np.loadtxt(self.dpt_file, delimiter=delim)
                return data
            except ValueError:
                continue

        return data

    def store_data(self, data: np.ndarray):
        # store data one spectrum at a time
        # x-values are in first column, y-values in the other columns
        x_vals = [float(row[0]) for row in data]
        num_spectra = len(data[0]) - 1  # excluding x-values

        for spec_idx in range(num_spectra):
            # use file name of dpt file for output files
            output_name = (f'{os.path.basename(self.dpt_file)}_'
                           f'{spec_idx + 1}.csv')
            output_file = os.path.join(self.output_dir, output_name)

            # slice out y-values for current spectrum
            y_vals = data[:, spec_idx + 1]

            with open(output_file, 'w', newline='') as outfile:
                csv_writer = writer(outfile)
                for i, x_val in enumerate(x_vals):
                    csv_writer.writerow([x_val, y_vals[i]])

        print(f'Stored {num_spectra} spectra to {self.output_dir}')


if __name__ == "__main__":
    # for debugging:
    # dpt_file = r"C:\Users\speicl\Downloads\REG MUR219 better line scan.0.dpt"
    # output_dir = r"C:\Users\speicl\Downloads\test"

    # GUI to select .dpt file and target directory
    root = tk.Tk()
    root.withdraw()
    dpt_file = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Select .dpt file to convert",
        filetypes=[("DPT files", "*.dpt")]
        )

    # wait here until file is selected
    dpt_dir = os.path.dirname(dpt_file)

    output_dir = filedialog.askdirectory(
        initialdir=dpt_dir,
        title="Select target directory"
        )

    # convert and store data
    converter = DPTConverter(dpt_file, output_dir)
    spectra = converter.convert()
    converter.store_data(spectra)
