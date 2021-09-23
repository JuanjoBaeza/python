import phonenumbers
from phonenumbers import carrier

ro_number = phonenumbers.parse("+346292198153", "ES")
carrier.name_for_number(ro_number, "es")

print(ro_number)
print(carrier.name_for_number(ro_number, "es"))