#!/usr/bin/env python3
# ============================================================
#   DoS DETECTION TOOL — Herramienta de Detección de Ataques DoS
#   Autor: Kaleth Corcho | WolvesTI | 2026
# ============================================================
 
import time
import random
import threading
from collections import defaultdict
from datetime import datetime
 
# ── CONFIGURACIÓN ──────────────────────────────────────────
UMBRAL_PAQUETES   = 100   # Paquetes por segundo antes de alertar
UMBRAL_CONEXIONES = 50    # Conexiones únicas por IP
VENTANA_TIEMPO    = 5     # Segundos de ventana de análisis
IPS_EN_LISTA_NEGRA = set()
 
registro_trafico  = defaultdict(list)
contador_paquetes = defaultdict(int)
alertas_emitidas  = []
lock = threading.Lock()
 
 
def registrar_paquete(ip_origen, protocolo="TCP", puerto_destino=80):
    """Registra la llegada de un paquete y limpia registros viejos."""
    ahora = time.time()
    with lock:
        registro_trafico[ip_origen].append(ahora)
        contador_paquetes[ip_origen] += 1
        registro_trafico[ip_origen] = [
            t for t in registro_trafico[ip_origen]
            if ahora - t <= VENTANA_TIEMPO
        ]
 
 
def detectar_dos(ip_origen):
    """Analiza si una IP supera el umbral de paquetes por segundo."""
    with lock:
        paquetes_recientes = len(registro_trafico[ip_origen])
    tasa = paquetes_recientes / VENTANA_TIEMPO
    return (True, tasa) if tasa >= UMBRAL_PAQUETES else (False, tasa)
 
 
def detectar_ddos():
    """Detecta DDoS analizando volumen total desde múltiples fuentes."""
    ahora = time.time()
    ips_activas, total_paquetes = 0, 0
    with lock:
        for ip, timestamps in registro_trafico.items():
            recientes = [t for t in timestamps if ahora - t <= VENTANA_TIEMPO]
            if recientes:
                ips_activas += 1
                total_paquetes += len(recientes)
    tasa_total = total_paquetes / VENTANA_TIEMPO
    es_ddos = ips_activas >= 10 and tasa_total >= UMBRAL_PAQUETES * 2
    return es_ddos, total_paquetes, ips_activas
 
 
