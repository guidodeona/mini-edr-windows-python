import winreg
from utils.alertas import print_alert

def scan_registry(config, collect_alerts=False):
    leves = []
    criticas = []

    if "registry_scanner" not in config or not config["registry_scanner"].get("enabled", False):
        return {"leves": leves, "criticas": criticas}

    print_alert("🔍 Escaneando registro (persistencia)...", "info")

    rutas_persistencia = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunOnce")
    ]

    suspicious_keywords = config["registry_scanner"].get("suspicious_keywords", ["cmd.exe", "powershell.exe", "wscript.exe", "temp"])

    for hive, subkey in rutas_persistencia:
        try:
            with winreg.OpenKey(hive, subkey) as key:
                num_values = winreg.QueryInfoKey(key)[1]
                for i in range(num_values):
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        # Check for suspicious content in the value (command)
                        for keyword in suspicious_keywords:
                            if keyword.lower() in str(value).lower():
                                msg = f"Persistencia sospechosa detectada: [{name}] -> {value}"
                                print_alert(f"[ALERTA] {msg}", "danger")
                                if collect_alerts:
                                    criticas.append(msg)
                    except OSError:
                        continue
        except OSError:
            # Key might not exist or permission denied
            continue

    return {"leves": leves, "criticas": criticas}
