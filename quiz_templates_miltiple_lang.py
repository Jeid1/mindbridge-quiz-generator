from langchain_core.prompts import ChatPromptTemplate

#------------------------------------------------
# Francais
def create_true_false_template_fr():
    prompt = ChatPromptTemplate.from_messages([
        (
            'system',
            "Vous êtes un moteur de quiz qui génère des questions Vrai/Faux avec des réponses conformément aux spécifications de l'utilisateur."
        ),
        (
            'human',
            "Créez un quiz avec {num_questions} questions Vrai/Faux en utilisant le contexte suivant : {quiz_context}"
        )
    ])
    return prompt
def create_open_ended_template_fr():
    prompt = ChatPromptTemplate.from_messages([
        (
            'system',
            "Vous êtes un moteur de quiz qui génère des questions ouvertes avec des réponses conformément aux spécifications de l'utilisateur."
        ),
        (
            'human',
            "Créez un quiz avec {num_questions} questions ouvertes en utilisant le contexte suivant : {quiz_context}"
        )
    ])
    return prompt
def create_multiple_choice_template_fr():
    prompt = ChatPromptTemplate.from_messages([
        (
            'system',
            "Vous êtes un moteur de quiz qui génère des questions à choix multiples avec des réponses conformément aux spécifications de l'utilisateur."
        ),
        (
            'human',
            "Créez un quiz avec {num_questions} questions en utilisant le contexte suivant : {quiz_context}"
        )
    ])
    return prompt


# Arabic
def create_open_ended_template_ar():
    prompt = ChatPromptTemplate.from_messages([
        (
            'system',
            "أنت محرك اختبارات (quiz) يقوم بإنشاء أسئلة مفتوحة النهاية مع إجابات وفقًا لمتطلبات المستخدم."
        ),
        (
            'human',
            "قم بإنشاء اختبار (quiz) يحتوي على {num_questions} من الأسئلة المفتوحة بناءً على السياق التالي: {quiz_context}"
        )
    ])
    return prompt
def create_true_false_template_ar():
    prompt = ChatPromptTemplate.from_messages([
        (
            'system',
            "أنت محرك اختبارات (quiz) يقوم بإنشاء أسئلة صحيحة/خاطئة مع إجابات وفقًا لمتطلبات المستخدم."
        ),
        (
            'human',
            "قم بإنشاء اختبار (quiz) يحتوي على {num_questions} من الأسئلة الصحيحة/الخاطئة بناءً على السياق التالي: {quiz_context}"
        )
    ])
    return prompt
def create_multiple_choice_template_ar():
    prompt = ChatPromptTemplate.from_messages([
        (
            'system',
            "أنت محرك اختبارات (quiz) يقوم بإنشاء أسئلة متعددة الخيارات مع إجابات وفقًا لمتطلبات المستخدم."
        ),
        (
            'human',
            "قم بإنشاء اختبار (quiz) يحتوي على {num_questions} من الأسئلة بناءً على السياق التالي: {quiz_context}"
        )
    ])
    return prompt


# English
def create_multiple_choice_template_en():
    prompt = ChatPromptTemplate.from_messages([
        (
            'system',
            "You are a quiz engine that generates multiple-choice questions with answers according to user input specifications."
        ),
        (
            'human',
            "Create a quiz with {num_questions} and this context {quiz_context}"
        )
    ])
    return prompt
def create_true_false_template_en():
    prompt = ChatPromptTemplate.from_messages([
        (
            'system',
            "You are a quiz engine that generates true-false questions with answers according to user input specifications."
        ),
        (
            'human',
            "Create a quiz with {num_questions} and this context {quiz_context}"
        )
    ])
    return prompt
def create_open_ended_template_en():
    prompt = ChatPromptTemplate.from_messages([
        (
            'system',
            "You are a quiz engine that generates open-ended questions with answers according to user input specifications."
        ),
        (
            'human',
            "Create a quiz with {num_questions} and this context {quiz_context}"
        )
    ])
    return prompt















