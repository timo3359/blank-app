import os

import streamlit as st

try:
    from mistralai import Mistral
except ImportError:
    Mistral = None

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
        "hint": "Frage dich, ob Aussagen auf konkrete, pruefbare Belege zurueckgeführt werden koennen.",
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

MISTRAL_MODEL_NAME = "mistral-large-latest"

CHAPTER_2_SOURCES = [
    {
        "id": "handbuch",
        "name": "Handbuch Waldner 13",
        "description": "Grundlagen, Störungsbilder und empfohlene Prüfschritte.",
    },
    {
        "id": "stoermeldungen",
        "name": "Ehemalige Störmeldungen",
        "description": "Historische Vorfälle mit Lösungsansätzen aus dem Betrieb.",
    },
    {
        "id": "wartung",
        "name": "Wartungsprotokolle",
        "description": "Wartungs- und Kalibrierhistorie der Maschine.",
    },
]

# Diese Dateien werden serverseitig geladen (nicht vom Endnutzer hochgeladen).
# Passe die Pfade auf deine echten Unterlagen an.
CHAPTER_2_SOURCE_FILE_PATHS = {
    "handbuch": [
        "rag_sources/handbuch_waldner13.txt",
    ],
    "stoermeldungen": [
        "rag_sources/stoermeldungen_historie.txt",
    ],
    "wartung": [
        "rag_sources/wartungsprotokolle.txt",
    ],
}

