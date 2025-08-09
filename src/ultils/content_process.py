import regex
from underthesea import word_tokenize, pos_tag, sent_tokenize, chunk
import re
from ultils import word_dictionary

folder_path = 'src/data/files'
#LOAD EMOJICON
file = open(f'{folder_path}/emojicon.txt', 'r', encoding="utf8")
emoji_lst = file.read().split('\n')
emoji_dict = {}
for line in emoji_lst:
    key, value = line.split('\t')
    emoji_dict[key] = str(value)
file.close()
#################
#LOAD TEENCODE
file = open(f'{folder_path}/teencode.txt', 'r', encoding="utf8")
teen_lst = file.read().split('\n')
teen_dict = {}
for line in teen_lst:
    key, value = line.split('\t')
    teen_dict[key] = str(value)
file.close()
###############
#LOAD TRANSLATE ENGLISH -> VNMESE
file = open(f'{folder_path}/english-vnmese.txt', 'r', encoding="utf8")
english_lst = file.read().split('\n')
english_dict = {}
for line in english_lst:
    key, value = line.split('\t')
    english_dict[key] = str(value)
file.close()
################
#LOAD wrong words
file = open(f'{folder_path}/wrong-word.txt', 'r', encoding="utf8")
wrong_lst = file.read().split('\n')
file.close()
#################
#LOAD STOPWORDS
file = open(f'{folder_path}/vietnamese-stopwords.txt', 'r', encoding="utf8")
stopwords_lst = file.read().split('\n')
file.close()

stopwords_lst = stopwords_lst + word_dictionary.manual_stopwords
####
# Chuẩn hóa unicode tiếng việt
def loaddicchar():
    uniChars = "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴÂĂĐÔƠƯ"
    unsignChars = "aaaaaaaaaaaaaaaaaeeeeeeeeeeediiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAAEEEEEEEEEEEDIIIOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYAADOOU"

    dic = {}
    char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
        '|')
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        '|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic

# Đưa toàn bộ dữ liệu qua hàm này để chuẩn hóa lại
def convert_unicode(txt):
    dicchar = loaddicchar()
    return regex.sub(
        r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
        lambda x: dicchar[x.group()], txt)

def process_special_word(text):
    # Tokenize the text if input is a string
    if isinstance(text, str):
        text_lst = word_tokenize(text, format="text").split()
    elif isinstance(text, list):
        text_lst = text
    else:
        raise ValueError("Input should be a string or a pre-tokenized list.")

    new_text = []
    i = 0

    while i < len(text_lst):
        # Check for multi-word phrases
        current_phrase = text_lst[i]
        next_idx = i + 1

        # Check for two-word phrase
        if next_idx < len(text_lst):
            combined_phrase = f"{text_lst[i]}_{text_lst[next_idx]}"
            if combined_phrase in word_dictionary.connecting_words:
                current_phrase = combined_phrase
                i += 1  # Skip the next word as it's part of the phrase

        new_text.append(current_phrase)
        i += 1

    # Join the processed words back into a single string
    return " ".join(new_text)

# Hàm để chuẩn hóa các từ có ký tự lặp
def normalize_repeated_characters(text):
    # Thay thế mọi ký tự lặp liên tiếp bằng một ký tự đó
    # Ví dụ: "lònggggg" thành "lòng", "thiệtttt" thành "thiệt"
    return re.sub(r'(.)\1+', r'\1', text)

def process_postag_thesea(text, lst_word_type=None, preserve_phrases=None):
    if lst_word_type is None:
        lst_word_type = ['N', 'Np', 'A', 'Ab', 'V', 'Vb', 'Vy', 'R']  # Default POS tags

    if preserve_phrases is None:
        preserve_phrases = ['giảm thâm','rất','rất_tốt','tốt','bình_thường','cũng_được',\
                            'tạm_được','khá','tệ','chán','10đ','chân_ái','ngon_bổ_rẻ','ngon_rẻ',
                            'ngon_bổ','ngon_tốt','xịn','quá tệ','không tốt',
                            'không như quảng cáo','không giống quảng cáo','không hài lòng','nâng_tone']  # Add more phrases as needed

    # Preprocess text to temporarily replace preserve_phrases with tokens
    for phrase in preserve_phrases:
        text = text.replace(phrase, '_'.join(phrase.split()))

    new_document = ''
    for sentence in sent_tokenize(text):
        sentence = sentence.replace('.', '')

        # Tokenize and POS tag
        tagged_words = pos_tag(word_tokenize(sentence, format="text"))

        # Filter words by POS tags
        filtered_sentence = []
        for word, tag in tagged_words:
            if word in preserve_phrases:
                # Restore preserved phrases
                filtered_sentence.append(word.replace('_', ' '))
            elif tag.upper() in lst_word_type:
                filtered_sentence.append(word)

        # Join the filtered words
        new_document += ' '.join(filtered_sentence) + ' '

    # Remove excess blank spaces
    new_document = regex.sub(r'\s+', ' ', new_document).strip()
    return new_document

