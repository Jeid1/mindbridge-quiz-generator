def simuler_session_state():
    """Simule une version simplifiée de session_state"""
    class SessionState:
        def __init__(self):
            # Notre "boîte de stockage"
            self.data = {}
        
        def get(self, key):
            # Récupérer une valeur
            return self.data.get(key)
        
        def __setattr__(self, name, value):
            # Stocker une valeur
            if name == 'data':
                super().__setattr__(name, value)
            else:
                self.data[name] = value

# Créer notre session_state simulée
st = simuler_session_state()

print("=== Test 1: Stockage simple ===")
# Stocker des données
st.nom = "Jean"
st.age = 25
st.notes = [15, 18, 12]

# Lire des données
print(f"Nom: {st.get('nom')}")
print(f"Age: {st.get('age')}")
print(f"Notes: {st.get('notes')}")

print("\n=== Test 2: Simulation d'un quiz simple ===")
# Stocker les questions
st.questions = ["2 + 2 = ?", "3 x 3 = ?"]
st.reponses_correctes = ["4", "9"]

# Simuler les réponses de l'utilisateur
st.data["reponse_0"] = "4"    # Réponse à la question 1
st.data["reponse_1"] = "8"    # Réponse à la question 2

# Afficher l'état actuel
print("\nContenu de session_state:")
print(f"Questions stockées: {st.get('questions')}")
print(f"Réponses correctes: {st.get('reponses_correctes')}")
print(f"Réponse utilisateur 1: {st.get('reponse_0')}")
print(f"Réponse utilisateur 2: {st.get('reponse_1')}")

print("\n=== Test 3: Modification des données ===")
# Modifier une valeur existante
st.age = 26
print(f"Nouvel âge: {st.get('age')}")

# Ajouter une nouvelle note
st.notes.append(16)
print(f"Nouvelles notes: {st.get('notes')}")

if __name__ == "__main__":
    # Le code s'exécute si on lance directement ce fichier
    pass 