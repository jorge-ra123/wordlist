import os
import random

# Datos provistos con "mimi" incluido
nombres = ["danicsa", "milo", "abigail", "angeles", "tatiana", "matias", "mimi"]
fechas_base = {
    "danicsa": ["02", "12", "1984", "84", "0212", "1202", "02121984", "12021984", "dic1984", "dic84"],
    "abigail": ["14", "12", "2003", "03", "1412", "1214", "14122003", "12142003", "dic2003", "dic03"],
    "tatiana": ["06", "04", "2008", "08", "0604", "0406", "06042008", "04062008", "abr2008", "abr08"],
    "matias": ["06", "12", "2011", "11", "0612", "1206", "06122011", "12062011", "dic2011", "dic11"],
    "milo": ["1984", "84"],
    "angeles": ["2003", "03"],
    "mimi": []  # Puedes añadir aquí sus fechas específicas si las tienes (ej: ["15", "08"])
}

# Rango masivo calibrado para inyectar volumen balanceado con el nuevo nombre
sufijos_num = [str(i) for i in range(1100)]
secuencias = ["123", "1234", "12345", "123456", "1234567", "12345678", "123456789", "0123", "1111", "0000"]
anios_extra = [str(y) for y in range(1950, 2031)]
sufijos_num.extend(secuencias)
sufijos_num.extend(anios_extra)

conectores = ["", "y", "con", "o", "en", "_", ".", "-", "and", "&"]
simbolos = ["", "!", "@", "#", "$", "*", "?", ".", "_", "-", "+", "/", "!!", "@@", "**", "##", "123"]


def get_cases(w):
    res = [w.lower(), w.capitalize(), w.upper()]
    leet1 = w.translate(str.maketrans("aeioult", "4310517"))
    leet2 = w.capitalize().translate(str.maketrans("aeioult", "4310517"))
    leet3 = w.upper().translate(str.maketrans("AEIOULT", "4310517"))
    res.extend([leet1, leet2, leet3])
    return list(set(res))


archivo_salida = "wordlist_80m_mimi_mezclada.txt"
print(f"[*] Creando tu diccionario masivo incluyendo a 'mimi' en: {archivo_salida}")

contador = 0
buffer_escritura = []
LIMITE_BUFFER = 3000000  # Mezcla activamente en bloques de 3 millones de líneas

with open(archivo_salida, "w", encoding="utf-8") as f:
    # 1. Combinaciones individuales (ej: mimi123, M1m1!)
    for n in nombres:
        cases = get_cases(n)
        sufijos_totales = list(set(fechas_base.get(n, []) + sufijos_num))
        for c in cases:
            for s in simbolos:
                for suf in sufijos_totales:
                    buffer_escritura.append(f"{c}{s}{suf}\n")
                    contador += 1

    # 2. Combinaciones de todos contra todos con conectores (ej: mimiyatias, miloconmimi)
    for n1 in nombres:
        cases1 = get_cases(n1)
        for n2 in nombres:
            if n1 == n2: continue
            cases2 = get_cases(n2)
            fechas_par = list(set(fechas_base.get(n1, []) + fechas_base.get(n2, []) + sufijos_num))

            for c1 in cases1:
                for c2 in cases2:
                    for con in conectores:
                        base_compuesta = f"{c1}{con}{c2}"
                        for s in simbolos:
                            for suf in fechas_par:
                                buffer_escritura.append(f"{base_compuesta}{s}{suf}\n")
                                contador += 1

                                if len(buffer_escritura) >= LIMITE_BUFFER:
                                    random.shuffle(buffer_escritura)  # Mezcla total de todos los nombres
                                    f.writelines(buffer_escritura)
                                    buffer_escritura.clear()
                                    print(
                                        f"[+] Escribiendo... {contador // 1000000} millones de líneas mezcladas con éxito.")

    if buffer_escritura:
        random.shuffle(buffer_escritura)
        f.writelines(buffer_escritura)

print(f"\n[¡LOGRADO!] Archivo finalizado con {contador:,} contraseñas únicas.")
