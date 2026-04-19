import streamlit as st

st.set_page_config(page_title="RAG Agent Academy", page_icon="🧠", layout="wide")


# Kapitelinhalte zentral als Datenstruktur.
# Du kannst Begriffe, Erklaerungen, Antwortoptionen und korrekte Antwort spaeter hier leicht anpassen.
CHAPTER_1_CONTENT = [
    {
        "term": "Retrieval-Augmented Generation (RAG)",
        "topic": "RAG",
        "explanation": (
            "RAG kombiniert ein Sprachmodell mit externer Wissenssuche. "
            "Statt nur aus trainiertem Wissen zu antworten, werden vor der Antwort "
            "passende Dokumente gesucht und als Kontext genutzt."
        ),
        "question": "Welcher Schritt macht aus einem normalen LLM-Chat ein RAG-System?",
        "options": [
            "Nur die Temperatur auf 0 setzen",
            "Externe Inhalte abrufen und als Kontext einbinden",
            "Mehr Emojis in den Prompt schreiben",
            "Nur kuerzere Antworten erzwingen",
        ],
        "correct": "Externe Inhalte abrufen und als Kontext einbinden",
        "hint": "Denke an den Unterschied zwischen reinem Modellwissen und externer Wissensbasis.",
    },
    {
        "term": "Chunking",
        "topic": "RAG",
        "explanation": (
            "Beim Chunking werden Dokumente in kleinere Abschnitte zerlegt. "
            "So kann die Suche genauer Treffer finden und dem Modell nur relevante "
            "Textteile liefern."
        ),
        "question": "Warum wird Chunking in RAG-Pipelines verwendet?",
        "options": [
            "Um die Schriftgroesse der Dokumente zu veraendern",
            "Um Daten in kleinere, besser durchsuchbare Einheiten zu teilen",
            "Um alle Quellen zu loeschen",
            "Um den Prompt komplett zu ersetzen",
        ],
        "correct": "Um Daten in kleinere, besser durchsuchbare Einheiten zu teilen",
        "hint": "Der Retriever braucht handhabbare Textstuecke statt sehr langer Seiten.",
    },
    {
        "term": "System Prompt",
        "topic": "Prompting",
        "explanation": (
            "Der System Prompt legt Rolle, Ton und Regeln des Assistenten fest. "
            "Er wirkt wie ein Rahmen, in dem spaetere Nutzereingaben interpretiert werden."
        ),
        "question": "Was ist die Hauptaufgabe eines System Prompts?",
        "options": [
            "Nur die Sprache Deutsch zu erzwingen",
            "Rolle und Verhalten des Modells langfristig steuern",
            "Bilder im Browser anzeigen",
            "Die Datenbank zu sichern",
        ],
        "correct": "Rolle und Verhalten des Modells langfristig steuern",
        "hint": "Es geht um Regeln, Persona und Grenzen fuer das Verhalten des Assistenten.",
    },
    {
        "term": "Grounding",
        "topic": "Prompting",
        "explanation": (
            "Grounding bedeutet, Antworten eng an konkrete Quellen und Fakten zu binden. "
            "Damit sinkt das Risiko von Halluzinationen und die Antwort wird nachvollziehbarer."
        ),
        "question": "Woran erkennst du gute Grounding-Praxis?",
        "options": [
            "Antworten basieren auf verifizierbaren Quellen",
            "Antworten sind absichtlich vage",
            "Der Bot ignoriert Kontextdokumente",
            "Das Modell antwortet immer mit Gegenfragen",
        ],
        "correct": "Antworten basieren auf verifizierbaren Quellen",
        "hint": "Frage dich, ob Aussagen auf konkrete, pruefbare Belege zurueckgefuehrt werden koennen.",
    },
    {
        "term": "Mensch-KI-Kollaboration",
        "topic": "Mensch-KI Beziehung",
        "explanation": (
            "In der Zusammenarbeit mit KI bleibt der Mensch verantwortlich fuer Ziele, "
            "Bewertung und Entscheidungen. Die KI unterstuetzt bei Recherche, Entwuerfen "
            "und Alternativen, ersetzt aber nicht die fachliche Verantwortung."
        ),
        "question": "Was beschreibt eine gesunde Mensch-KI-Beziehung im Arbeitsalltag?",
        "options": [
            "Die KI entscheidet allein ueber finale Ergebnisse",
            "Menschen pruefen Ergebnisse und treffen die finalen Entscheidungen",
            "Prompts werden nie dokumentiert",
            "KI-Ausgaben werden ungeprueft weitergegeben",
        ],
        "correct": "Menschen pruefen Ergebnisse und treffen die finalen Entscheidungen",
        "hint": "Wer traegt in Unternehmen am Ende Verantwortung fuer Entscheidungen?",
    },
]


def init_state() -> None:
    if "chapter_1_submitted" not in st.session_state:
        st.session_state.chapter_1_submitted = False
    if "chapter_1_score" not in st.session_state:
        st.session_state.chapter_1_score = 0
    if "chapter_1_page" not in st.session_state:
        st.session_state.chapter_1_page = 0
    if "chapter_1_page_selector" not in st.session_state:
        st.session_state.chapter_1_page_selector = 0


def clamp_page(page: int, total_pages: int) -> int:
    return max(0, min(page, total_pages - 1))


