"""
Author: Kostas Zoumpatianos
File: gui.py
Description: Gui experiments..... not good.... looks like #@$@#$@#%.... :S
Date: March, 6 2010
"""
"""
from Tkinter import *
import sys

from id3 import ID3
from utils.dataset import DataSet



def calculate_branch_depth(elements):
    depth = 1
    for element in elements:
        if(type(element) != dict):
            if(len(element)!=3):
                depth += calculate_branch_depth(element[1])
    return depth


def draw_vertical(dataset, elements, canvas, x=0, y=0):
    #w.create_line(x, y, 200, 100)
    for element in elements:
        x = x + 100
        canvas.create_line(x, y, x, y+100, fill="red", dash=(4, 4))
        if(len(element)!=3):
            draw_vertical(dataset, element[1],canvas, x+100, y+100)
        else:
            pass
            
        
def draw(dataset, elements, canvas, x, y, spread, size_of_labels=100):
    #w.create_line(x, y, 200, 100)
    initial_y = y
    initial_x = x
    for element in elements:
        
        canvas.create_line(x, initial_y, x+100, y, fill="red", dash=(4, 4))
        canvas.create_rectangle(x+100, y-15, x+100+size_of_labels, y+15 )
        canvas.create_text(x+(200+size_of_labels)/2, y, text="%s = %s" % (dataset.fields[element[0][0]]["name"], element[0][1] ))
        if(len(element)!=3):
            draw(dataset, element[1],canvas,x+100+size_of_labels,y,spread/len(element[1]), size_of_labels)
        else:
            canvas.create_text(x+(200+size_of_labels)-50, y,text=str(element[2][0]))
        y += spread
            
            
        

        
def visualize(id3_instance):
    master = Tk()
    frame = Frame(master, bd=2, relief=SUNKEN)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
    xscrollbar.grid(row=1, column=0, sticky=E+W)

    yscrollbar = Scrollbar(frame)
    yscrollbar.grid(row=0, column=1, sticky=N+S)

    canvas = Canvas(frame, bd=0, scrollregion=(0, 0, 10000, 10000),
                    xscrollcommand=xscrollbar.set,
                    yscrollcommand=yscrollbar.set)
                    
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    
    xscrollbar.config(command=canvas.xview)
    yscrollbar.config(command=canvas.yview)
    
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.pack(fill=BOTH,expand=1)
    
    tree = id3_instance.tree
    #draw(dataset = dataset, elements = tree, canvas = canvas, 
    #        spread = 1000, x = 10, y = 20,size_of_labels = 200)
    draw_vertical(dataset = dataset, elements = tree, canvas = canvas)
    mainloop()


        
def create_view(id3_instance):
    pass
    


if __name__ == "__main__":
    
    dataset = DataSet(sys.argv[1], sys.argv[2])
    target_attribute = 2 # First from the end, i.e. the last one
    id3_instance = ID3(dataset, target_attribute)
    id3_instance.train()
    id3_instance.print_tree()
    #visualize(id3_instance)
    
"""