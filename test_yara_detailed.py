import yara

# Test individual de strings YARA
test_content = """YOUR FILES HAVE BEEN ENCRYPTED!

To decrypt your files, send 1 Bitcoin to:
1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa

Visit: http://xyz123abc.onion for instructions"""

print("Contenido del archivo:")
print("-" * 60)
print(test_content)
print("-" * 60)
print()

# Cargar reglas
rules = yara.compile(filepath="rules/malware.yar")

# Test con string match
print("Buscando coincidencias individuales:")
print(f"  'your files have been encrypted' en contenido: {'your files have been encrypted' in test_content.lower()}")
print(f"  'bitcoin' en contenido: {'bitcoin' in test_content.lower()}")
print(f"  'decrypt' en contenido: {'decrypt' in test_content.lower()}")
print(f"  'ransom' en contenido: {'ransom' in test_content.lower()}")
print(f"  '.onion' en contenido: {'.onion' in test_content.lower()}")
print()

# Escanear con YARA
matches = rules.match(data=test_content.encode())

print(f"Resultados YARA: {len(matches)} regla(s) detectada(s)")
for match in matches:
    print(f"\nRegla: {match.rule}")
    if match.strings:
        print("Strings que coincidieron:")
        for s in match.strings:
            print(f"  - Instance: {s}")
