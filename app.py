import re, os, json, platform, shutil, sys, tkinter.font
from TkinterDnD2 import *
try:
    from Tkinter import *
    from Tkinter import filedialog
    from ScrolledText import ScrolledText
except ImportError:
    from tkinter import *
    from tkinter import filedialog
    from tkinter.scrolledtext import ScrolledText


class simple_file_move:
    def __init__(self):
        self.window = TkinterDnD.Tk()
        self.company_name = tkinter.StringVar()
        self.product_name = tkinter.StringVar()
        self.serial_number = tkinter.StringVar()
        self.target_dir = ""
        self.target_path_dic = {}
        self.submit_result = tkinter.StringVar()
        self.input_file_listbox = None
        self.input_file_list = []
        self.input_file_dic = {}
        self.separator = ''
        self.config = None

    def run(self):
        self.get_config()
        self.set_separator()

        # 설정값 지정
        font = tkinter.font.Font(size=15)
        self.window.title("간편 파일 이동")
        self.window.geometry("600x700+100+100")
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
        input_frame = Frame(self.window)
        input_frame.place(x=260, y=280, width=250, height=200)

        input_file_label = Label(self.window, text="첨부 파일", font=font, bg="white", anchor="w")
        input_file_label.place(x=110, y=280, width=130, height=30)

        self.input_file_listbox = tkinter.Listbox(input_frame, selectmode=tkinter.SINGLE, font=12, bd=1,
                                                  highlightbackground="white", highlightcolor="white",
                                                  activestyle="none")
        self.input_file_listbox.place(x=0, y=0, width="233", height="183")
        self.input_file_listbox.drop_target_register(DND_FILES)
        self.input_file_listbox.dnd_bind("<<Drop>>", self.files_drop)

        xscrollbar = Scrollbar(input_frame, orient="horizontal")
        xscrollbar.config(command=self.input_file_listbox.xview)
        xscrollbar.pack(side="bottom", fill="both")
        yscrollbar = Scrollbar(input_frame, orient="vertical")
        yscrollbar.config(command=self.input_file_listbox.yview)
        yscrollbar.pack(side="right", fill="both")
        self.input_file_listbox.config(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

        input_file_btn = tkinter.Button(self.window, text='파일을 선택하거나 드롭해주세요.', font=12, command=self.file_select,
                                        bd=1, highlightbackground="white")
        input_file_btn.place(x=260, y=490, width=250, height=30)

        # 저장 할 곳 위치
        target_path_label = Label(self.window, text="저장 폴더", font=font, bg="white", anchor="w")
        target_path_label.place(x=110, y=530, width=130, height=30)

        target_path_btn = tkinter.Button(self.window, text='폴더 선택', font=12, command=self.folder_select, bd=1,
                                         highlightbackground="white")
        target_path_btn.place(x=260, y=530, width=250, height=30)

        # 확인 버튼
        submit = Button(self.window, text="확인", command=self.file_move, bd=1, highlightbackground="white")
        submit.place(x=450, y=560, width=60, height=30)

        # 결과
        submit_result = Label(self.window, textvariable=self.submit_result, text="", font=font, bg="white", anchor="w")
        submit_result.place(x=110, y=600, width=300, height=30)

        self.window.mainloop()

    # OS 별 기본 경로 구분자 지정
    def set_separator(self):
        if platform.system() == 'windows':
            self.separator = '\\'
        else:
            self.separator = '/'

    # 파일 DND 로직
    def files_drop(self, event):
        temp_files_str = event.data.replace('{', '')
        temp_files_split = re.split(r'[},a-zA-Z0-9] ', temp_files_str)

        for file in temp_files_split:
            file = file[0:-1] + file[-1].replace('}', '')
            if file not in self.input_file_list:
                self.input_file_list.append(file)
                self.input_file_listbox.insert('end', file)

    # 파일 선택 로직
    def file_select(self):
        self.window.file = filedialog.askopenfiles(parent=self.window, title='파일을 선택해주세요.')
        for file in self.window.file:
            if hasattr(file, 'name'):
                if file.name not in self.input_file_list:
                    self.input_file_list.append(file.name)
                    self.input_file_listbox.insert('end', file.name)
                    file.close()

    # 폴더 선택 로직
    def folder_select(self):
        self.target_dir = filedialog.askdirectory(parent=self.window, title='폴더를 선택해주세요.', initialdir="/")

        # 저장 폴더 설정
        self.set_config(self.target_dir)

    # 저장 경로 재정의
    def move_path_set(self):
        # validation
        if self.company_name.get() == '':
            self.result_message('회사 명을 입력해주세요.')
            return False
        elif self.product_name.get() == '':
            self.result_message('제품 명을 입력해주세요.')
            return False
        elif self.serial_number.get() == '':
            self.result_message('시리얼 번호를 입력해주세요.')
            return False
        elif self.target_dir == '':
            self.result_message('저장 경로를 설정해주세요.')
            return False
        elif len(self.input_file_list) == 0:
            self.result_message('첨부 파일이 없습니다.')
            return False

        self.target_dir = f"{self.target_dir}{self.separator}{self.company_name.get()}{self.separator}{self.product_name.get()}{self.separator}{self.serial_number.get()}"

        for file in self.input_file_list:
            target_path_split = file.split(self.separator)
            fileName = target_path_split[-1]
            self.input_file_dic[fileName] = file
            self.target_path_dic[fileName] = f"{self.target_dir}{self.separator}{fileName}"

        return True

    # 파일 이동 로직
    def file_move(self):
        # 파일 이동 경로 설정
        if not self.move_path_set():
            return

        # 저장 경로 존재 여부 확인 및 없으면 생성
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

        # 파일 이동
        success_count = 0

        for key in self.input_file_dic.keys():
            if not os.path.exists(self.input_file_dic[key]):
                return

            shutil.move(self.input_file_dic[key], self.target_path_dic[key])
            if os.path.exists(self.target_path_dic[key]):
                success_count += 1

        # 이동 성공 여부 확인
        if success_count == len(self.input_file_dic.keys()):
            self.result_message('전체 성공')
        else:
            self.result_message(f"{success_count}건 성공")

        # 설정 값 초기화
        self.config_reset()

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

    # Json 인지 확인
    def is_json(self, obj):
        try:
            json_object = json.loads(obj)
            # { } 가 포함된 string이 invalid json 인 경우 Exception
            iterator = iter(json_object)
            # { } 가 없는 경우는 string의 경우 Exception
        except Exception as e:
            return False
        return True

    # config 호출
    def get_config(self):
        if not os.path.exists('./config.json'):
            return

        config_file = open(f"./config.json", "r")
        self.config = config_file.read()
        config_file.close()

        if self.is_json(self.config):
            self.config = json.loads(self.config)
            if 'target_dir' in self.config.keys():
                self.target_dir = self.config['target_dir']

    # config 설정
    def set_config(self, target_dir):
        if str(type(self.config)) not in 'dict':
            self.config = {}

        if 'target_dir' not in self.config.keys():
            self.config['target_dir'] = target_dir

        config_file = open("./config.json", "w+")
        config_file.write(json.dumps(self.config))
        config_file.close()

    # 시스템에 적용한 config 초기화
    def config_reset(self):
        self.target_dir = self.config['target_dir']
        self.target_path_dic = {}
        self.input_file_list = []
        self.input_file_dic = {}
        self.input_file_listbox.delete(0, END)


if __name__ == '__main__':
    simple_file_move = simple_file_move()
    simple_file_move.run()
