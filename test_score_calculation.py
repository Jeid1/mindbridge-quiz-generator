def simuler_session_state():
    """Simule le comportement de session_state de Streamlit"""
    class SessionState:
        def __init__(self):
            self.data = {}
        
        def get(self, key):
            return self.data.get(key)
        
        def __setattr__(self, name, value):
            if name == 'data':
                super().__setattr__(name, value)
            else:
                self.data[name] = value

    return SessionState()

def test_score_calculation():
    print("\n=== Test du calcul de score ===\n")
    
    # Simuler session_state
    st = simuler_session_state()
    
    # 1. Exemple avec QCM
    print("Test 1: QCM")
    print("-----------")
    
    # Simuler les questions et réponses correctes
    st.questions = [
        "Quelle est la capitale de la France?",
        "Quelle est la plus grande planète du système solaire?",
        "Quel est le symbole chimique de l'or?"
    ]
    
    st.answers = ["a", "b", "c"]  # a=Paris, b=Jupiter, c=Au
    
    # Simuler les réponses de l'utilisateur (stockées dans session_state)
    st.data["question_0"] = "a"  # Correct
    st.data["question_1"] = "b"  # Correct
    st.data["question_2"] = "a"  # Incorrect
    
    # Transformation des réponses utilisateur
    print("\nÉtape 1: Récupération des réponses utilisateur")
    user_answers = [
        st.get(f"question_{i}") for i in range(len(st.questions))
    ]
    print(f"Réponses utilisateur: {user_answers}")
    print(f"Réponses correctes : {st.answers}")
    
    # Calcul du score
    print("\nÉtape 2: Calcul du score")
    score = sum(
        user_answer == correct_answer
        for user_answer, correct_answer
        in zip(user_answers, st.answers)
    )
    
    # Afficher les détails
    print("\nDétails de la correction:")
    for i, (question, user_ans, correct_ans) in enumerate(zip(st.questions, user_answers, st.answers)):
        is_correct = user_ans == correct_ans
        print(f"\nQuestion {i+1}: {question}")
        print(f"Votre réponse: {user_ans}")
        print(f"Réponse correcte: {correct_ans}")
        print(f"Résultat: {'✓ Correct' if is_correct else '✗ Incorrect'}")
    
    print(f"\nScore final: {score}/{len(st.questions)}")

if __name__ == "__main__":
    test_score_calculation() 