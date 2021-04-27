import logging
import re

def process_text(text):
    #text = re.sub('\s+', ' ', text).strip()
    text = re.sub(r'(\n)+', r'\1', text).lower()
    with open("Messages.txt", "a") as f:
        f.write(text + "\n\n")
    contacts = []
    resources = []
    tags = []
    location = []
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
    for match in re.finditer('#[0-9A-Za-z]*', text):
        tags.append(match.group())
    for match in re.finditer('(urgent)|(request)|(need)|(required)|(fraud)|(fake)|(require)', text):
        tags.append("#"+match.group())
    for match in re.finditer(cities_reg, text):
        location.append("#" + match.group())
    ret = ""
    if contacts:
        ret += "*Contacts*: " + " ".join(list(set(contacts))) + "\n"
    if resources:
        ret += "*Resources*: " + " ".join(list(set(resources))) + "\n"
    if tags:
        ret += "*Tags*: " + " ".join(list(set(tags))) + "\n"
    if location:
        ret += "*Location*: " + " ".join(list(set(location))) + "\n"
    return ret
