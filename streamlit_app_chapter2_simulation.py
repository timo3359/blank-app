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

CHAPTER_2_SCENARIO = (
    "Du bist an der Maschine Waldner 13 und die Bechereintaktung will nicht funktionieren. "
    "Deine Aufgabe ist es, mit Hilfe des Chatbots eine plausible Loesung zu erarbeiten."
)

CHAPTER_2_SOURCES = [
    {
        "id": "handbuch",
        "name": "Handbuch Waldner 13",
        "description": "Grundlagen, Stoerungsbilder und empfohlene Pruefschritte.",
    },
    {
        "id": "stoermeldungen",
        "name": "Ehemalige Stoermeldungen",
        "description": "Historische Vorfaelle mit Loesungsansaetzen aus dem Betrieb.",
    },
    {
        "id": "wartung",
        "name": "Wartungsprotokolle",
        "description": "Wartungs- und Kalibrierhistorie der Maschine.",
    },
]

CHAPTER_2_KNOWLEDGE = {
    "handbuch": {
        "default": "Im Handbuch wird fuer Taktfehler zuerst Sensorposition, Foerderbandlauf und Synchronsignal geprueft.",
        "rules": [
            {
                "keywords": ["becher", "eintakt", "takt"],
                "snippet": "Handbuch: Bei Problemen mit der Bechereintaktung zuerst Lichtschranke LS-4 auf Verschmutzung und Abstand pruefen.",
            },
            {
                "keywords": ["sensor", "lichtschranke"],
                "snippet": "Handbuch: Sensor LS-4 Sollabstand 12 mm, danach Referenzlauf der Linie starten.",
            },
        ],
    },
    "stoermeldungen": {
        "default": "In frueheren Meldungen trat der Fehler oft nach Formatwechsel auf.",
        "rules": [
            {
                "keywords": ["format", "wechsel", "umruesten"],
                "snippet": "Stoermeldung #1842: Nach Formatwechsel half das Nachziehen des Sternrad-Anschlags und ein neuer Referenzlauf.",
            },
            {
                "keywords": ["stop", "stillstand", "ruck"],
                "snippet": "Stoermeldung #1771: Kurze Ruckler im Einlauf wurden durch lockeren Sensorhalter verursacht.",
            },
        ],
    },
    "wartung": {
        "default": "Die letzten Wartungsdaten zeigen eine ueberfaellige Kalibrierung des Einlaufmoduls.",
        "rules": [
            {
                "keywords": ["kalibrier", "wartung", "protokoll"],
                "snippet": "Wartung: Kalibrierung des Einlaufmoduls ist seit 17 Tagen ueberfaellig.",
            },
            {
                "keywords": ["schraube", "halter", "locker"],
                "snippet": "Wartung: Beim letzten Check wurde erhöhte Vibration am Sensorhalter dokumentiert.",
            },
        ],
    },
}


def init_state() -> None:
    if "chapter_1_submitted" not in st.session_state:
        st.session_state.chapter_1_submitted = False
    if "chapter_1_score" not in st.session_state:
        st.session_state.chapter_1_score = 0
    if "chapter_1_page" not in st.session_state:
        st.session_state.chapter_1_page = 0
    if "chapter_1_page_selector" not in st.session_state:
        st.session_state.chapter_1_page_selector = 0
    if "chapter_1_completed" not in st.session_state:
        st.session_state.chapter_1_completed = False
    if "active_chapter" not in st.session_state:
        st.session_state.active_chapter = "Kapitel 1"
    if "active_chapter_selector" not in st.session_state:
        st.session_state.active_chapter_selector = "Kapitel 1"
    if "chapter_2_sources" not in st.session_state:
        st.session_state.chapter_2_sources = []
    if "chapter_2_chat" not in st.session_state:
        st.session_state.chapter_2_chat = [
            {
                "role": "assistant",
                "content": (
                    "Ich bin dein Chatbot. Aktuell habe ich kein Anlagenwissen. "
                    "Wenn du Quellen verbindest, kann ich konkreter helfen."
                ),
            }
        ]


def clamp_page(page: int, total_pages: int) -> int:
    return max(0, min(page, total_pages - 1))


def source_name_map() -> dict[str, str]:
    return {source["id"]: source["name"] for source in CHAPTER_2_SOURCES}


def reset_chapter_2_chat() -> None:
    st.session_state.chapter_2_chat = [
        {
            "role": "assistant",
            "content": (
                "Chat wurde zurueckgesetzt. Ohne Quellen habe ich nur allgemeine Aussagen. "
                "Waehle Unterlagen aus, um mich mit Kontext zu versorgen."
            ),
        }
    ]


def sync_active_chapter() -> None:
    st.session_state.active_chapter = st.session_state.active_chapter_selector


