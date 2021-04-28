import logging
import regex as re

from utils import contains_iter
from regex_cities import cities_list

class TextResult():
    def __init__(self, full_text, contacts = [], resources = [], location = [],
                 tags = [], msg_type = ""):
        self.contacts = contacts
        self.resources = resources
        self.location = location
        self.tags = tags
        self.msg_type = ""
        self.full_text = full_text

    def generate_reply(self):
        text = ""
        if(self.contacts):
            text+="*Contacts*: " + " ".join(self.contacts) + "\n"
        if(self.resources):
            text+="*Resources*: " + " ".join(map(lambda x: "#"+x, self.resources)) + "\n"
        if(self.location):
            text+="*Location*: " + " ".join(map(lambda x: "#"+x, self.location)) + "\n"
        if(self.tags):
            text+="*Tags*: " + " ".join(map(lambda x: "#"+x, self.tags)) + "\n"

        return text

    @staticmethod
    def from_text(text):
        d, msg_type = process_text(text)
        result = TextResult(text, d["Contacts"], d["Resources"], d["Location"], d["Tags"], msg_type)
        return result
  
def process_text(text):
    #text = re.sub('\s+', ' ', text).strip()
    text = re.sub(r'(\n)+', r'\1', text).lower()
    with open("Messages.txt", "a") as f:
        f.write(text + "\n\n")
    contacts = []
    resources = []
    tags = []
    location = []
    message_type = ""
    for match in re.finditer(
            '\+?([0-9-]|\s|\([0-9]+\)){4,20}[0-9]', #r"[0-9][0-9 ]{3,}",
            text
    ):
        x = match.group()
        if sum([c.isdigit() for c in x]) < 6:
            continue
        contacts.append(x.strip())
        
    for match in re.finditer('#[0-9A-Za-z]*', text):
        tags.append(match.group()[1:])

    for match in contains_iter(['oxygen', 'cylinder', 'ventilator', 'plasma', 'bed', 'icu', 'refill', 'ambulance', 'food', 'remdisivir', 'hospital', 'remdesivir', 'concentrator', 'beds', 'home icu', 'favipiravir', 'tocilizumab', 'fabiflu', 'test', 'tests'], text, "{i<=1,s<=1,d<=1,i+d+s<=1}"):
        resources.append(match)
        message_type = "resource"

    for match in contains_iter(['urgent', 'request', 'need', 'required', 'fraud', 'fake', 'require'], text):
        tags.append(match)

    for match in contains_iter(["urgent", "require", "need", "please", "pls", "request"], text):
        message_type = "request"

    for match in contains_iter(cities_list, text, "{i<=1,s<=1,d<=1,i+d+s<=1}"):
        location.append(match)

    ret = {}
    ret["Contacts"] = list(set(contacts))
    ret["Resources"] = list(set(resources))
    ret["Tags"] = list(set(tags))
    ret["Location"] = list(set(location))
    print()
    return ret, message_type
