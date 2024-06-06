from random import random


class RSUTransmission:

    def __init__(self):
        pass

    def transmit_object_list(self, objects):

        vru_present = False
        vru_located = False

        if not objects.empty: # Wenn objekte da sind wird geschaut ob sie erkannt werden und auch lokalisiert werden
            if random() < 0.9: # 99% chance Objekte zu erkennen
                if random() < 0.75: # 95% Chance objecte nach erkennung auch zu lokalisieren
                    vru_present = True
                    vru_located = True
                else:
                    vru_present = True
                    vru_located = False
            else:
                vru_present = False
                vru_located = False

        if vru_located:
            objects_transmitted = self.sending_vru_location(objects)
        elif vru_present:
            objects_transmitted = self.sending_vru_present(objects)
        else:
            objects_transmitted = self.sending_no_vru(objects)

        transmission_successful = self.transmit_objects()

        return objects_transmitted, vru_present, vru_located, transmission_successful

    def sending_no_vru(self, objects):
        objects_transmitted = objects
        return objects_transmitted

    def sending_vru_present(self, objects):
        objects_transmitted = objects
        return objects_transmitted

    def sending_vru_location(self, objects):
        objects_transmitted = objects
        return objects_transmitted

    def transmit_objects(self):
        if random() < 0.95: # 95% of transisition are succesful
            transmission_succesful = True
        else:
            transmission_succesful = False
        return transmission_succesful