def emitir_alerta(tipo, ip=None, tasa=0, detalles=""):
    """Registra y muestra una alerta de seguridad."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alertas_emitidas.append({
        "timestamp": timestamp, "tipo": tipo,
        "ip": ip or "MÚLTIPLES", "tasa_pps": round(tasa, 2),
        "detalles": detalles
    })
    print(f"\n{'='*60}")
    print(f"  🚨 ALERTA DE SEGURIDAD — {timestamp}")
    print(f"  Tipo     : {tipo}")
    print(f"  IP       : {ip or 'MÚLTIPLES FUENTES'}")
    print(f"  Tasa     : {round(tasa, 2)} paquetes/segundo")
    print(f"  Detalles : {detalles}")
    print(f"{'='*60}\n")
 
 
def bloquear_ip(ip):
    """Añade la IP a la lista negra y simula bloqueo con iptables."""
    IPS_EN_LISTA_NEGRA.add(ip)
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"  🔒 [{ts}] IP BLOQUEADA: {ip}")
    print(f"  💡 Producción: iptables -A INPUT -s {ip} -j DROP")
 
 
def monitor_continuo(duracion_segundos=30):
    """Monitor de tráfico en tiempo real durante N segundos."""
    print(f"\n  ⚡ Monitor activo por {duracion_segundos} segundos...")
    inicio = time.time()
    while time.time() - inicio < duracion_segundos:
        time.sleep(2)
        with lock:
            ips = list(registro_trafico.keys())
        for ip in ips:
            if ip in IPS_EN_LISTA_NEGRA:
                continue
            es_dos, tasa = detectar_dos(ip)
            if es_dos:
                emitir_alerta("DoS — Flood", ip, tasa,
                              f"Supera {UMBRAL_PAQUETES} pkt/s")
                bloquear_ip(ip)
        es_ddos, total, activas = detectar_ddos()
        if es_ddos:
            emitir_alerta("DDoS — Distribuido", tasa=total/VENTANA_TIEMPO,
                          detalles=f"{activas} IPs atacando simultáneamente")
    print("\n  ✅ Monitoreo finalizado.")
 
 
def simular_trafico_normal():
    """Simula tráfico legítimo para contexto de prueba."""
    ips = ["192.168.1.10", "192.168.1.20", "10.0.0.5", "172.16.0.3"]
    for _ in range(50):
        registrar_paquete(random.choice(ips), "TCP",
                          random.choice([80, 443, 8080]))
        time.sleep(random.uniform(0.05, 0.2))
 
 
def simular_ataque_dos(ip_atacante="203.0.113.99"):
    """Simula ataque DoS enviando paquetes a alta velocidad."""
    print(f"\n  ⚠️  Simulando ataque DoS desde {ip_atacante}...")
    for _ in range(800):
        registrar_paquete(ip_atacante, "UDP", 80)
        time.sleep(0.005)   # ~200 paquetes/segundo
 
 
def ver_estadisticas():
    """Muestra estadísticas del tráfico registrado."""
    ahora = time.time()
    print(f"\n  {'IP':<20} {'Total pkt':<15} {'En ventana':<15} {'Estado'}")
    print("  " + "-"*65)
    with lock:
        for ip, timestamps in registro_trafico.items():
            recientes = len([t for t in timestamps if ahora - t <= VENTANA_TIEMPO])
            total = contador_paquetes[ip]
            estado = "🔒 BLOQUEADA" if ip in IPS_EN_LISTA_NEGRA else \
                     "🚨 SOSPECHOSA" if recientes/VENTANA_TIEMPO >= UMBRAL_PAQUETES \
                     else "✅ Normal"
            print(f"  {ip:<20} {total:<15} {recientes:<15} {estado}")
 
 
def mostrar_reporte():
    """Reporte completo de la sesión de monitoreo."""
    print("\n" + "="*60)
    print("  📊 REPORTE FINAL DE SESIÓN")
    print("="*60)
    print(f"  IPs monitoreadas : {len(registro_trafico)}")
    print(f"  IPs bloqueadas   : {len(IPS_EN_LISTA_NEGRA)}")
    print(f"  Alertas emitidas : {len(alertas_emitidas)}")
    for a in alertas_emitidas:
        print(f"    [{a['timestamp']}] {a['tipo']} — {a['ip']} — {a['tasa_pps']} pkt/s")
    for ip in IPS_EN_LISTA_NEGRA:
        print(f"  🔒 {ip}")
    print("="*60)
 
 
def main():
    while True:
        print("\n" + "="*50)
        print("  🛡️  DoS DETECTION TOOL — WolvesTI 2026")
        print("="*50)
        print("  1. Iniciar monitoreo en tiempo real")
        print("  2. Simular ataque DoS (prueba)")
        print("  3. Ver estadísticas de tráfico")
        print("  4. Ver reporte de alertas")
        print("  5. Salir")
        print("="*50)
        opcion = input("  Selecciona una opción (1-5): ").strip()
 
        if opcion == '1':
            dur = input("  Duración en segundos (default 30): ").strip()
            t = threading.Thread(target=monitor_continuo,
                                 args=(int(dur) if dur.isdigit() else 30,))
            t.start(); t.join()
        elif opcion == '2':
            ip = input("  IP atacante (Enter=203.0.113.99): ").strip() or "203.0.113.99"
            for fn in [simular_trafico_normal, lambda: simular_ataque_dos(ip),
                       lambda: monitor_continuo(15)]:
                threading.Thread(target=fn, daemon=True).start()
            time.sleep(16)
        elif opcion == '3':
            ver_estadisticas()
        elif opcion == '4':
            mostrar_reporte()
        elif opcion == '5':
            print("\n  👋 Saliendo...\n"); break
        else:
            print("\n  ❌ Opción inválida.")
 
if __name__ == "__main__":
    main()