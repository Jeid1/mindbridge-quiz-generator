from langdetect import detect

# Test pour le français uniquement
texte_fr = "Bonjour, comment allez-vous? Je suis ravi de vous rencontrer."
print(f"Texte français: '{texte_fr}'")
print(f"Langue détectée: {detect(texte_fr)}") 