def render_chapter_switcher() -> None:
    chapter_options = ["Kapitel 1"]
    if st.session_state.chapter_1_completed:
        chapter_options.append("Kapitel 2")

    if st.session_state.active_chapter not in chapter_options:
        st.session_state.active_chapter = "Kapitel 1"

    st.session_state.active_chapter_selector = st.session_state.active_chapter

    with st.sidebar:
        st.markdown("## Lernpfad")
        st.selectbox(
            "Kapitel auswaehlen",
            options=chapter_options,
            key="active_chapter_selector",
            on_change=sync_active_chapter,
        )
        if not st.session_state.chapter_1_completed:
            st.caption("Kapitel 2 wird nach Abschluss von Kapitel 1 freigeschaltet.")


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
    st.session_state.chapter_1_completed = True
    st.info(f"Du hast {score} von {len(CHAPTER_1_CONTENT)} Fragen korrekt beantwortet.")

    if score == len(CHAPTER_1_CONTENT):
        st.success(
            "Stark! Kapitel 1 abgeschlossen. Du bist bereit fuer Kapitel 2: "
            "RAG-Systeme konfigurieren."
        )
    else:
        st.warning("Lies die Lernkarten noch einmal und versuche den Quiz erneut.")

    if st.button("Zu Kapitel 2 wechseln", use_container_width=True):
        st.session_state.active_chapter = "Kapitel 2"
        st.session_state.active_chapter_selector = "Kapitel 2"
        st.rerun()


def retrieve_context(user_message: str, selected_sources: list[str]) -> list[str]:
    message = user_message.lower()
    snippets: list[str] = []

    for source_id in selected_sources:
        source_knowledge = CHAPTER_2_KNOWLEDGE[source_id]
        matched = False
        for rule in source_knowledge["rules"]:
            if any(keyword in message for keyword in rule["keywords"]):
                snippets.append(rule["snippet"])
                matched = True
        if not matched:
            snippets.append(source_knowledge["default"])

    return snippets


def generate_chapter_2_answer(user_message: str, selected_sources: list[str]) -> str:
    if not selected_sources:
        return (
            "Aktuell kann ich nur allgemein helfen, weil keine Unterlagen verbunden sind. "
            "Ich wuerde bei der Waldner 13 strukturiert vorgehen: "
            "1) Symptom genau beobachten, 2) Sensorik pruefen, 3) letzten Eingriff klaeren. "
            "Verbinde Handbuch oder Stoermeldungen, dann kann ich dir konkrete Schritte nennen."
        )

    snippets = retrieve_context(user_message=user_message, selected_sources=selected_sources)
    source_names = source_name_map()
    connected = ", ".join(source_names[source_id] for source_id in selected_sources)

    evidence_lines = "\n".join([f"- {snippet}" for snippet in snippets[:4]])
    return (
        "Mit den verbundenen Quellen kann ich dir gezielter helfen.\n\n"
        f"Aktive Quellen: {connected}\n\n"
        "Relevanter Kontext:\n"
        f"{evidence_lines}\n\n"
        "Empfohlener naechster Schritt: Starte mit Sensor LS-4 (Reinigung + Abstand), "
        "danach Referenzlauf. Wenn der Fehler bleibt, pruefe Sternrad-Anschlag und den Sensorhalter auf Spiel."
    )


def render_chapter_2() -> None:
    st.title("RAG Agent Academy")
    st.subheader("Kapitel 2: Interaktives RAG-Modell")
    st.write(
        "Hier erlebst du den Unterschied zwischen einem Chatbot ohne Wissensbasis "
        "und einem Chatbot mit angebundenen Quellen."
    )
    st.progress(2 / 3, text="Lernpfad-Fortschritt: Kapitel 2 von 3")

    with st.container(border=True):
        st.markdown("### Einsatzsituation")
        st.write(CHAPTER_2_SCENARIO)

    st.markdown("### Schritt 1: Quellen verbinden")
    options = [source["name"] for source in CHAPTER_2_SOURCES]
    id_by_name = {source["name"]: source["id"] for source in CHAPTER_2_SOURCES}

    selected_names = st.multiselect(
        "Waehle Unterlagen fuer dein RAG-System",
        options=options,
        default=[source_name_map()[source_id] for source_id in st.session_state.chapter_2_sources],
    )
    st.session_state.chapter_2_sources = [id_by_name[name] for name in selected_names]

    info_cols = st.columns(len(CHAPTER_2_SOURCES))
    for idx, source in enumerate(CHAPTER_2_SOURCES):
        with info_cols[idx]:
            enabled = "Verbunden" if source["id"] in st.session_state.chapter_2_sources else "Nicht verbunden"
            st.metric(source["name"], enabled)
            st.caption(source["description"])

    action_col_1, action_col_2 = st.columns([1, 1])
    with action_col_1:
        if st.button("Chat zuruecksetzen", use_container_width=True):
            reset_chapter_2_chat()
            st.rerun()
    with action_col_2:
        if st.button("Zurueck zu Kapitel 1", use_container_width=True):
            st.session_state.active_chapter = "Kapitel 1"
            st.session_state.active_chapter_selector = "Kapitel 1"
            st.rerun()

    st.markdown("### Schritt 2: Mit dem Chatbot arbeiten")
    st.caption("Tipp: Frage zuerst ohne Quellen und dann mit Handbuch + Stoermeldungen.")

    for message in st.session_state.chapter_2_chat:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_prompt = st.chat_input("Stelle dem Chatbot eine Frage zur Situation...")
    if user_prompt:
        st.session_state.chapter_2_chat.append({"role": "user", "content": user_prompt})
        assistant_answer = generate_chapter_2_answer(
            user_message=user_prompt,
            selected_sources=st.session_state.chapter_2_sources,
        )
        st.session_state.chapter_2_chat.append({"role": "assistant", "content": assistant_answer})
        st.rerun()



def main() -> None:
    init_state()
    render_chapter_switcher()

    if st.session_state.active_chapter == "Kapitel 2":
        render_chapter_2()
        return

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
