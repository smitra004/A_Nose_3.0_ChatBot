from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# This dictionary is our internal knowledge base for specific pollutants.
POLLUTANT_DB = {
    "carbon monoxide": "Carbon Monoxide (CO) is a toxic gas produced by incomplete burning of fuels. In high concentrations, it reduces oxygen in the bloodstream.",
    "co": "Carbon Monoxide (CO) is a toxic gas produced by incomplete burning of fuels. In high concentrations, it reduces oxygen in the bloodstream.",
    "sulphur dioxide": "Sulphur Dioxide (SO₂) is a gas from burning fossil fuels like coal and oil. It harms the respiratory system and contributes to acid rain.",
    "so2": "Sulphur Dioxide (SO₂) is a gas from burning fossil fuels like coal and oil. It harms the respiratory system and contributes to acid rain.",
    "ozone": "Ground-level Ozone (O₃) is a major pollutant created when sunlight reacts with emissions from vehicles and industry. It is a key component of smog.",
    "nitrogen dioxide": "Nitrogen Dioxide (NO₂) comes from burning fuel, mainly from vehicles and power plants. It can irritate the respiratory system.",
    "no2": "Nitrogen Dioxide (NO₂) comes from burning fuel, mainly from vehicles and power plants. It can irritate the respiratory system.",
    "pm2.5": "PM2.5 are fine inhalable particles that can travel deep into the respiratory tract, reaching the lungs and causing serious health issues.",
    "pm10": "PM10 are coarse inhalable particles from sources like dust and construction. They can irritate the eyes, nose, and throat."
}

class ActionExplainPollutant(Action):

    def name(self) -> Text:
        return "action_explain_pollutant"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pollutants = tracker.get_latest_entity_values("pollutant")
        
        if not pollutants:
            dispatcher.utter_message(text="I'm sorry, I don't recognize that pollutant. I can tell you about CO, SO2, Ozone, PM2.5, and PM10.")
            return []

        responses = []
        for p in pollutants:
            description = POLLUTANT_DB.get(p.lower())
            if description:
                responses.append(description)
            else:
                responses.append(f"I don't have information on '{p}'.")
        
        dispatcher.utter_message(text="\n\n".join(responses))
        return []