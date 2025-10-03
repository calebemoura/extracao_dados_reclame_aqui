def normalize_text(texto: str ) -> str
    texto_sujo = texto
    texto_limpo = []

    mapa_limpeza = [
        # Vogais minúsculas com acento
        ('á', 'a'), ('à', 'a'), ('â', 'a'), ('ã', 'a'),
        ('é', 'e'), ('ê', 'e'),
        ('í', 'i'),
        ('ó', 'o'), ('ô', 'o'), ('õ', 'o'),
        ('ú', 'u'),
        ('ç', 'c'),
        ('ü', 'u'),
        # Símbolos e Pontuação (para serem removidos)
        ('.', ''), (',', ''), (';', ''), (':', ''), ('?', ''), ('!', ''),
        ('-', ''), ('_', ''), ('\'', ''), ('"', ''), ('/', ''), ('\\', ''),
        ('|', ''), ('(', ''), (')', ''), ('[', ''), (']', ''), ('{', ''),
        ('}', ''), ('<', ''), ('>', ''), ('@', ''), ('#', ''), ('$', ''),
        ('%', ''), ('&', ''), ('*', ''), ('+', ''), ('=', ''), ('~', ''),
        ('`', ''), ('^', ''), ('°', ''), ('§', ''), ('¢', '')
    ]

    for palavra in texto_sujo.strip().lower().split(' '):
        for letra in palavra:
            for letra_nova in mapa_limpeza:
                if letra == letra_nova[0]:
                palavra = palavra.replace(letra, letra_nova[1])
        
        texto_limpo.append(palavra)

    return '-'.join(filter(lambda x: x != '', texto_limpo))