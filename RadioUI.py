import tkinter as tk
import tkinter.ttk as ttk
import platform
import re
if platform.system() == 'Darwin':
    from tkmacosx import Button
    gLeftButton = '<ButtonRelease-2>'
else:
    Button = tk.Button
    gLeftButton = '<ButtonRelease-3>'
import copy

class RadioUI:
    root = None
    contest = None
    contest_msg = [{"label":"Call", "column": 0, "width": 15}, 
                   {"label":"Serial#", "column": 1, "width": 6},
                   {"label":"Received", "column": 2, "width": 20}]
    
    run_functions = [
                    {"label":"F1", "column": 0, "row":0, "width": 15}, 
                    {"label":"F2", "column": 1, "row":0, "width": 15},
                    {"label":"F3", "column": 2, "row":0, "width": 15}, 
                    {"label":"F4", "column": 3, "row":0, "width": 15},
                    {"label":"F5", "column": 4, "row":0, "width": 15}, 
                    {"label":"F6", "column": 5, "row":0, "width": 15},
                    {"label":"F7", "column": 0, "row":1, "width": 15}, 
                    {"label":"F8", "column": 1, "row":1, "width": 15},
                    {"label":"F9", "column": 2, "row":1, "width": 15}, 
                    {"label":"F10", "column": 3, "row":1, "width": 15},
                    {"label":"F11", "column": 4, "row":1, "width": 15}, 
                    {"label":"F12", "column": 5, "row":1, "width": 15}]
    sp_functions = copy.deepcopy(run_functions)

    macros_ = {"MYCALL":"NU6N"}

    def __init__(self, title, contest, size="650x250"):
        if RadioUI.root is None:
            RadioUI.root = tk.Tk()
            self.window = RadioUI.root
            RadioUI.contest = contest
        else:
            self.window = tk.Toplevel(RadioUI.root)
        self.window.title("SO2Runner: " + title)
        self.window.geometry(size)
        self.read_functions_file()
        print(RadioUI.run_functions)
        self.running_ = tk.BooleanVar(value=True)
        self.functions_ = RadioUI.run_functions
        self.create_layout()
        
    def get_window(self):
        return self.window
    
    def create_layout(self):
        #inputs
        input_fame = ttk.Frame()
        input_fame.grid(column=0, padx=3, pady=10)
        self.inputs = []
        for element in RadioUI.contest_msg:
            width = element['width']
            col = element['column']
            ttk.Label(input_fame, text=element["label"]).grid(column=col, row=0)
            entry = ttk.Entry(input_fame, width=width, font=("Helvetica", 20))
            entry.grid(column=col, row=1, padx=5, pady=5)
            self.inputs.append(entry)
        
        #Status
        status_frame = ttk.Frame()
        status_frame.grid(row=1, column=0, padx=3, pady=10)
        ttk.Radiobutton(status_frame, value=True, variable=self.running_, text="Run", command=self.update_state).grid(row=0, column=0, padx=5, pady=5)
        ttk.Radiobutton(status_frame, value=False, variable=self.running_, text="S&P", command=self.update_state).grid(row=0, column=1, padx=5, pady=5)

        # Functions
        func_frame = ttk.Frame()
        func_frame.grid(row=2, column=0, padx=3, pady=10)
        self.fbuttons_=[]
        for el in RadioUI.run_functions:
            col = el["column"]
            row = el["row"]
            label = el["label"]
            button = Button(func_frame, text=label, height=30, width=97)
            button.grid(column=col, row=row, padx=5, pady=5)
            self.fbuttons_.append(button)

    def update_state(self):
        if self.running_.get():
            self.functions_ = RadioUI.run_functions
        else:
            self.functions_ = RadioUI.sp_functions
        for button, func in zip(self.fbuttons_, self.functions_):
            button.config(text = func["label"])


    def read_functions_file(self):
        filename = "config/messages.mc"
        run_messages = True
        with open(file=filename) as f:
            ind = 0
            for line in f:
                if line.startswith('#'):
                    continue
                line = line.strip()
                line = self.parse_line(line).split(',')
                print(line)
                if run_messages:
                    RadioUI.run_functions[ind]["label"] = line[0]
                    RadioUI.run_functions[ind]["msg"] = line[1]
                else:
                    RadioUI.sp_functions[ind]["label"] = line[0]
                    RadioUI.sp_functions[ind]["msg"] = line[1] 
                ind += 1
                if ind > 11:
                    run_messages = False
                    ind = 0
                
    def parse_line(self, line):
        macros = re.findall(r'\{(.*?)\}', line)
        for macro in macros:
            if macro in RadioUI.macros_:
                line = line.replace('{' + macro + '}', RadioUI.macros_[macro])
            else:
                line = line.replace('{' + macro + '}', '')
        line = line.replace('*', RadioUI.macros_["MYCALL"])
        return line

if __name__ =='__main__':
    r = RadioUI(title="Radio 1", contest="ARRL10")
    root = r.get_window()
    root.mainloop()