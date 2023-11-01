import os
import platform
import shutil
import sys
import tkinter.font
from tkinter import Tk, PhotoImage, Label, Entry, Button, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD


class simple_file_move:
    def __init__(self):
        self.window = Tk()
        self.source_path = ""
        self.company_name = tkinter.StringVar()
        self.product_name = tkinter.StringVar()
        self.serial_number = tkinter.StringVar()
        self.target_dir = ""
        self.target_path = ""
        self.submit_result = tkinter.StringVar()

    def run(self):
        font = tkinter.font.Font(size=15)

        # 설정값 지정
        self.window.title("간편 파일 이동")
        self.window.geometry("600x500+100+100")
        self.window.resizable(False, False)
        self.window.configure(bg="white")

        # 로고
        photo = PhotoImage(file=self.resource_path("resource/logo.png"))
        logo = Label(self.window, image=photo, borderwidth=0)
        logo.place(x=0, y=5)

        # 회사명
        company_name = Label(self.window, text='회사 명', font=font, bg="white", anchor="w")
        company_name.place(x=110, y=160, width=130, height=30)

        company_input = Entry(self.window, textvariable=self.company_name, font=font, bg="white", bd=1,
                             highlightbackground="white",
                             highlightcolor="blue")
        company_input.place(x=260, y=160, width=250, height=30)

        # 제품명
        product_name = Label(self.window, text='제품 명', font=font, bg="white", anchor="w")
        product_name.place(x=110, y=200, width=130, height=30)

        product_input = Entry(self.window, textvariable=self.product_name, font=font, bg="white", bd=1,
                             highlightbackground="white",
                             highlightcolor="blue")
        product_input.place(x=260, y=200, width=250, height=30)

        # 시리얼번호
        serial_number = Label(self.window, text="시리얼 번호", font=font, bg="white", anchor="w")
        serial_number.place(x=110, y=240, width=130, height=30)

        serial_number_input = Entry(self.window, textvariable=self.serial_number, font=font, bg="white", bd=1,
                                  highlightbackground="white", highlightcolor="blue")
        serial_number_input.place(x=260, y=240, width=250, height=30)

        # 첨부 파일 선택
        input_file_label = Label(self.window, text="첨부 파일", font=font, bg="white", anchor="w")
        input_file_label.place(x=110, y=280, width=130, height=30)

        input_file_btn = tkinter.Button(self.window, text='파일 찾기', font=12, command=self.file_select, bd=1,
                                      highlightbackground="white")
        input_file_btn.place(x=260, y=280, width=250, height=30)

        # 저장 할 곳 위치
        target_path_label = Label(self.window, text="저장 폴더", font=font, bg="white", anchor="w")
        target_path_label.place(x=110, y=320, width=130, height=30)

        target_path_btn = tkinter.Button(self.window, text='폴더 선택', font=12, command=self.folder_select, bd=1,
                                       highlightbackground="white")
        target_path_btn.place(x=260, y=320, width=250, height=30)

        # 결과
        submit_result = Label(self.window, textvariable=self.submit_result, text="", font=font, bg="white", anchor="w")
        submit_result.place(x=110, y=400, width=300, height=30)

        submit = Button(self.window, text="확인", command=self.file_move, bd=1, highlightbackground="white")
        submit.place(x=450, y=360, width=60, height=30)

        self.window.mainloop()

    # 파일 선택 로직
    def file_select(self):
        self.window.file = filedialog.askopenfile(parent=self.window, title='파일을 선택해주세요.')
        if hasattr(self.window.file, 'name'):
            self.source_path = self.window.file.name
            self.window.file.close()
        else:
            self.source_path = ''

    # 폴더 선택 로직
    def folder_select(self):
        target_dir = filedialog.askdirectory(parent=self.window, title='폴더를 선택해주세요.', initialdir="/")
        self.move_path_set(target_dir)

    # 저장 경로 재정의
    def move_path_set(self, target_dir):
        if target_dir == '':
            return

        if platform.system() == 'windows':
            separator = '\\'
        else:
            separator = '/'
        target_path_split = self.source_path.split(separator)
        fileName = target_path_split[-1]
        self.target_dir = f"{target_dir}{separator}{self.company_name.get()}{separator}{self.product_name.get()}{separator}{self.serial_number.get()}"
        self.target_path = f"{self.target_dir}{separator}{fileName}"

    # 파일 이동 로직
    def file_move(self):
        if self.target_path == '':
            self.result_message('저장 폴더 위치를 먼저 선택해주세요.')
            return
        elif self.source_path == '':
            self.result_message('첨부 파일을 먼저 선택해주세요.')
            return

        # 저장 경로 존재 여부 확인 및 없으면 생성
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

        # 파일 이동
        shutil.move(self.source_path, self.target_path)

        # 이동 성공 여부 확인
        if os.path.exists(self.target_path):
            self.result_message('성공')
        else:
            self.result_message('실패')

    # 리소스 위치 변경
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # 결과 메시지 출력
    def result_message(self, message):
        if message == '' or message == None:
            self.submit_result.set('오류')
        else:
            self.submit_result.set(message)


if __name__ == '__main__':
    simple_file_move = simple_file_move()
    simple_file_move.run()
