from langdetect import detect

def detect_language(text: str) -> str:
    """
    Détecte la langue du texte fourni.
    Retourne le code de la langue (ex: 'fr', 'en', 'ar')
    """
    return detect(text)

# Tests avec différentes langues
def test_language_detection():
    # Test en français
    texte_fr = "Bonjour, comment allez-vous? Je suis ravi de vous rencontrer."
    print(f"Texte français: '{texte_fr}'")
    print(f"Langue détectée: {detect_language(texte_fr)}\n")

    # Test en anglais
    texte_en = "Hello, how are you? I am happy to meet you."
    print(f"Texte anglais: '{texte_en}'")
    print(f"Langue détectée: {detect_language(texte_en)}\n")

    # Test en arabe
    texte_ar = "مرحبا كيف حالك؟ أنا سعيد بلقائك."
    print(f"Texte arabe: '{texte_ar}'")
    print(f"Langue détectée: {detect_language(texte_ar)}\n")

if __name__ == "__main__":
    print("=== Test de détection de langue ===")
    test_language_detection() 