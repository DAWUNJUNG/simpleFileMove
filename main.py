import os
import platform
import shutil
import sys
import tkinter.font
from tkinter import *
from tkinter import filedialog


class SimpleFileMove:
    def __init__(self):
        self.window = Tk()
        self.sourcePath = ""
        self.companyName = tkinter.StringVar()
        self.productName = tkinter.StringVar()
        self.serialNumber = tkinter.StringVar()
        self.targetDir = ""
        self.targetPath = ""
        self.submitResult = tkinter.StringVar()

    def run(self):
        font = tkinter.font.Font(size=15)

        # 설정값 지정
        self.window.title("간편 파일 이동")
        self.window.geometry("600x500+100+100")
        self.window.resizable(False, False)
        self.window.configure(bg="white")

        # 로고
        photo = PhotoImage(file=self.resourcePath("resource/logo.png"))
        logo = Label(self.window, image=photo, borderwidth=0)
        logo.place(x=0, y=5)

        # 회사명
        companyName = Label(self.window, text='회사 명', font=font, bg="white", anchor="w")
        companyName.place(x=110, y=160, width=130, height=30)

        companyInput = Entry(self.window, textvariable=self.companyName, font=font, bg="white", bd=1,
                             highlightbackground="white",
                             highlightcolor="blue")
        companyInput.place(x=260, y=160, width=250, height=30)

        # 제품명
        productName = Label(self.window, text='제품 명', font=font, bg="white", anchor="w")
        productName.place(x=110, y=200, width=130, height=30)

        productInput = Entry(self.window, textvariable=self.productName, font=font, bg="white", bd=1,
                             highlightbackground="white",
                             highlightcolor="blue")
        productInput.place(x=260, y=200, width=250, height=30)

        # 시리얼번호
        serialNumber = Label(self.window, text="시리얼 번호", font=font, bg="white", anchor="w")
        serialNumber.place(x=110, y=240, width=130, height=30)

        serialNumberInput = Entry(self.window, textvariable=self.serialNumber, font=font, bg="white", bd=1,
                                  highlightbackground="white", highlightcolor="blue")
        serialNumberInput.place(x=260, y=240, width=250, height=30)

        # 첨부 파일 선택
        inputFileLabel = Label(self.window, text="첨부 파일", font=font, bg="white", anchor="w")
        inputFileLabel.place(x=110, y=280, width=130, height=30)

        inputFileBtn = tkinter.Button(self.window, text='파일 찾기', font=12, command=self.fileSelect, bd=1,
                                      highlightbackground="white")
        inputFileBtn.place(x=260, y=280, width=250, height=30)

        # 저장 할 곳 위치
        targetPathLabel = Label(self.window, text="저장 폴더", font=font, bg="white", anchor="w")
        targetPathLabel.place(x=110, y=320, width=130, height=30)

        targetPathBtn = tkinter.Button(self.window, text='폴더 선택', font=12, command=self.folderSelect, bd=1,
                                       highlightbackground="white")
        targetPathBtn.place(x=260, y=320, width=250, height=30)

        # 결과
        submitResult = Label(self.window, textvariable=self.submitResult, text="", font=font, bg="white", anchor="w")
        submitResult.place(x=110, y=400, width=300, height=30)

        submit = Button(self.window, text="확인", command=self.fileMove, bd=1, highlightbackground="white")
        submit.place(x=450, y=360, width=60, height=30)

        self.window.mainloop()

    # 파일 선택 로직
    def fileSelect(self):
        self.window.file = filedialog.askopenfile(parent=self.window, title='파일을 선택해주세요.')
        if hasattr(self.window.file, 'name'):
            self.sourcePath = self.window.file.name
            self.window.file.close()
        else:
            self.sourcePath = ''

    # 폴더 선택 로직
    def folderSelect(self):
        targetDir = filedialog.askdirectory(parent=self.window, title='폴더를 선택해주세요.', initialdir="/")
        self.movePathSet(targetDir)

    # 저장 경로 재정의
    def movePathSet(self, targetDir):
        if targetDir == '':
            return

        if platform.system() == 'windows':
            separator = '\\'
        else:
            separator = '/'
        targetPathSplit = self.sourcePath.split(separator)
        fileName = targetPathSplit[-1]
        self.targetDir = f"{targetDir}{separator}{self.companyName.get()}{separator}{self.productName.get()}{separator}{self.serialNumber.get()}"
        self.targetPath = f"{self.targetDir}{separator}{fileName}"

    # 파일 이동 로직
    def fileMove(self):
        if self.targetPath == '':
            self.resultMessage('저장 폴더 위치를 먼저 선택해주세요.')
            return
        elif self.sourcePath == '':
            self.resultMessage('첨부 파일을 먼저 선택해주세요.')
            return

        # 저장 경로 존재 여부 확인 및 없으면 생성
        if not os.path.exists(self.targetDir):
            os.makedirs(self.targetDir)

        # 파일 이동
        shutil.move(self.sourcePath, self.targetPath)

        # 이동 성공 여부 확인
        if os.path.exists(self.targetPath):
            self.resultMessage('성공')
        else:
            self.resultMessage('실패')

    # 리소스 위치 변경
    def resourcePath(self, relativePath):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relativePath)

    # 결과 메시지 출력
    def resultMessage(self, message):
        if message == '' or message == None:
            self.submitResult.set('오류')
        else:
            self.submitResult.set(message)


if __name__ == '__main__':
    simpleFileMove = SimpleFileMove()
    simpleFileMove.run()
