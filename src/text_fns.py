import logging
import re

from utils import contains_iter

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
            text+="*Resources*: " + " ".join(self.resources) + "\n"
        if(self.location):
            text+="*Location*: " + " ".join(self.location) + "\n"
        if(self.tags):
            text+="*Tags*: " + " ".join(self.tags) + "\n"

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
    for match in re.finditer('(oxygen)|(cylinder)|(ventilator)|(plasma)|(bed)|(icu)|(refill)|(ambulance)|(food)|(remdisivir)|(hospital)|(remdesivir)|(concentrator)', text):
        resources.append("#"+match.group())
        message_type = "resource"
    for match in re.finditer('#[0-9A-Za-z]*', text):
        tags.append(match.group())
    for match in re.finditer('(urgent)|(request)|(need)|(required)|(fraud)|(fake)|(require)', text):
        tags.append("#"+match.group())
    for match in contains_iter(["urgent", "require", "need", "please", "pls", "request"], text):
        message_type = "request"
    for match in re.finditer(cities_reg, text):
        location.append("#" + match.group())
    ret = {}
    ret["Contacts"] = list(set(contacts))
    ret["Resources"] = list(set(resources))
    ret["Tags"] = list(set(tags))
    ret["Location"] = list(set(location))
    return ret, message_type
