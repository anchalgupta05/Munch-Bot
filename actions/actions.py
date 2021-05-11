# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType

import datetime

class ActionRestaurantForm(Action):
    def name(self) -> Text:
        return "user_details_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        required_slots = ["number", "section", "time"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None: # whatever slot not filled will be requested to user to fill next
                return [SlotSet("requested_slot", slot_name)]

        return [SlotSet("requested_slot", None)]

class ValidateForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_details_form"

    # def checkInt(self, s):
    #     try: 
    #         int(s)
    #         return True
    #     except ValueError:
    #         return False

    def validate_number(self, slot_value: any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        # check_float = isinstance(float(slot_value), float)
        # if float(slot_value) != int(slot_value):
        # if self.checkInt(slot_value):
        #     if int(slot_value) > 0:
        #         return {"number": slot_value}
        #     # if check_float != int(slot_value):
        # dispatcher.utter_message("You have input erroneous number of seats. Please give valid number of seats!")
        # return {"number": None}
        return {"number": slot_value}

    def validate_section(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        slot_value = slot_value.upper()
        if slot_value == 'AC':
            return {"section": slot_value}
        elif slot_value == 'NON-AC':
            return {"section": slot_value}
        else: 
            dispatcher.utter_message("You have input erroneous section. Please give either AC or Non-AC as section!")
            return {"section": None}

    def validate_time(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        # slot_value = slot_value.upper()
        h = int(slot_value[11:13])
        m = int(slot_value[14:16])
        if h >= 19 and h <= 21:
            slot_value = str(h-12) + ':'
            if m >= 30:
                slot_value = slot_value + str(30)
            elif m >= 0:
                slot_value = slot_value + str(0) + str(0)
            slot_value = slot_value + ' PM'
            return {"time": slot_value}

        dispatcher.utter_message(response="utter_incorrect_time")
        return {"time": None}

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_reserved_thanks", Seats=tracker.get_slot("number"), Section=tracker.get_slot("section"), Time=tracker.get_slot("time"))

