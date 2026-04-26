def generar_comb(con_gem, con_cons, tipo, anteriores):
    gemelos = [11, 22, 33, 44]
    
    for _ in range(5000):  # Aumentamos intentos para asegurar precisión
        # 1. Selección de base según tus grupos
        c_desp = random.sample(despertando, 4)
        c_extra = random.sample(hielo_frio_down, 2)
        c_cal_pool = [n for n in calientes if n not in repes]
        c_cal = [random.choice(c_cal_pool if c_cal_pool else calientes)]
        
        c_final = list(set(c_desp + c_extra + c_cal))
        
        # Si al unir grupos no hay 7 únicos, reintentamos
        if len(c_final) < 7: continue
        c_final.sort()

        # --- FILTRO DE DECENAS (REGLA 2-2-1-1-1) ---
        # Calculamos cuántos números hay en cada decena (0:1-10, 1:11-20, etc.)
        conteo_decs = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        for n in c_final:
            idx = (n-1)//10 if n < 50 else 4
            if idx > 4: idx = 4
            conteo_decs[idx] += 1
        
        # REGLA: Ninguna decena vacía Y máximo 2 números por decena
        # Esto obliga a que la distribución sea exactamente [2, 2, 1, 1, 1]
        if any(v == 0 for v in conteo_decs.values()): continue # Evita decenas vacías
        if any(v > 2 for v in conteo_decs.values()): continue  # Evita más de 2 por decena
        
        # --- FILTRO SOLAPAMIENTO (Máx 2 entre combinaciones) ---
        if not validar_solapamiento(c_final, anteriores): continue

        # --- FILTRO PARES/IMPARES ---
        p = [n for n in c_final if n % 2 == 0]
        if tipo == "3P4I" and len(p) != 3: continue
        if tipo == "4P3I" and len(p) != 4: continue

        # --- FILTRO SUMA (131-160) ---
        if not (131 <= sum(c_final) <= 160): continue

        # --- FILTRO GAPS < 18 ---
        if any(c_final[idx+1] - c_final[idx] > 18 for idx in range(6)): continue

        # --- FILTRO GEMELOS (Botón ON/OFF) ---
        pres_gem = [n for n in c_final if n in gemelos]
        if con_gem:
            if len(pres_gem) != 1: continue
        else:
            if len(pres_gem) > 0: continue

        # --- FILTRO CONSECUTIVOS (Botón ON/OFF) ---
        tiene_cons = any(c_final[idx+1] - c_final[idx] == 1 for idx in range(6))
        if con_cons:
            if not tiene_cons: continue # Si está ON y no tiene, descartamos
        else:
            if tiene_cons: continue # Si está OFF y tiene, descartamos

        return c_final
        
    # Si después de 5000 intentos falla (muy raro), genera una aleatoria que cumpla lo básico
    return sorted(random.sample(range(1, 49), 7))
