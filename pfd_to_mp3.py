import pdfplumber
from gtts import gTTS
from deep_translator import GoogleTranslator, single_detection
from pathlib import Path


def pdf_to_mp(path='test.pdf', language='ru'):
    """
    Simple program to convert pdf file to a mp3 file with translator.
    :param path: path to the file in pdf format
    :param language: language code in abbreviation format.
    :return: str with response.
    api_key for language detection taken from https://detectlanguage.com/private
    Used list slicing for GoogleTranslator, to avoid max_size of string length error.
    """
    if Path(path).is_file() and Path(path).suffix == '.pdf':
        print(f'[+] Original file: {Path(path).name}')
        print('[+] working...')
        with pdfplumber.open(path) as pdf:
            extrated_list_text = [i.extract_text() for i in pdf.pages]
        lang_detect = single_detection(extrated_list_text[0], api_key='411eac5fb6bd5acff96113c7c3df0cd0')
        text = " ".join(extrated_list_text).replace('\n', '')
        if lang_detect != language:
            print('[+] translating....')
            translated_text = ""
            i_prev = 0
            for i in range(0, len(text), 900):
                translated_text += GoogleTranslator(source='auto', target=language).translate(text[i_prev:i_prev+900])
                i_prev += 900
            print('[+] translated successfully, carry on')
            tts = gTTS(text=translated_text, lang=language, slow=False)
        else:
            print('[+] Working hard')
            tts = gTTS(text=text, lang=language, slow=False)
        file_name = Path(path).stem
        tts.save(f'{file_name}({language}).mp3')
        return f'[+] {file_name}.mp3 file saved successfully! \nHave a good day!'
    else:
        return f"File does not exist or wrong type"


def main():
    path = input('enter file_path: ')
    lang = input('choose language: ru or en ')
    print(pdf_to_mp(path=path, language=lang))


if __name__ == '__main__':
    main()