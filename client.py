# -------------------- IMPORTS -------------------- #
import requests
# ------------------------------------------------- #


# -------------------- CONST ---------------------- #
BASE_URL = "http://localhost:8081"
USER_SERVICE = "user_service"
MESSAGE_SERVICE = "message_service"
CHANNEL_SERVICE = "channel_service"
STATS_SERVICE = "stats_service"


# -------------------- AUTH ----------------------- #
JWT_TOKEN = None
# ------------------------------------------------- #


# ------------------------------------------------- #


# -------------------- FONCTIONS ------------------ #

def do_request(method, route, host, **kwargs):
    global JWT_TOKEN
    try:
        print(f"{BASE_URL}{route}")
        print(f"{host}.localhost")

        headers = {"Host": f"{host}.localhost"}
        if JWT_TOKEN:
            headers["Authorization"] = f"Bearer {JWT_TOKEN}"

        res = requests.request(method, f"{BASE_URL}{route}", headers=headers, **kwargs)
        print(f"\n[{res.status_code}] {method} {route}")
        try:
            data = res.json()

            # Si un token est présent dans la réponse, on le stocke
            if "token" in data:
                JWT_TOKEN = data["token"]
                print("Jeton JWT reçu et stocké.")

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
    print("/user              -> Routes dynamiques sur utilisateur")
    print("/msg               -> Routes dynamiques sur messages")
    print("/channel           -> Routes dynamiques sur canaux")
    print("/get_channel       -> Liste des canaux publics")
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


def interactive_subroute(category):
    known_routes = {
        "user": [
            "user/<pseudo>/password", "user/status", "user/avatar/<pseudo>",
            "user/roles/<pseudo> (GET)", "user/roles/<pseudo> (POST)",
            "user/<pseudo> (DELETE)", "make-admin/<pseudo>"
        ],
        "msg": [
            "msg", "msg?channel", "msg/reaction (POST)", "msg/reaction (DELETE)",
            "msg/<id> (PUT)", "msg/<id> (DELETE)",
            "msg/thread/<id>", "msg/pinned?channel", "msg/private", "msg/search"
        ],
        "channel": [
            "channel (POST)", "channel/<nom>/users",
            "channel/<nom> (PATCH)", "channel/<nom>/topic", "channel/<nom>/mode",
            "channel/<nom>/config", "channel/<nom>/invite", "channel/<nom>/ban",
            "channel/<nom> (DELETE)"
        ]
    }

    print(f"\n===== Routes disponibles pour {category.upper()} =====")
    for route in known_routes.get(category, []):
        print(f"/{route}")
    print("Tapez /<route> ou 'exit' pour revenir.\n")

    while True:
        sub = input(f"/{category} >>> ").strip()
        if sub.lower() in ["exit", "quit"]:
            break
        if sub.startswith("/"):
            sub = sub[1:]  # enlever le /
        full_path = f"/{category}/{sub}".replace("//", "/")
        dynamic_route(full_path)


def dynamic_route(path):
    segments = path.strip("/").split("/")
    if not segments:
        print("Route vide.")
        return

    category = segments[0]
    subroute = "/" + "/".join(segments[1:])
    full_path = f"/{category}{subroute}"

    # Détection du service cible
    service = {
        "user": USER_SERVICE,
        "msg": MESSAGE_SERVICE,
        "channel": CHANNEL_SERVICE
    }.get(category)

    if not service:
        print("Service inconnu.")
        return

    # Définition des routes connues
    raw_known_routes = {
        "user": {
            "/user/<pseudo>/password": ("PATCH", [("ancien", str), ("nouveau", str)]),
            "/user/status": ("POST", [("pseudo", str), ("status", str)]),
            "/user/avatar/<pseudo>": ("GET", []),
            "/user/roles/<pseudo>": ("GET", []),
            "/user/roles/<pseudo>": ("POST", [("role", str)]),
            "/user/<pseudo>": ("DELETE", []),
            "/make-admin/<pseudo>": ("POST", [])
        },
        "msg": {
            "/msg": ("POST", [("channel", str), ("text", str)]),
            "/msg?channel": ("GET", [("channel", str)]),
            "/msg/reaction": ("POST", [("message_id", int), ("emoji", str)]),
            "/msg/reaction": ("DELETE", [("message_id", int), ("emoji", str)]),
            "/msg/<id>": ("PUT", [("text", str)]),
            "/msg/<id>": ("DELETE", []),
            "/msg/thread/<id>": ("GET", []),
            "/msg/pinned?channel": ("GET", [("channel", str)]),
            "/msg/private": ("GET", [("from", str), ("to", str)]),
            "/msg/search": ("GET", [("q", str)])
        },
        "channel": {
            "/channel": ("POST", [("name", str), ("private", lambda x: x.lower() == "true")]),
            "/channel/<nom>/users": ("GET", []),
            "/channel/<nom>": ("PATCH", [("topic", str), ("mode", str)]),
            "/channel/<nom>/topic": ("POST", [("topic", str)]),
            "/channel/<nom>/mode": ("POST", [("mode", str)]),
            "/channel/<nom>/config": ("GET", []),
            "/channel/<nom>/invite": ("POST", [("pseudo", str)]),
            "/channel/<nom>/ban": ("POST", [("pseudo", str), ("reason", str)]),
            "/channel/<nom>": ("DELETE", [])
        }
    }

    # Affichage des routes connues
    if category in raw_known_routes:
        print(f"\nRoutes connues pour {category.upper()} :")
        for route, (method, params) in raw_known_routes[category].items():
            param_str = ", ".join(p[0] for p in params) if params else "—"
            print(f"  {method:6} {route:40}  ← {param_str}")
        print()

    # Trouver toutes les routes qui matchent structurellement
    candidates = []
    for route_template, (method, params) in raw_known_routes.get(category, {}).items():
        route_parts = route_template.strip("/").split("/")
        if len(route_parts) != len(segments):
            continue

        is_match = all(
            t == p or (t.startswith("<") and t.endswith(">"))
            for t, p in zip(route_parts, segments)
        )

        if is_match:
            candidates.append((route_template, method, params))

    if not candidates:
        print("Aucune route connue ne correspond.")
        return

    # Si plusieurs méthodes possibles, demander laquelle utiliser
    methods_possible = list(set(m for _, m, _ in candidates))
    if len(methods_possible) > 1:
        print(f"Plusieurs méthodes disponibles pour {full_path} : {', '.join(methods_possible)}")
        method = input("Méthode HTTP à utiliser ? > ").strip().upper()
    else:
        method = methods_possible[0]

    # Trouver les bons paramètres pour cette méthode
    for route_template, m, params in candidates:
        if m == method:
            json_data = {}
            for key, conv in params:
                val = input(f"{key} ? > ").strip()
                try:
                    json_data[key] = conv(val)
                except Exception:
                    print(f"Erreur : valeur invalide pour {key}.")
                    return

            if method in ["POST", "PATCH", "PUT"]:
                do_request(method, full_path, service, json=json_data)
            elif method == "GET":
                full_path += "?" + "&".join(f"{k}={v}" for k, v in json_data.items())
                do_request(method, full_path, service)
            else:
                do_request(method, full_path, service)

            return

    print("Méthode non prise en charge pour cette route.")


        
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
        
        if command in ["user", "msg", "channel"] :
            interactive_subroute(command)
        else :
            match command:
                case "register": register()
                case "login": login()
                case "whois": whois()
                case "seen": seen()
                case "ison": ison()
                case "make-admin": make_admin()
                case "msg": msg()
                case "get_channel": channel()
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