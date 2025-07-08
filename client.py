import requests

def main():
    try:
        hello_resp = requests.get("http://localhost:80/stats",headers={"Host": "service_tests.localhost"})

        print("Réponse du service Hello :", hello_resp.text)

    except requests.exceptions.RequestException as e:
        print("Erreur lors de l'appel aux services :", e)

if __name__ == "__main__":
    main()