def render_header(current_page: int, total_pages: int) -> None:
    st.title("RAG Agent Academy")
    st.subheader("Kapitel 1: Grundlagen verstehen")
    st.write(
        "In diesem Kapitel hat jede Lernkarte eine eigene Seite. "
        "Nach den 5 Karten folgt ein Quiz auf einer separaten Seite."
    )

    progress_value = (current_page + 1) / total_pages
    st.progress(
        progress_value,
        text=f"Seite {current_page + 1} von {total_pages} in Kapitel 1",
    )


def page_labels() -> list[str]:
    card_pages = [f"Lernkarte {idx}: {item['term']}" for idx, item in enumerate(CHAPTER_1_CONTENT, start=1)]
    return card_pages + ["Quiz"]


def sync_page_from_sidebar() -> None:
    st.session_state.chapter_1_page = st.session_state.chapter_1_page_selector


def render_sidebar_navigation(total_pages: int) -> int:
    labels = page_labels()
    st.session_state.chapter_1_page = clamp_page(st.session_state.chapter_1_page, total_pages)
    st.session_state.chapter_1_page_selector = st.session_state.chapter_1_page

    with st.sidebar:
        st.markdown("### Navigation")
        st.selectbox(
            "Seite auswaehlen",
            options=list(range(total_pages)),
            format_func=lambda page_idx: labels[page_idx],
            key="chapter_1_page_selector",
            on_change=sync_page_from_sidebar,
        )
        current_page = st.session_state.chapter_1_page

        st.caption("Du kannst jederzeit zwischen Lernkarten und Quiz wechseln.")

    return current_page


def render_step_navigation(current_page: int, total_pages: int) -> int:

    prev_col, next_col = st.columns(2)
    with prev_col:
        if st.button("Zurueck", use_container_width=True, disabled=current_page == 0):
            st.session_state.chapter_1_page = clamp_page(current_page - 1, total_pages)
            st.rerun()
    with next_col:
        if st.button(
            "Weiter",
            use_container_width=True,
            disabled=current_page == total_pages - 1,
        ):
            st.session_state.chapter_1_page = clamp_page(current_page + 1, total_pages)
            st.rerun()

    return current_page


def render_learning_card(card_index: int, total_cards: int) -> None:
    item = CHAPTER_1_CONTENT[card_index]
    st.markdown(f"### Lernkarte {card_index + 1} von {total_cards}")
    with st.container(border=True):
        st.markdown(f"## {item['term']}")
        st.caption(f"Themenfeld: {item['topic']}")
        st.write(item["explanation"])


def render_quiz() -> None:
    st.markdown("### Quiz: Pruefe dein Wissen")
    st.write("Beantworte alle Fragen und klicke auf **Auswertung starten**.")
    st.info("Unter jeder Frage kannst du bei Bedarf einen Hinweis aufklappen.")

    with st.form("chapter_1_quiz"):
        answers = {}
        for idx, item in enumerate(CHAPTER_1_CONTENT, start=1):
            st.markdown(f"**{idx}) {item['question']}**")
            with st.expander("Hinweis anzeigen"):
                st.write(item["hint"])

            options_with_placeholder = ["Bitte waehlen..."] + item["options"]
            selected = st.radio(
                "Antwort",
                options=options_with_placeholder,
                key=f"q_{idx}",
                label_visibility="collapsed",
            )
            answers[idx] = selected

        submitted = st.form_submit_button("Auswertung starten", use_container_width=True)

    if not submitted:
        return

    unanswered_questions = [idx for idx, answer in answers.items() if answer == "Bitte waehlen..."]
    if unanswered_questions:
        st.warning("Bitte beantworte zuerst alle Fragen, bevor du die Auswertung startest.")
        st.caption(
            "Noch offen: "
            + ", ".join([f"Frage {question_idx}" for question_idx in unanswered_questions])
        )
        return

    st.session_state.chapter_1_submitted = True
    score = 0

    st.markdown("### Ergebnis")
    for idx, item in enumerate(CHAPTER_1_CONTENT, start=1):
        user_answer = answers[idx]
        is_answered = user_answer != "Bitte waehlen..."
        is_correct = user_answer == item["correct"]

        if is_correct:
            score += 1

        with st.container(border=True):
            st.markdown(f"**Frage {idx}**")
            if is_correct:
                st.success("Richtig beantwortet.")
            else:
                st.error("Noch nicht korrekt.")

            st.write(f"Deine Antwort: {user_answer}")
            if is_answered:
                st.write(f"Korrekte Antwort: {item['correct']}")

    st.session_state.chapter_1_score = score
    st.info(f"Du hast {score} von {len(CHAPTER_1_CONTENT)} Fragen korrekt beantwortet.")

    if score == len(CHAPTER_1_CONTENT):
        st.success(
            "Stark! Kapitel 1 abgeschlossen. Du bist bereit fuer Kapitel 2: "
            "RAG-Systeme konfigurieren."
        )
    else:
        st.warning("Lies die Lernkarten noch einmal und versuche den Quiz erneut.")



def main() -> None:
    init_state()

    total_pages = len(CHAPTER_1_CONTENT) + 1
    st.session_state.chapter_1_page = clamp_page(st.session_state.chapter_1_page, total_pages)
    current_page = render_sidebar_navigation(total_pages=total_pages)
    current_page = clamp_page(current_page, total_pages)

    render_header(current_page=current_page, total_pages=total_pages)
    current_page = render_step_navigation(current_page=current_page, total_pages=total_pages)

    if current_page < len(CHAPTER_1_CONTENT):
        render_learning_card(card_index=current_page, total_cards=len(CHAPTER_1_CONTENT))
    else:
        render_quiz()


if __name__ == "__main__":
    main()
