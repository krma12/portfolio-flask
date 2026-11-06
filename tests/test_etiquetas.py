from etiquetas import etiquetas_visibles, categoria_de


def test_quita_variantes_y_genericos():
    lista = ["Python", "Gemini API", "Gemini API Key", "Groq", "Groq API", "AI Assistants", "LLM"]
    assert etiquetas_visibles(lista) == ["Python", "Gemini API", "Groq", "LLM"]


def test_no_toca_etiquetas_distintas():
    lista = ["Kali Linux", "Networking", "SMB", "SMBGhost"]
    assert etiquetas_visibles(lista) == lista


def test_categoria_por_prioridad():
    assert categoria_de(["Python", "LLM", "Cybersecurity"]) == "ai"
    assert categoria_de(["Kali Linux", "CVE"]) == "security"
    assert categoria_de(["Python", "OpenCV"]) == "vision"
    assert categoria_de(["Python", "Pandas"]) == "data"
    assert categoria_de(["HTML", "CSS"]) == "web"
    assert categoria_de(["Python", "Pygame"]) == "games"
    assert categoria_de(["Rust"]) == "other"
