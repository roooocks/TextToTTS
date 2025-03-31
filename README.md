## 프로그램 설명

"영어/한국어\n영어/한국어..."을 적으면 영어와 한국어를 TTS로 차례대로 읽어주는 프로그램입니다.
<br>

## 만든 이유

아빠가 영어 공부 때문에 만들어달라고 하셨는데, 저도 음성 파일은 건드려 본 적이 없어서 호기심에 만들었습니다.

## 개발환경

사용 언어 = Python <br>
사용 운영체제 = Window 10 <br>
가상 환경 사용 = virtualenv

## virtualenv에서 받은 패키지

`pip install gTTS` <br>
`pip install pydub` <br>
`pip install pyinstaller` <br>

## 추가적으로 받아야 할 외부 파일

imageio-ffmpeg 패키지를 써도 ffmpeg 인식이 안되서 ffmpeg 사이트에서 윈도우용 파일을 다운받아서 써야합니다.
<br><br>
ffmpeg.exe만 있으면 안되고 ffprobe.exe도 있어야 합니다. (ffplay.exe는 혹시 몰라서 넣었습니다.)

## pyinstaller 설정

1. `pyinstaller --onefile --console main.py` 실행
2. 생성된 main.spec에 binaries, datas에 아래처럼 설정

```spec
...
    binaries=[
        ('./ffmpeg.exe', '.'),
        ('./ffprobe.exe', '.'),
        ('./ffplay.exe', '.')
    ],
    datas=[
        ('./venv/Lib/site-packages', 'site-packages')
    ]
...
```

## 사용방법

### text 폴더에 들어갈 메모장의 구조

```txt
영어1/한글1
영어2/한글2
영어3/한글3
영어4/한글4
영어5/한글5
영어6/한글6
...
```

### 폴더가 없을 경우

1. main.exe 를 실행시키면 폴더가 생성되고 종료됩니다.
2. text 폴더에 음성을 만들 내용을 적어둔 메모장을 넣습니다.
3. 다시 한번 main.exe를 실행시킵니다.
4. audioResult 폴더에 mp3 파일이 생성됩니다!

### 폴더가 있을 경우

1. text 폴더에 음성을 만들 내용을 적어둔 메모장을 넣습니다.
2. main.exe를 실행시킵니다.
3. audioResult 폴더에 mp3 파일이 생성됩니다!
