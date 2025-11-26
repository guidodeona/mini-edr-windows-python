import os
import datetime

LOG_DIR = "logs"

def crear_informe(alertas_detectadas, alertas_criticas):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"{LOG_DIR}/informe_{timestamp}.txt"
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("========== INFORME DE SEGURIDAD ==========\n")
        f.write(f"Fecha y hora: {datetime.datetime.now()}\n\n")
        
        f.write("---- RIESGOS DETECTADOS / COSAS A VIGILAR ----\n")
        if alertas_detectadas:
            for a in alertas_detectadas:
                f.write(f"- {a}\n")
        else:
            f.write("No se detectaron riesgos leves.\n")
        
        f.write("\n---- PROBLEMAS CRÍTICOS / POSIBLES INFECCIONES ----\n")
        if alertas_criticas:
            for a in alertas_criticas:
                f.write(f"- {a}\n")
        else:
            f.write("No se detectaron problemas críticos.\n")
    
    print(f"\n📄 Informe generado: {nombre_archivo}\n")
    return nombre_archivo
