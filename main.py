import os, sys

from gtts import gTTS
from pydub import AudioSegment

def get_ffmpeg_path():
    ffmpeg_path = ''
    if getattr(sys, 'frozen', False):  # pyinstaller로 빌드된 실행 파일일 경우
        # 임시 폴더가 있는 디렉터리 기준으로 ffmpeg 경로 설정
        base_path = sys._MEIPASS

        ffmpeg_path = os.path.join(base_path, "ffmpeg.exe")
    else:
        # 개발 환경에서 스크립트 파일 기준으로 ffmpeg 경로 설정
        base_path = os.path.dirname(os.path.abspath(__file__))

        # virtualenv 환경 필수
        ffmpeg_path = os.path.join(base_path, "ffmpeg.exe")
    
    # 경로 확인 및 반환
    if not os.path.isfile(ffmpeg_path):
        raise FileNotFoundError(f"ffmpeg 실행 파일이 존재하지 않습니다: {ffmpeg_path}")
    
    return ffmpeg_path

ffmpeg_path = get_ffmpeg_path()

# ffmpeg 설정
os.environ["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ["PATH"]
AudioSegment.converter = ffmpeg_path

def exit_program(message = '') -> None:
    print(f'\n{message}')
    os.system('pause')
    sys.exit(0)

def folder_exists(folder_name: str) -> None:
    current_directory = os.getcwd()
    folder_path = os.path.join(current_directory, folder_name)
    if not os.path.isdir(folder_path):
        print(f'\n실행 파일 위치에 {folder_name} 폴더가 없어 생성 중입니다.')
        os.mkdir(folder_path)

def folder_check() -> None:
    print("폴더 유무 검사 중...")
    folder_exists('text')
    folder_exists('audio')
    folder_exists('audioResult')

def gTTS_converter(text = '', lang = 'en', slow = False, file_name = '기본 이름') -> None:
    tts = gTTS(text=text, lang=lang, slow=slow)
    tts.save(f'audio/{file_name}.mp3')

if __name__ == '__main__':
    folder_check()

    file_list = os.listdir('./text/')
    if len(file_list) <= 0:
        exit_program('음성으로 만들 파일이 존재하지 않습니다.')

    for file_name in file_list:
        with open(f'./text/{file_name}', encoding='utf-8') as f:
            texts = f.readlines()
            file_name = file_name.removesuffix('.txt')
            for index, line in enumerate(texts):
                if len(line.split('/')) < 2:
                    exit_program('파일 구성이 잘못되었습니다.\n"영어1/한글1\n영어2/한글2" 방식으로 작성해주세요.')

                gTTS_converter(line.split('/')[0], 'en', False, f'{file_name}_{index}_en')
                gTTS_converter(line.split('/')[1], 'ko', False, f'{file_name}_{index}_ko')

        audio_list = os.listdir('./audio/')
        combined_audio = AudioSegment.empty()
        index = 0
        print(f'{file_name} 파일을 mp3로 변환 중...')
        while len([audio for audio in audio_list if f'{file_name}_{index}' in audio]) != 0:
            print(f'mp3파일 생성: ./audio/{file_name}_{index}_en.mp3')
            en_audio = AudioSegment.from_file(f'./audio/{file_name}_{index}_en.mp3', format='mp3')
            ko_audio = AudioSegment.from_file(f'./audio/{file_name}_{index}_ko.mp3', format='mp3')

            combined_audio += (en_audio + AudioSegment.silent(duration=500) + ko_audio + AudioSegment.silent(duration=1000))

            index += 1

        combined_audio.export(f'./audioResult/{file_name}.mp3', format='mp3')
        print(f'{file_name}.mp3가 생성되었습니다!\n')

    # audio 폴더의 파일 전부 삭제
    for audio in audio_list:
        os.remove(f'./audio/{audio}')

    # 끝나면 유저가 확인할 수 있도록
    exit_program()