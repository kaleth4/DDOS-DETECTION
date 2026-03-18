<div align="center">
 
```
██████╗  ██████╗ ███████╗    ██████╗ ███████╗████████╗███████╗ ██████╗████████╗ ██████╗ ██████╗ 
██╔══██╗██╔═══██╗██╔════╝    ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
██║  ██║██║   ██║███████╗    ██║  ██║█████╗     ██║   █████╗  ██║        ██║   ██║   ██║██████╔╝
██║  ██║██║   ██║╚════██║    ██║  ██║██╔══╝     ██║   ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
██████╔╝╚██████╔╝███████║    ██████╔╝███████╗   ██║   ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
╚═════╝  ╚═════╝ ╚══════╝    ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
```
 
# 🛡️ DoS Detection Tool
 
**Herramienta de detección de ataques de Denegación de Servicio en tiempo real.**  
Monitorea tráfico de red, identifica patrones anómalos y bloquea IPs ofensoras automáticamente.
 
---
 
[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Security](https://img.shields.io/badge/Categoría-Blue_Team-0077ff?style=for-the-badge&logo=shield&logoColor=white)](https://github.com/)
[![Threading](https://img.shields.io/badge/Módulo-Threading-orange?style=for-the-badge)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-00ff41?style=for-the-badge)](https://github.com/)
 
</div>
 
---
 
## 📌 ¿Qué es un ataque DoS?
 
Un ataque **Denial of Service (DoS)** tiene como objetivo abrumar un sistema con tráfico masivo para dejarlo inoperativo. Los usuarios legítimos no pueden acceder al servicio.
 
```
TRÁFICO NORMAL:                  ATAQUE DoS:
                                                  
  Usuario A ──┐                  Atacante ──────────────────────┐
  Usuario B ──┤──→ Servidor ✅   Atacante ──────────────────────┤──→ Servidor 💥
  Usuario C ──┘                  Atacante ──────────────────────┘
  
  ~10 req/seg                    ~10,000 req/seg → COLAPSO
```
 
| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **DoS** | Un solo atacante satura el servidor | SYN Flood |
| **DDoS** | Miles de IPs atacan simultáneamente | Botnet Attack |
| **UDP Flood** | Paquetes UDP masivos a puertos aleatorios | Volumétrico |
| **ICMP Flood** | Ping flood para saturar el ancho de banda | Smurf Attack |
 
---
 
## ⚙️ ¿Cómo funciona la herramienta?
 
```
┌──────────────────────────────────────────────────────────────┐
│                   FLUJO DE DETECCIÓN                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  📡 Paquete recibido                                         │
│       ↓                                                      │
│  📋 Registrar IP + timestamp en ventana de tiempo           │
│       ↓                                                      │
│  🔢 Calcular tasa: paquetes / segundos                       │
│       ↓                                                      │
│  ⚖️  ¿Supera el umbral? (100 pkt/seg default)               │
│      ├── NO  →  ✅ Tráfico normal — continuar               │
│      └── SÍ  →  🚨 ALERTA emitida                          │
│                    ↓                                         │
│               🔒 IP añadida a lista negra                   │
│                    ↓                                         │
│               📊 Registro en reporte final                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```
 
---
 
## 🖥️ Demo de salida
 
```bash
==================================================
  🛡️  DoS DETECTION TOOL — WolvesTI 2026
==================================================
  1. Iniciar monitoreo en tiempo real
  2. Simular ataque DoS (prueba)
  3. Ver estadísticas de tráfico
  4. Ver reporte de alertas
  5. Salir
==================================================
  Selecciona una opción (1-5): 2
 
  IP atacante (Enter=203.0.113.99): [Enter]
  ⚠️  Simulando ataque DoS desde 203.0.113.99...
  ⚡ Monitor activo por 15 segundos...
 
============================================================
  🚨 ALERTA DE SEGURIDAD — 2026-03-15 14:32:07
  Tipo     : DoS — Flood de paquetes
  IP       : 203.0.113.99
  Tasa     : 187.4 paquetes/segundo
  Detalles : Supera umbral de 100 pkt/s sostenido
============================================================
 
  🔒 [14:32:07] IP BLOQUEADA: 203.0.113.99
  💡 Producción: iptables -A INPUT -s 203.0.113.99 -j DROP
```
 
```bash
  IP                   Total pkt       En ventana      Estado
  ─────────────────────────────────────────────────────────────────
  192.168.1.10         12              8               ✅ Normal
  192.168.1.20         9               5               ✅ Normal
  10.0.0.5             15              7               ✅ Normal
  203.0.113.99         800             0               🔒 BLOQUEADA
```
 
---
 
## 📂 Estructura del proyecto
 
```
dos-detection-tool/
│
├── 📄 dos_detector.py        # Herramienta principal
├── 📄 README.md              # Documentación
└── 📁 logs/
    └── alertas_sesion.txt    # (opcional) exportar reportes
```
 
---
 
## 🚀 Instalación y uso
 
```bash
# 1. Clonar el repositorio
git clone https://github.com/kaleth4/dos-detection-tool.git
cd dos-detection-tool
 
# 2. Sin dependencias externas requeridas
python --version   # Python 3.8+
 
# 3. Ejecutar
python dos_detector.py
```
 
> ✅ **No requiere librerías externas** — usa solo la librería estándar de Python.
 
---
 
## 🔬 Conceptos de seguridad aplicados
 
| Concepto | Implementación en el código |
|----------|-----------------------------|
| **Rate Limiting** | Umbral de paquetes/segundo por IP |
| **Sliding Window** | Ventana de tiempo deslizante de 5s |
| **IP Blacklisting** | Lista negra con bloqueo automático |
| **DDoS Detection** | Análisis de múltiples fuentes simultáneas |
| **Threading** | Monitoreo concurrente sin bloquear UI |
| **Disponibilidad (CIA)** | Proteger el pilar de disponibilidad |
 
---
 
## ⚠️ Consideraciones importantes
 
```
✅  Usar en entornos de laboratorio o con permiso explícito
✅  Ideal para aprender Blue Team y detección de anomalías
✅  Base para integrar con herramientas como Suricata o Snort
❌  No ejecutar contra sistemas sin autorización escrita
❌  No reemplaza un IDS/IPS en producción (Suricata, Wazuh)
```
 
---
 
## 🔮 Mejoras futuras
 
- [ ] 📡 Captura de paquetes reales con `scapy` o `pyshark`
- [ ] 📊 Dashboard visual con `Flask` + gráficas en tiempo real
- [ ] 📧 Notificaciones por email/Slack al detectar ataques
- [ ] 🗃️ Exportar alertas a CSV / JSON / SIEM
- [ ] 🔁 Integración con `iptables` real en Linux
- [ ] 🤖 Machine Learning para detección de anomalías
 
---
 
## 👤 Autor
 
**Kaleth Corcho**  
Ingeniería de Sistemas · WolvesTI · Bogotá, Colombia
 
[![LinkedIn](https://img.shields.io/badge/LinkedIn-kaleth--corcho-0077B5?style=flat&logo=linkedin)](https://linkedin.com)
[![GitHub](https://img.shields.io/badge/GitHub-kaleth4-181717?style=flat&logo=github)](https://github.com/kaleth4)
 
---
 
<div align="center">
 
**⭐ Si este proyecto te fue útil, dale una estrella**
 
*Proyecto de portafolio en ciberseguridad · Blue Team · 2026 · WolvesTI*
 
</div>
