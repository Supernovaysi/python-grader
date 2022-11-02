import subprocess
import tkinter
from tkinter import *
from tkinter import ttk
import os
import tkinter.filedialog
from openpyxl import Workbook

def set_progress(now, total):
    progressbar_value.set(now / total * 100)
    progressbar.update()

def save_xl(result_datas, problems_dir):
    problems_dir_name = parse_dir(problems_dir)

    write_wb = Workbook()
    write_ws = write_wb.active

    for data in result_datas:
        write_ws.append(data)

    write_wb.save(problems_dir + "/" + problems_dir_name + ".xlsx")

def set_text_box(s: str):
    text.configure(state="normal")
    text.insert(tkinter.END, s + "\n")
    text.configure(state="disabled")

def parse_dir(s: str) -> str:
    return s.split("/")[-1]

def browse_filedialog():
    file_path = tkinter.filedialog.askdirectory(initialdir="./")
    combo_box_dir.set(parse_dir(file_path))
    print(file_path)

def get_answer_str(problem_number: int, problem_dir: str) -> str:
    os.chdir(root_path + "/" + "answer")
    f = open(str(problem_number) + ".py.txt")
    answer_str = f.read().strip()
    f.close()
    os.chdir(problem_dir)
    return answer_str

def compare_submit_to_answer(submit: str, answer: str):
    submit = submit.strip()
    answer = answer.strip()
    return submit == answer

def run_judge():
    set_text_box("채점 중...")
    cur_path_abs = os.path.abspath("./")
    print(cur_path_abs)

    judge_dir = combo_box_dir.get()
    problems_dir = cur_path_abs + "/" + judge_dir

    judge_file_list = os.listdir(problems_dir)
    judge_file_list_py = [file for file in judge_file_list if file.endswith(".py")]
    os.chdir(problems_dir)
    print(judge_file_list_py)

    problem_num = int(combo_box_problem.get().split(" ")[-1])
    problem_ans = get_answer_str(problem_num, problems_dir)

    result_datas = []

    for py_file in judge_file_list_py:
        out = subprocess.check_output([py_file], shell=True, encoding='utf-8')
        result = compare_submit_to_answer(out, problem_ans)
        result_datas.append([py_file, result])
        set_progress(judge_file_list_py.index(py_file) + 1, len(judge_file_list_py))
        print(result)

    save_xl(result_datas, problems_dir)
    os.chdir(cur_path_abs)
    set_text_box("{}개 파일 채점 완료".format(len(judge_file_list_py)))


######## main ########
# run 'pyinstaller -w -F main.py' to create main.exe file
problem_list = []
for i in range(1,11):
    problem_list.append("별 찍기 " + str(i))

root_path = os.path.abspath(".")
path = "./"
total_dir = os.listdir(path)
total_dir = list(filter(lambda item: item.find(".") == -1, total_dir))

subprocess.call(['chcp','65001'], shell=True)

window = Tk()

window.title("채점 프로그램")
window.geometry("600x450+100+100")
window.resizable(False, False)

combo_box_dir = ttk.Combobox(window, height=15, values=total_dir, state="readonly")
combo_box_dir.pack()
combo_box_dir.set("폴더 선택")

button_dir = Button(window, text="폴더 선택", overrelief="solid", width=7, command=browse_filedialog, repeatdelay=1000, repeatinterval=100)
button_dir.place(x=385, y=0)

combo_box_problem = ttk.Combobox(window, height=15, values=problem_list, state="readonly")
combo_box_problem.pack()
combo_box_problem.set("문제 선택")

text=tkinter.Text(window)
text.insert(tkinter.CURRENT, "제출폴더와 문제번호를 선택하고 채점 버튼을 눌러주세요.\n")
text.pack()
text.configure(state="disabled")

progressbar_value = tkinter.DoubleVar()
progressbar = ttk.Progressbar(window, maximum=100, variable=progressbar_value)
progressbar.pack(fill="x", padx=20)

button = Button(window, text="채점", overrelief="solid", width=15, command=run_judge, repeatdelay=1000, repeatinterval=100)
button.pack(side='bottom', pady=10)

window.mainloop()


