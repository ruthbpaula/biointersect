# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 14:02:48 2021

@author: ruthb
"""

#### Programming project

# Part 1: Run intersection code

# It is not possible to properly install bedtools or pybedtools in a Windows machine. So I developed my own intersection
# code instead.

# IMPORTANT!!! For big input files: Sorting input files prior submission will make the program run faster.

import os
import sys
import pandas as pd
import numpy as np

def positionsAreOverlapping(position1, position2):
        if position2[left] <= position1[left] <= position2[right] or position2[left] <= position1[right] <= position2[right]:
                return True
        else:
                return False

def linesMatch(line_file1, line_file2):
        positions_file1 = [file1.iloc[line_file1, start_idx], file1.iloc[line_file1, end_idx]]
        positions_file2 = [file2.iloc[line_file2, start_idx], file2.iloc[line_file2, end_idx]]

        if file1.iloc[line_file1, chr_idx] == file2.iloc[line_file2, chr_idx]: # Match chromosome names
                if positionsAreOverlapping(positions_file1, positions_file2) or positionsAreOverlapping(positions_file2, positions_file1):
                        return True

def writeMatchToFile(line_file1, line_file2, output_file):
        # Match  pos:
        startMatch = max(file2.iloc[line_file2, start_idx], file1.iloc[line_file1, start_idx])
        endMatch = min(file2.iloc[line_file2, end_idx], file1.iloc[line_file1, end_idx])
        sizeMatch = (endMatch - startMatch) + 1
        # Prepare matchLine to write
        matchLine = str(file1.iloc[line_file1,0]) + "," + str(startMatch) + "," + str(endMatch) + "," + str(sizeMatch) + "," + str(file2.iloc[line_file2,3])
        # Write the matchLine
        output_file.write(matchLine)

arg1 = input("Input 1 name: ")
arg2 = input("Input 2 name: ")
arg3 = "output.csv"

file1 = pd.read_csv(arg1, delimiter = '\t', names = ['chr', 'start', 'end'])
file2 = pd.read_csv(arg2, delimiter = '\t', names = ['chr', 'start', 'end', 'gene'])
file2 = file2.sort_values(file2.columns[0])

output_file= open(arg3,"w")

chr_idx = 0
start_idx = 1
end_idx = 2

left = 0
right = 1

firstMatchFound = False
for line_file1 in range(0, (file1.shape[0])):
        for line_file2 in range(0, (file2.shape[0])):
                if linesMatch(line_file1, line_file2):
                        writeMatchToFile(line_file1, line_file2, output_file)
                        firstMatchFound = True
                        break

        if firstMatchFound:
                break

for line_file1 in range(1, (file1.shape[0])):
        for line_file2 in range(0, (file2.shape[0])):
                if file2.iloc[line_file2, chr_idx] > file1.iloc[line_file1, chr_idx]: # I can stop the search
                        break
                if linesMatch(line_file1, line_file2):
                        output_file.write("\n")
                        writeMatchToFile(line_file1, line_file2, output_file)

del file1
del file2
output_file.close()


## Part 2: Visualizing intersection table
### References:
# https://pyqtgraph.readthedocs.io/en/latest/
# https://github.com/hackstarsj/Python_GUI_Tkinter
# https://stackoverflow.com/questions/15416663/pyqt-populating-qtablewidget-with-csv-data

import csv
from PyQt5 import QtCore, QtGui, QtWidgets

class MyWindow(QtWidgets.QWidget):
    def __init__(self, fileName, parent=None):
        super(MyWindow, self).__init__(parent)
        self.fileName = fileName

        self.model = QtGui.QStandardItemModel(self)

        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        self.pushButtonLoad = QtWidgets.QPushButton(self)
        self.pushButtonLoad.setText("Load intersection table!")
        self.pushButtonLoad.clicked.connect(self.on_pushButtonLoad_clicked)

        self.pushButtonWrite = QtWidgets.QPushButton(self)
        self.pushButtonWrite.setText("Write modifications")
        self.pushButtonWrite.clicked.connect(self.on_pushButtonWrite_clicked)

        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.tableView)
        self.layoutVertical.addWidget(self.pushButtonLoad)
        self.layoutVertical.addWidget(self.pushButtonWrite)

    def loadCsv(self, fileName):
        with open(fileName, "r") as fileInput:
            for row in csv.reader(fileInput):
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]
                self.model.appendRow(items)

    def writeCsv(self, fileName):
        with open(fileName, "w") as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(self.model.rowCount()):
                fields = [
                    self.model.data(
                        self.model.index(rowNumber, columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    for columnNumber in range(self.model.columnCount())
                ]
                writer.writerow(fields)

    @QtCore.pyqtSlot()
    def on_pushButtonWrite_clicked(self):
        self.writeCsv(self.fileName)

    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        self.loadCsv(self.fileName)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Intersection table')

    # Intersection table
    main = MyWindow(arg3)
    main.show()

#    sys.exit(app.exec_())


## Part 3: Generating and visualizing Venn diagram + chr statistics barplot
### References:
# https://pyqtgraph.readthedocs.io/en/latest/
# https://github.com/hackstarsj/Python_GUI_Tkinter
# https://towardsdatascience.com/how-to-create-and-customize-venn-diagrams-in-python-263555527305
# https://www.geeksforgeeks.org/pyqt5-how-to-add-image-in-window/
# GUI class

import matplotlib
from matplotlib import pyplot as plt
from matplotlib_venn import venn2
from PIL import Image, ImageTk
import os

# Venn diagram

input1_only = abs(sum(1 for line in open(arg1)) - sum(1 for line in open(arg3)))
input2_only = abs(sum(1 for line in open(arg2)) - sum(1 for line in open(arg3)))
intersection_only = sum(1 for line in open(arg3))

plt.figure(1)

venn_output = venn2(subsets=(input1_only, input2_only, intersection_only), set_labels=('Input 1', 'Input 2'), set_colors=('purple', 'skyblue'), alpha = 0.7)
plt.title("Coordinates intersection");
plt.savefig('venn.png')

# Barplot

output_file = pd.read_csv(arg3)

chrom_names = ('chr01', 'chr02', 'chr03', 'chr04', 'chr05', 'chr06', 'chr07', 'chr08', 'chr09', 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chr22', 'chr23', 'chr24')
chrom_counts = []

for i in chrom_names:
    calc = len(output_file[output_file.iloc[:,0].str.contains( i )])
    chrom_counts.append(calc)

plt.figure(2)

height = chrom_counts
bars = chrom_names
x_pos = np.arange(len(bars))

plt.bar(x_pos, height, color=(0.2, 0.4, 0.6, 0.6))
plt.xticks(x_pos, bars, rotation = 'vertical')
plt.ylabel('Number of intersections per chromosome')

plt.savefig('barplot.png')

# Displaying both graphs in new windows

plt.show()
