'''questions = ["Q1", "Q2", "Q3"]
for i, question in enumerate(questions):
    print(f"Question {i+1}: {question}")
'''


from langdetect import detect

def detect_language(text: str) -> str:
    """
    Uses langdetect to detect the language from the provided text.
    Returns a language code (e.g. 'en', 'fr', 'ar', etc.).
    """
    return detect(text)

TXT ="اﻟﺪورة - اﻟﻠﻐﻮﻳﺔ اﻟﺪروس «إﻋﺪادي اﻷوﻟﻰ :اﻟﻌﺮﺑﻴﺔ اﻟﻠﻐﺔ  "
print(detect_language(TXT))