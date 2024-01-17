import json
import requests
from bs4 import BeautifulSoup


class NtuityRequestClass:
    def __init__(self, temp_id, temp_bearer, temp_user, temp_password):
        self.id = temp_id
        self.bearer = temp_bearer
        self.user = temp_user
        self.password = temp_password
        
        self.ntuitycurrentdata = ""
        self.ntuitytotaldata = ""

        self.power_consumption = 0
        self.power_consumption_calc = 0
        self.power_production = 0
        self.power_storage = 0
        self.power_grid = 0
        self.power_charging_stations = 0
        self.power_heating = 0
        self.power_appliances = 0
        self.state_of_charge = 0
        self.self_sufficiency = 0
        self.consumers_total_count = 0
        self.consumers_online_count = 0
        self.producers_total_count = 0
        self.producers_online_count = 0
        self.storages_total_count = 0
        self.storages_online_count = 0
        self.heatings_total_count = 0
        self.heatings_online_count = 0
        self.charging_points_total_count = 0
        self.charging_points_online_count = 0
        self.grids_total_count = 0
        self.grids_online_count = 0

        self.total_success = False
        self.total_status_code = False
        self.total_production = 0.0
        self.total_consumption = 0.0
        self.total_imported = 0.0
        self.total_exported = 0.0
        self.total_charged = 0.0
        self.total_discharged = 0.0
        self.total_co2_savings = 0.0
        self.total_profit = 0.0
        self.total_autarky = 0.0
        self.total_currency = ""
        self.total_grouping = ""


        self.get_current_values()
        #self.get_total_values()
        self.login()

        self.readValues()

        #print(self.ntuitycurrentdata)
        #print(self.ntuitytotaldata)

    def get_current_values(self):

        url = ("https://api.ntuity.io/v1/sites/" + self.id + "/energy-flow/latest")

        headers = {
            "accept": "application/json",
            "authorization": "Bearer " + self.bearer
        }

        response = requests.get(url, headers=headers)

        #print(response.text)
        self.ntuitycurrentdata = response.json()

    def get_total_values(self):

        url = "https://navi.ntuity.io/api/v1/sites/" + self.id + "/production_and_consumption"
        params = {
            'from': '2021-01-01',
            'to': '2099-01-31',
            'totals_only': 'true'
        }
        headers = {
            "authorization": "Bearer " + self.login_bearer
        }

        login_data = {
            'username': self.user,
            'password': self.password
        }

        response = requests.get(url, params=params, data=login_data)

        if response.status_code == 200:
            #print(response.text)
            self.ntuitytotaldata = response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")

    def login(self):
        # Ziel-URL
        login_url = "https://navi.ntuity.io/users/sign_in"

        # Benutzername und Passwort
        username = self.user
        password = self.password

        # Sitzung starten
        session = requests.Session()

        # Zuerst die Anmeldeseite öffnen, um CSRF-Token zu erhalten
        response = session.get(login_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # CSRF-Token extrahieren
        csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']

        # Daten für die POST-Anfrage vorbereiten
        login_data = {
            'utf8': '✓',
            'authenticity_token': csrf_token,
            'user[email]': username,
            'user[password]': password,
            'user[remember_me]': '0'
        }

        # POST-Anfrage für die Anmeldung senden
        response = session.post(login_url, data=login_data)

        # Überprüfen, ob die Anmeldung erfolgreich war
        if response.ok:
            True
        else:
            print("Fehler beim Anmelden. Statuscode:", response.status_code)
            print(response.text)  # Hier können Sie die Antwort für weitere Fehleranalyse ausgeben

        url = "https://navi.ntuity.io/api/v1/sites/" + self.id + "/production_and_consumption"
        params = {
            'from': '2021-01-01',
            'to': '2099-01-31',
            'totals_only': 'true'
        }
        #headers = {
        #    "authorization": "Bearer " + self.login_bearer
        #}

        login_data = {
            'username': self.user,
            'password': self.password
        }

        response = session.get(url, params=params, data=login_data)

        if response.status_code == 200:
            #print(response.text)
            self.ntuitytotaldata = response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")

    def readValues(self):
        self.power_consumption = self.ntuitycurrentdata["power_consumption"]["value"]
        self.power_consumption_calc = self.ntuitycurrentdata["power_consumption_calc"]["value"]
        self.power_production = self.ntuitycurrentdata["power_production"]["value"]
        self.power_storage = self.ntuitycurrentdata["power_storage"]["value"]
        self.power_grid = self.ntuitycurrentdata["power_grid"]["value"]
        self.power_charging_stations = self.ntuitycurrentdata["power_charging_stations"]["value"]
        self.power_heating = self.ntuitycurrentdata["power_heating"]["value"]
        self.power_appliances = self.ntuitycurrentdata["power_appliances"]["value"]
        self.state_of_charge = self.ntuitycurrentdata["state_of_charge"]["value"]
        self.self_sufficiency = self.ntuitycurrentdata["self_sufficiency"]["value"]
        self.consumers_total_count = self.ntuitycurrentdata["consumers_total_count"]
        self.consumers_online_count = self.ntuitycurrentdata["consumers_online_count"]
        self.producers_total_count = self.ntuitycurrentdata["producers_total_count"]
        self.producers_online_count = self.ntuitycurrentdata["producers_online_count"]
        self.storages_total_count = self.ntuitycurrentdata["storages_total_count"]
        self.storages_online_count = self.ntuitycurrentdata["storages_online_count"]
        self.heatings_total_count = self.ntuitycurrentdata["heatings_total_count"]
        self.heatings_online_count = self.ntuitycurrentdata["heatings_online_count"]
        self.charging_points_total_count = self.ntuitycurrentdata["charging_points_total_count"]
        self.charging_points_online_count = self.ntuitycurrentdata["charging_points_online_count"]
        self.grids_total_count = self.ntuitycurrentdata["grids_total_count"]
        self.grids_online_count = self.ntuitycurrentdata["grids_online_count"]

        self.total_success = self.ntuitytotaldata["success"]
        self.total_status_code = self.ntuitytotaldata["status_code"]
        self.total_production = self.ntuitytotaldata["totals"]["production"]
        self.total_consumption = self.ntuitytotaldata["totals"]["consumption"]
        self.total_imported = self.ntuitytotaldata["totals"]["imported"]
        self.total_exported = self.ntuitytotaldata["totals"]["exported"]
        self.total_charged = self.ntuitytotaldata["totals"]["charged"]
        self.total_discharged = self.ntuitytotaldata["totals"]["discharged"]
        self.total_co2_savings = self.ntuitytotaldata["totals"]["co2_savings"]
        self.total_profit = self.ntuitytotaldata["totals"]["profit"]
        self.total_autarky = self.ntuitytotaldata["totals"]["autarky"]
        self.total_currency = self.ntuitytotaldata["currency"]
        self.total_grouping = self.ntuitytotaldata["grouping"]

    def get_power_consumption(self):
        return self.power_consumption
    def get_power_consumption_calc(self):
        return self.power_consumption_calc
    def get_power_production(self):
        return self.power_production
    def get_power_storage(self):
        return self.power_storage
    def get_power_grid(self):
        return self.power_grid
    def get_power_charging_stations(self):
        return self.power_charging_stations
    def get_power_heating(self):
        return self.power_heating
    def get_power_appliances(self):
        return self.power_appliances
    def get_state_of_charge(self):
        return self.state_of_charge
    def get_self_sufficiency(self):
        return self.self_sufficiency
    def get_consumers_total_count(self):
        return self.consumers_total_count
    def get_consumers_online_count(self):
        return self.consumers_online_count
    def get_producers_total_count(self):
        return self.producers_total_count
    def get_producers_online_count(self):
        return self.producers_online_count
    def get_storages_total_count(self):
        return self.storages_total_count
    def get_storages_online_count(self):
        return self.storages_online_count
    def get_heatings_total_count(self):
        return self.heatings_total_count
    def get_heatings_online_count(self):
        return self.heatings_online_count
    def get_charging_points_total_count(self):
        return self.charging_points_total_count
    def get_charging_points_online_count(self):
        return self.charging_points_online_count
    def get_grids_total_count(self):
        return self.grids_total_count
    def get_grids_online_count(self):
        return self.grids_online_count
    def get_total_success(self):
        return self.total_success
    def get_total_status_code(self):
        return self.total_status_code
    def get_total_production(self):
        return self.total_production
    def get_total_consumption(self):
        return self.total_consumption
    def get_total_imported(self):
        return self.total_imported
    def get_total_exported(self):
        return self.total_exported
    def get_total_charged(self):
        return self.total_charged
    def get_total_discharged(self):
        return self.total_discharged
    def get_total_co2_savings(self):
        return self.total_co2_savings
    def get_total_profit(self):
        return self.total_profit
    def get_total_autarky(self):
        return self.total_autarky
    def get_total_currency(self):
        return self.total_currency
    def get_total_grouping(self):
        return self.total_grouping
