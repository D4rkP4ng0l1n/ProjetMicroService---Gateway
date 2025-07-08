# -------------------- IMPORTS -------------------- #
import requests
# ------------------------------------------------- #


# -------------------- CONST ---------------------- #
BASE_URL = "http://localhost:8081"
USER_SERVICE = "user_service"
MESSAGE_SERVICE = "message_service"
CHANNEL_SERVICE = "channel_service"
STATS_SERVICE = "stats_service"
# ------------------------------------------------- #


# -------------------- FONCTIONS ------------------ #

def do_request(method, route, host, **kwargs):
    try:
        res = requests.request(method, f"{BASE_URL}{route}", headers={"Host": f"{host}.localhost"}, **kwargs)
        print(f"\n[{res.status_code}] {method} {route}")
        try:
            data = res.json()
            if data.get("status") == "ok":
                print("Succès :")
                print_json(data["reponse"])
            elif data.get("status") == "ko":
                print("Erreur :")
                print(f"{data['reponse']}")
            else:
                print("Format inattendu :", data)
        except ValueError:
            print("Erreur : réponse non JSON :", res.text)
    except requests.exceptions.ConnectionError:
        print("Connexion au service impossible.")
    except Exception as e:
        print("Erreur inattendue :", e)
        

def commands_list():
    print("\nCommandes disponibles :")
    print("/register          -> Créer un compte utilisateur")
    print("/login             -> Authentifier un utilisateur")
    print("/whois             -> Infos publiques sur un utilisateur")
    print("/seen              -> Dernière activité d'un utilisateur")
    print("/ison              -> Utilisateurs connectés")
    print("/make-admin        -> Donner le rôle admin")
    print("/user/*            -> Routes dynamiques sur utilisateur")
    print("/msg/*             -> Routes dynamiques sur messages")
    print("/channel/*         -> Routes dynamiques sur canaux")
    print("/stats             -> Statistiques")
    print("/help              -> Affiche cette aide")
    print("/exit              -> Quitter CanaDuck\n")
    
    
def print_json(data):
    if isinstance(data, dict):
        for key, val in data.items():
            print(f"  - {key} : {val}")
    elif isinstance(data, list):
        for i, item in enumerate(data):
            print(f"  [{i}] {item}")
    else:
        print(data)
    
    
def register():
    print("Créer un compte utilisateur")
    do_request("POST", "/register", USER_SERVICE)


def login():
    print("Authentifier l'utilisateur")
    do_request("POST", "/login", USER_SERVICE)


def whois():
    pseudo = input("Pseudo ? > ").strip()
    if pseudo:
        do_request("GET", f"/whois/{pseudo}", USER_SERVICE)


def seen():
    pseudo = input("Pseudo ? > ").strip()
    if pseudo:
        do_request("GET", f"/seen/{pseudo}", USER_SERVICE)


def ison():
    users = input("Liste des pseudos séparés par des virgules ? > ").strip()
    if users:
        do_request("GET", f"/ison?users={users}", USER_SERVICE)


def make_admin():
    pseudo = input("Pseudo à promouvoir admin ? > ").strip()
    if pseudo:
        do_request("POST", f"/make-admin/{pseudo}", USER_SERVICE)


def msg():
    channel = input("Nom du canal ? > ").strip()    
    if channel:
        do_request("GET", f"/msg?channel={channel}", MESSAGE_SERVICE)


def channel():
    do_request("GET", "/channel", CHANNEL_SERVICE)


def user() :
    pass

def stats():
    print("\nStatistiques disponibles :")
    print("1 -> Canaux les plus actifs")
    print("2 -> Messages par heure")
    print("3 -> Messages par utilisateur")
    print("4 -> Messages les plus réactés")
    choix = input("Numéro ? > ").strip()
    path_map = {
        "1": "/stats/active-channels",
        "2": "/stats/hourly-activity",
        "3": "/stats/messages-per-user",
        "4": "/stats/top-reacted-messages"
    }
    if choix in path_map:
        do_request("GET", path_map[choix], STATS_SERVICE)


def dynamic_route(path):
    segments = path.strip("/").split("/")
    if not segments:
        print("Route vide.")
        return

    category = segments[0]
    subroute = "/" + "/".join(segments[1:])
    method = input("Méthode HTTP (GET, POST, PATCH, DELETE) ? > ").strip().upper()

    # Routes connues avec prompts personnalisés
    known_routes = {
        "user": {
            "/user/status": {
                "method": "POST",
                "params": [("pseudo", str), ("status", str)]
            },
            "/user/roles": {
                "method": "POST",
                "params": [("pseudo", str), ("role", str)]
            },
            "/user/<pseudo>/password": {
                "method": "PATCH",
                "params": [("ancien", str), ("nouveau", str)]
            }
        },
        "msg": {
            "/msg/reaction": {
                "method": "POST",
                "params": [("message_id", int), ("emoji", str)]
            },
            "/msg/private": {
                "method": "GET",
                "params": [("from", str), ("to", str)]
            }
        },
        "channel": {}
    }

    payload = {}

    if category in known_routes:
        matched = False
        for route_key, route_info in known_routes[category].items():
            if route_key in path or "<pseudo>" in route_key and len(segments) >= 3:
                print(f"Remplissage automatique des champs pour {path}")
                json_data = {}
                for key, typ in route_info["params"]:
                    val = input(f"{key} ? > ").strip()
                    json_data[key] = typ(val)
                payload = {"json": json_data}
                matched = True
                break

        if not matched:
            # Si la route n'est pas connue alors on a une erreur
            pass

    # Exécuter la requête
    service = {
        "user": USER_SERVICE,
        "msg": MESSAGE_SERVICE,
        "channel": CHANNEL_SERVICE
    }.get(category)

    if service:
        route = f"/{category}{subroute}"
        do_request(method, route, service, **payload)
    else:
        print("Service inconnu.")

        
# -------------------- BOUCLE PRINCIPALE ------------------ #

def main():
    print("==================== CanaDuck ====================\n")
    print("Bienvenue sur CanaDuck !")
    commands_list()

    while True:
        cmd = input(">>> ").strip()
        if not cmd.startswith("/"):
            print("Une commande commence par `/`.")
            continue

        command = cmd[1:]
        
        if ( command.startswith("user") or command.startswith("channel") or command.startswith("msg")) :
            dynamic_route('/' + command)
        else :
            match command:
                case "register": register()
                case "login": login()
                case "whois": whois()
                case "seen": seen()
                case "ison": ison()
                case "make-admin": make_admin()
                case "msg": msg()
                case "channel": channel()
                case "stats": stats()
                case "help": commands_list()
                case "exit":
                    print("\nMerci d'avoir utilisé CanaDuck 🦆")
                    print("==================================================")
                    break
                case _:
                    print("Commande inconnue, tape /help.")

# ------------------------------------------------- #
    
if __name__ == "__main__":
    main()