CHAPTER_2_KNOWLEDGE = {
    "handbuch": {
        "default": "Im Handbuch wird fuer Taktfehler zuerst Sensorposition, Foerderbandlauf und Synchronsignal geprüft.",
        "rules": [
            {
                "keywords": ["becher", "eintakt", "takt"],
                "snippet": "Handbuch: Bei Problemen mit der Bechereintaktung zuerst Lichtschranke LS-4 auf Verschmutzung und Abstand prüfen.",
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

KNOWLEDGE_TOPICS = [
    {
        "id": "rag_intro",
        "title": "Was ist RAG?",
        "summary": "Grundidee von Retrieval-Augmented Generation, Vorteile und typische Einsatzszenarien.",
        "details": (
            "RAG verbindet ein Sprachmodell mit einer externen Wissensbasis. "
            "Statt nur aus dem Trainingswissen zu antworten, werden relevante Dokumente gesucht, "
            "als Kontext hinzugefügt und dann für die Antwort verwendet."
        ),
    },
    {
        "id": "prompting",
        "title": "Prompting im Alltag",
        "summary": "Wie gute Anfragen formuliert werden und welche Informationen wichtig sind.",
        "details": (
            "Gute Prompts benennen Ziel, Kontext, Rollenbild und erwartetes Ergebnis. "
            "Je konkreter die Aufgabe und je besser die Rahmenbedingungen beschrieben sind, "
            "desto konsistenter werden die Antworten."
        ),
    },
    {
        "id": "sources",
        "title": "Quellen und Dokumente",
        "summary": "Wie Handbuch, Stoermeldungen und Wartungsnotizen in RAG genutzt werden.",
        "details": (
            "Im Wissensteil kannst du dir anschauen, wie verschiedene Dokumenttypen aufgebaut sind. "
            "In RAG werden Quellen normalerweise segmentiert, indiziert und dann bei passenden Fragen wiedergefunden."
        ),
    },
    {
        "id": "human_ai",
        "title": "Mensch-KI-Zusammenarbeit",
        "summary": "Welche Rolle der Mensch bei Kontrolle, Bewertung und Entscheidung hat.",
        "details": (
            "KI unterstuetzt bei Recherche, Strukturierung und Formulierung. "
            "Die Verantwortung fuer fachliche Entscheidungen, Freigaben und Kontrolle bleibt aber beim Menschen."
        ),
    },
]


def init_state() -> None:
    if "chapter_1_submitted" not in st.session_state:
        st.session_state.chapter_1_submitted = False
    if "chapter_1_score" not in st.session_state:
        st.session_state.chapter_1_score = 0
    if "chapter_1_result_details" not in st.session_state:
        st.session_state.chapter_1_result_details = []
    if "chapter_1_page" not in st.session_state:
        st.session_state.chapter_1_page = 0
    if "chapter_1_page_selector" not in st.session_state:
        st.session_state.chapter_1_page_selector = 0
    if "chapter_1_completed" not in st.session_state:
        st.session_state.chapter_1_completed = False
    if "chapter_1_passed" not in st.session_state:
        st.session_state.chapter_1_passed = False
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
    if "chapter_2_mode" not in st.session_state:
        st.session_state.chapter_2_mode = "Simulation (Regelbasiert)"
    if "app_section" not in st.session_state:
        st.session_state.app_section = "start"
    if "knowledge_topic" not in st.session_state:
        st.session_state.knowledge_topic = KNOWLEDGE_TOPICS[0]["id"]


def clamp_page(page: int, total_pages: int) -> int:
    return max(0, min(page, total_pages - 1))


def source_name_map() -> dict[str, str]:
    return {source["id"]: source["name"] for source in CHAPTER_2_SOURCES}


def get_mistral_api_key() -> str:
    key_from_secrets = st.secrets.get("MISTRAL_API_KEY", "")
    key_from_env = os.getenv("MISTRAL_API_KEY", "")
    return key_from_secrets or key_from_env


def load_script_source_documents() -> tuple[dict[str, list[dict[str, str]]], list[str]]:
    docs_by_source: dict[str, list[dict[str, str]]] = {source["id"]: [] for source in CHAPTER_2_SOURCES}
    missing_files: list[str] = []

    for source_id, paths in CHAPTER_2_SOURCE_FILE_PATHS.items():
        for path in paths:
            try:
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read().strip()
                docs_by_source.setdefault(source_id, []).append(
                    {
                        "path": path,
                        "content": content,
                    }
                )
            except OSError:
                missing_files.append(path)

    return docs_by_source, missing_files


def retrieve_document_chunks(
    user_message: str,
    selected_sources: list[str],
    docs_by_source: dict[str, list[dict[str, str]]],
    max_chunks: int = 4,
) -> list[str]:
    message_terms = [term for term in user_message.lower().split() if len(term) > 2]
    candidates: list[tuple[int, str]] = []

    for source_id in selected_sources:
        for doc in docs_by_source.get(source_id, []):
            content = doc["content"]
            lowered_content = content.lower()
            score = sum(1 for term in message_terms if term in lowered_content)
            snippet = content[:700]
            candidates.append((score, f"Quelle {doc['path']}:\n{snippet}"))

    candidates.sort(key=lambda item: item[0], reverse=True)
    top_candidates = [candidate[1] for candidate in candidates[:max_chunks] if candidate[0] > 0]

    if not top_candidates:
        top_candidates = [candidate[1] for candidate in candidates[:max_chunks]]

    return top_candidates


def reset_chapter_2_chat() -> None:
    st.session_state.chapter_2_chat = [
        {
            "role": "assistant",
            "content": (
                "Chat wurde zurückgesetzt. Ohne Quellen habe ich nur allgemeine Aussagen. "
                "Wähle Unterlagen aus, um mich mit Kontext zu versorgen."
            ),
        }
    ]


def sync_active_chapter() -> None:
    st.session_state.active_chapter = st.session_state.active_chapter_selector


def go_to_learning_path() -> None:
    st.session_state.app_section = "learning"
    st.session_state.active_chapter = "Kapitel 1"


def go_to_knowledge_section() -> None:
    st.session_state.app_section = "knowledge"


def render_start_screen() -> None:
    st.title("RAG Agent Academy")
    st.subheader("Womit möchtest du starten?")
    st.write(
        "Wähle entweder den geführten Lernpfad mit Quiz und interaktivem RAG-System "
        "oder den freien Wissensteil zum Selbstlesen."
    )

    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.markdown("### Lernpfad")
            st.write("Kapitel 1, Quiz und Kapitel 2 mit dem interaktiven RAG-Modell.")
            if st.button("Zum Lernpfad", use_container_width=True):
                go_to_learning_path()
                st.rerun()
    with col_right:
        with st.container(border=True):
            st.markdown("### Wissensteil")
            st.write("Freies Lesen zu RAG, Prompting, Quellen und Mensch-KI-Zusammenarbeit.")
            if st.button("Zum Wissensteil", use_container_width=True):
                go_to_knowledge_section()
                st.rerun()


def render_knowledge_section() -> None:
    st.title("RAG Agent Academy")
    st.subheader("Wissensteil")
    st.write(
        "Dieser Bereich ist unabhängig vom Quiz und Lernpfad. "
        "Hier kannst du Themen nachlesen und Inhalte frei durchgehen."
    )

    topic_titles = [topic["title"] for topic in KNOWLEDGE_TOPICS]
    title_by_id = {topic["id"]: topic["title"] for topic in KNOWLEDGE_TOPICS}
    st.selectbox(
        "Thema wählen",
        options=[topic["id"] for topic in KNOWLEDGE_TOPICS],
        format_func=lambda topic_id: title_by_id[topic_id],
        key="knowledge_topic",
    )

    selected_topic = next(topic for topic in KNOWLEDGE_TOPICS if topic["id"] == st.session_state.knowledge_topic)

    with st.container(border=True):
        st.markdown(f"### {selected_topic['title']}")
        st.write(selected_topic["summary"])
        st.write(selected_topic["details"])

    st.markdown("### Weitere Themen")
    cols = st.columns(len(KNOWLEDGE_TOPICS) - 1)
    col_idx = 0
    for topic in KNOWLEDGE_TOPICS:
        if topic["id"] == selected_topic["id"]:
            continue
        with cols[col_idx]:
            with st.container(border=True):
                st.markdown(f"**{topic['title']}**")
                st.write(topic["summary"])
                if st.button(
                    "Zum Thema",
                    key=f"topic_btn_{topic['id']}",
                    use_container_width=True,
                ):
                    st.session_state.knowledge_topic = topic["id"]
                    st.rerun()
        col_idx += 1

    if st.button("Zurück zur Auswahl", use_container_width=True):
        st.session_state.app_section = "start"
        st.rerun()


def render_chapter_switcher() -> None:
    chapter_options = ["Kapitel 1"]
    if st.session_state.chapter_1_passed:
        chapter_options.append("Kapitel 2")

    if st.session_state.active_chapter not in chapter_options:
        st.session_state.active_chapter = "Kapitel 1"

    st.session_state.active_chapter_selector = st.session_state.active_chapter

    with st.sidebar:
        st.markdown("## Lernpfad")
        st.selectbox(
            "Kapitel auswählen",
            options=chapter_options,
            key="active_chapter_selector",
            on_change=sync_active_chapter,
        )
        if not st.session_state.chapter_1_passed:
            st.caption("Kapitel 2 wird nur mit 5/5 richtigen Antworten in Kapitel 1 freigeschaltet.")


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
    st.markdown("### Quiz: Prüfe dein Wissen")
    st.write("Beantworte alle Fragen und klicke auf **Auswertung starten**.")
    st.info("Unter jeder Frage kannst du bei Bedarf einen Hinweis aufklappen.")

    def render_stored_quiz_result() -> None:
        if not st.session_state.chapter_1_submitted:
            return

        st.markdown("### Ergebnis")
        for detail in st.session_state.chapter_1_result_details:
            with st.container(border=True):
                st.markdown(f"**Frage {detail['idx']}**")
                if detail["is_correct"]:
                    st.success("Richtig beantwortet.")
                else:
                    st.error("Noch nicht korrekt.")
                st.write(f"Deine Antwort: {detail['user_answer']}")
                st.write(f"Korrekte Antwort: {detail['correct_answer']}")

        score = st.session_state.chapter_1_score
        st.info(f"Du hast {score} von {len(CHAPTER_1_CONTENT)} Fragen korrekt beantwortet.")
        if st.session_state.chapter_1_passed:
            st.success(
                "Stark! Kapitel 1 abgeschlossen. Du bist bereit fuer Kapitel 2: "
                "RAG-Systeme konfigurieren."
            )
            if st.button("Zu Kapitel 2 wechseln", use_container_width=True):
                st.session_state.active_chapter = "Kapitel 2"
                st.rerun()
        else:
            st.warning("Lies die Lernkarten noch einmal und versuche den Quiz erneut.")
            st.info("Kapitel 2 ist gesperrt, bis alle 5 Fragen korrekt beantwortet sind.")

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
        render_stored_quiz_result()
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
    result_details = []

    for idx, item in enumerate(CHAPTER_1_CONTENT, start=1):
        user_answer = answers[idx]
        is_answered = user_answer != "Bitte wählen..."
        is_correct = user_answer == item["correct"]

        if is_correct:
            score += 1
        if is_answered:
            result_details.append(
                {
                    "idx": idx,
                    "user_answer": user_answer,
                    "correct_answer": item["correct"],
                    "is_correct": is_correct,
                }
            )

    st.session_state.chapter_1_score = score
    st.session_state.chapter_1_result_details = result_details
    st.session_state.chapter_1_completed = True
    st.session_state.chapter_1_passed = score == len(CHAPTER_1_CONTENT)
    render_stored_quiz_result()


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
            "1) Symptom genau beobachten, 2) Sensorik pruefen, 3) letzten Eingriff klären. "
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
        "Empfohlener nächster Schritt: Starte mit Sensor LS-4 (Reinigung + Abstand), "
        "danach Referenzlauf. Wenn der Fehler bleibt, pruefe Sternrad-Anschlag und den Sensorhalter auf Spiel."
    )


def generate_real_rag_answer_mistral(
    user_message: str,
    selected_sources: list[str],
    docs_by_source: dict[str, list[dict[str, str]]],
) -> str:
    if Mistral is None:
        return (
            "Mistral SDK ist nicht installiert. Bitte installiere Abhängigkeiten aus requirements.txt "
            "und starte die App neu."
        )

    if not selected_sources:
        return (
            "Fuer echtes RAG musst du mindestens eine Quelle aktivieren, damit Kontext geladen werden kann."
        )

    api_key = get_mistral_api_key()
    if not api_key:
        return (
            "Kein Mistral API Key gefunden. Lege MISTRAL_API_KEY in Streamlit Secrets oder als Umgebungsvariable an."
        )

    context_chunks = retrieve_document_chunks(
        user_message=user_message,
        selected_sources=selected_sources,
        docs_by_source=docs_by_source,
    )
    if not context_chunks:
        return (
            "Es wurden keine Dokumentinhalte gefunden. Pruefe CHAPTER_2_SOURCE_FILE_PATHS und Quelldateien."
        )

    system_prompt = (
        "Du bist ein technischer Assistent fuer Produktionsanlagen. "
        "Antworte ausschliesslich auf Basis des bereitgestellten Kontexts. "
        "Wenn Kontext nicht ausreicht, sage das klar. "
        "Liefere konkrete, sichere Pruefschritte in Reihenfolge."
    )
    rag_context = "\n\n".join(context_chunks)

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                "Kontext aus den verknüpften Unterlagen:\n"
                f"{rag_context}\n\n"
                f"Nutzerfrage: {user_message}"
            ),
        },
    ]

    try:
        client = Mistral(api_key=api_key)
        response = client.chat.complete(model=MISTRAL_MODEL_NAME, messages=messages)
        return response.choices[0].message.content
    except Exception as error:
        return f"Fehler beim Mistral-Aufruf: {error}"


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
    docs_by_source, missing_files = load_script_source_documents()

    options = [source["name"] for source in CHAPTER_2_SOURCES]
    id_by_name = {source["name"]: source["id"] for source in CHAPTER_2_SOURCES}

    selected_names = st.multiselect(
        "Waehle Unterlagen für dein RAG-System",
        options=options,
        default=[source_name_map()[source_id] for source_id in st.session_state.chapter_2_sources],
    )
    st.session_state.chapter_2_sources = [id_by_name[name] for name in selected_names]

    st.markdown("### Schritt 1b: Betriebsmodus")
    st.radio(
        "Chat-Modus",
        options=["Simulation (Regelbasiert)", "Echtes RAG (Mistral, Platzhalter)"],
        key="chapter_2_mode",
        horizontal=True,
    )

    st.caption("Dateiquellen werden serverseitig aus dem Skript geladen (kein Nutzer-Upload).")
    if missing_files:
        st.warning(
            "Einige konfigurierte Quellen wurden nicht gefunden: " + ", ".join(missing_files)
        )

    with st.expander("Geladene Quell-Dateien (aus Skript)"):
        has_any_doc = False
        for source in CHAPTER_2_SOURCES:
            source_docs = docs_by_source.get(source["id"], [])
            if source_docs:
                has_any_doc = True
                st.markdown(f"**{source['name']}**")
                for doc in source_docs:
                    st.write(f"- {doc['path']}")
        if not has_any_doc:
            st.write("Noch keine Quelldateien gefunden. Passe CHAPTER_2_SOURCE_FILE_PATHS an.")

    with st.expander("Mistral-Integration (Platzhalter)"):
        api_key_available = "Ja" if get_mistral_api_key() else "Nein"
        st.write(f"API Key in Secrets/Env gefunden: {api_key_available}")
        st.code(
            """# Laufzeitquellen fuer API-Key
# 1) .streamlit/secrets.toml -> MISTRAL_API_KEY="..."
# 2) Umgebungsvariable -> export MISTRAL_API_KEY="..."
#
# Im Modus "Echtes RAG" wird ein echter Mistral-Call ausgeführt.
""",
            language="python",
        )

    info_cols = st.columns(len(CHAPTER_2_SOURCES))
    for idx, source in enumerate(CHAPTER_2_SOURCES):
        with info_cols[idx]:
            enabled = "Verbunden" if source["id"] in st.session_state.chapter_2_sources else "Nicht verbunden"
            st.metric(source["name"], enabled)
            st.caption(source["description"])

    action_col_1, action_col_2 = st.columns([1, 1])
    with action_col_1:
        if st.button("Chat zurücksetzen", use_container_width=True):
            reset_chapter_2_chat()
            st.rerun()
    with action_col_2:
        if st.button("Zurück zu Kapitel 1", use_container_width=True):
            st.session_state.active_chapter = "Kapitel 1"
            st.rerun()

    st.markdown("### Schritt 2: Mit dem Chatbot arbeiten")
    st.caption("Tipp: Frage zuerst ohne Quellen und dann mit Handbuch + Stoermeldungen.")

    for message in st.session_state.chapter_2_chat:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_prompt = st.chat_input("Stelle dem Chatbot eine Frage zur Situation...")
    if user_prompt:
        st.session_state.chapter_2_chat.append({"role": "user", "content": user_prompt})
        if st.session_state.chapter_2_mode == "Simulation (Regelbasiert)":
            assistant_answer = generate_chapter_2_answer(
                user_message=user_prompt,
                selected_sources=st.session_state.chapter_2_sources,
            )
        else:
            assistant_answer = generate_real_rag_answer_mistral(
                user_message=user_prompt,
                selected_sources=st.session_state.chapter_2_sources,
                docs_by_source=docs_by_source,
            )
        st.session_state.chapter_2_chat.append({"role": "assistant", "content": assistant_answer})
        st.rerun()



def main() -> None:
    init_state()

    if st.session_state.app_section == "start":
        render_start_screen()
        return

    if st.session_state.app_section == "knowledge":
        render_knowledge_section()
        return

    render_chapter_switcher()

    if st.session_state.active_chapter == "Kapitel 2" and not st.session_state.chapter_1_passed:
        st.session_state.active_chapter = "Kapitel 1"

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