def remove_stopword(text, stopwords):
    ###### REMOVE stop words
    document = ' '.join('' if word in stopwords else word for word in text.split())
    #print(document)
    ###### DEL excess blank space
    document = regex.sub(r'\s+', ' ', document).strip()
    return document

def handle_ambiguous_words(text, sentiment_dict):
    # Split text into words
    words = text.split()
    processed_text = []

    for i, word in enumerate(words):
        # If 'mụn' is found, look at its context
        if word == "mụn":
            # Check the previous and next words
            prev_word = words[i - 1] if i > 0 else ""
            next_word = words[i + 1] if i < len(words) - 1 else ""

            # Combine 'mụn' with previous or next words
            phrase_prev = f"{prev_word}_{word}"
            phrase_next = f"{word}_{next_word}"

            # Determine if the phrase has sentiment
            if phrase_prev in sentiment_dict:
                processed_text.append(phrase_prev)
            elif phrase_next in sentiment_dict:
                processed_text.append(phrase_next)
            else:
                processed_text.append(word)
        else:
            processed_text.append(word)

    return " ".join(processed_text)

def remove_stopword_with_protection(text, stopwords_lst, protected_words):
    # Split the text into words
    words = text.split()

    # Remove stopwords but keep protected words
    filtered_words = [word for word in words if word in protected_words or word not in stopwords_lst ]

    # Rejoin the filtered words into a string
    return ' '.join(filtered_words)


def process_text(text, emoji_dict, teen_dict, wrong_lst, english_dict):
    document = text.lower()
    document = document.replace("’",'')
    document = regex.sub(r'\.+', ".", document)
    new_sentence =''
    for sentence in sent_tokenize(document):
        # if not(sentence.isascii()):
        ###### CONVERT EMOJICON
        sentence = ''.join(emoji_dict[word]+' ' if word in emoji_dict else word for word in list(sentence))

        ###### CONVERT TEENCODE
        sentence = ' '.join(teen_dict[word] if word in teen_dict else word for word in sentence.split())

        ###### DEL Punctuation & Numbers
        pattern = r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]+\b'
        sentence = ' '.join(regex.findall(pattern,sentence))

        ###### CONVERT ENG-VN
        sentence = ' '.join(english_dict[word] + ' ' if word in english_dict else word for word in sentence.split())

        ###### DEL wrong words
        sentence = ' '.join('' if word in wrong_lst else word for word in sentence.split())

        ###### Normalize Repeated Characters
        sentence = normalize_repeated_characters(sentence)

        new_sentence = new_sentence + sentence + ' '

    document = new_sentence
    #print(document)

    ###### DEL excess blank space
    document = regex.sub(r'\s+', ' ', document).strip()
    #...
    return document


def clean_comment(df_data, input_col, output_col):
    # Step 1: Convert Unicode
    df_data[f'{output_col}'] = df_data[input_col].apply(lambda x: convert_unicode(x))
    print('- step1: Convert Unicode - Done...')

    # Step 2: Process Text
    df_data[f'{output_col}'] = df_data[output_col].apply(
        lambda x: process_text(x, emoji_dict, teen_dict, wrong_lst, english_dict)
    )
    print('- step2: Process Text - Done...')

    # Step 3: Process Special Words
    df_data[f'{output_col}'] = df_data[output_col].apply(lambda x: process_special_word(x))
    print('- step3: Process Special Words - Done...')

    # Step 4: Handle Ambiguous Words
    df_data[f'{output_col}'] = df_data[output_col].apply(lambda x: handle_ambiguous_words(x, word_dictionary.sentiment_dict))
    print('- step4: Handle Ambiguous Words - Done...')

    # Step 5: Process POS Tags
    df_data[f'{output_col}'] = df_data[output_col].apply(lambda x: process_postag_thesea(x))
    print('- step5: Process Postag Thesea - Done...')

    # Step 6: Remove Stopwords
    df_data[f'{output_col}'] = df_data[output_col].apply(lambda x: remove_stopword(x, stopwords_lst))
    print('- step6: Remove Stopword - Done...')

    # Step 7: Create chunk word
    df_data[f'{output_col}_chunk'] = df_data[output_col].apply(lambda x: chunk(x))
    print('- step7: Create Chunk - Done...')

    return df_data