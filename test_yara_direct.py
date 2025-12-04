import yara
import os

# Cargar reglas YARA
rules = yara.compile(filepath="rules/malware.yar")

# Archivo de prueba
test_file = r"C:\Users\Memotito\Desktop\EDR_TEST\DECRYPT_YOUR_FILES.txt"

print("="*60)
print("PRUEBA DIRECTA DE REGLAS YARA")
print("="*60)
print(f"\nArchivo: {test_file}")
print(f"Existe: {os.path.exists(test_file)}\n")

# Escanear archivo
matches = rules.match(test_file)

if matches:
    print(f"DETECCIONES ENCONTRADAS: {len(matches)}\n")
    for match in matches:
        print(f"Regla: {match.rule}")
        print(f"Tags: {match.tags}")
        print(f"Strings encontradas:")
        for string_match in match.strings:
            print(f"  - {string_match}")
        print()
else:
    print(" NO SE DETECTARON AMENAZAS\n")

print("="*60)
