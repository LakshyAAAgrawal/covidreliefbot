import logging
import re

from CovidAPI import fetch_data_from_API

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import ConversationHandler, CallbackQueryHandler, PicklePersistence

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ParseMode
from PIL import Image
import telegram
import os
import pytesseract
import cv2
import numpy as np
import re

BEGINMSG = "Hi. Welcome to Covid Relief Bot"

MENU, GET_LOCATION = range(2)

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text(
        BEGINMSG,
        #reply_markup = ReplyKeyboardMarkup(
        #    [['Oxygen']
        #     #['Oxygen Bed'], ['Medicine'], ['Plasma'], ['Ambulance'], ['Exit']
        #     ],
        #    one_time_keyboard=True,
        #    resize_keyboard=True
        #),
    )
    return MENU

def exit_convo(update, context):
    start(update, context)
    return MENU

def handle_menu(update, context):
    resource = update.message.text
    context.user_data['resource_wanted'] = resource
    update.message.reply_text("Please enter city")
    return GET_LOCATION

def fetch_info(update, context):
    if 'resource_wanted' not in context.user_data:
        return exit_convo(update, context)
    resource = context.user_data['resource_wanted']
    location = update.message.text
    #update.message.reply_text(fetch_data_from_API(resource, location))
    res_list = fetch_data_from_API(resource, location)
    for resource in res_list:
        context.bot.send_message(chat_id=update.message.chat_id, text=resource, parse_mode = ParseMode.MARKDOWN)
    return exit_convo(update, context)

def preprocess_img(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #img = cv2.GaussianBlur(thresh, (5,5), 0)
    #img = cv2.medianBlur(img,5)
    return img

def process_text(text):
    #text = re.sub('\s+', ' ', text).strip()
    text = re.sub(r'(\n)+', r'\1', text).lower()
    print(text)
    ret = "*Contacts*: "
    for match in re.finditer(
            '\+?([0-9-]|\s|\([0-9]+\)){4,20}[0-9]', #r"[0-9][0-9 ]{3,}",
            text
    ):
        x = match.group()
        if sum([c.isdigit() for c in x]) < 6:
            continue
        ret += x.strip() + ", "
    ret += "\n*Resources*:"
    city_reg = re.compile('(mumbai)|(delhi)|(bangalore)|(hyderabad)|(ahmedabad)|(chennai)|(kolkata)|(surat)|(pune)|(jaipur)|(lucknow)|(kanpur)|(nagpur)|(indore)|(thane)|(bhopal)|(visakhapatnam)|(salem)|(pimpri-chinchwad)|(patna)|(vadodara)|(ghaziabad)|(ludhiana)|(agra)|(nashik)|(ranchi)|(faridabad)|(meerut)|(rajkot)|(kalyan-dombivli)|(vasai-virar)|(varanasi)|(srinagar)|(aurangabad)|(dhanbad)|(amritsar)|(navi mumbai)|(allahabad)|(howrah)|(gwalior)|(jabalpur)|(coimbatore)|(vijayawada)|(jodhpur)|(madurai)|(raipur)|(kota)|(chandigarh)|(guwahati)|(solapur)|(hubli–dharwad)|(mysore)|(tiruchirappalli)|(bareilly)|(aligarh)|(tiruppur)|(gurgaon)|(moradabad)|(jalandhar)|(bhubaneswar)|(warangal)|(mira-bhayandar)|(jalgaon)|(guntur)|(thiruvananthapuram)|(bhiwandi)|(saharanpur)|(gorakhpur)|(bikaner)|(amravati)|(noida)|(jamshedpur)|(bhilai)|(cuttack)|(firozabad)|(kochi)|(nellore)|(bhavnagar)|(dehradun)|(durgapur)|(asansol)|(rourkela)|(nanded)|(kolhapur)|(ajmer)|(akola)|(gulbarga)|(jamnagar)|(ujjain)|(loni)|(siliguri)|(jhansi)|(ulhasnagar)|(jammu)|(sangli-miraj & kupwad)|(mangalore)|(erode)|(belgaum)|(kurnool)|(ambattur)|(rajahmundry)|(tirunelveli)|(malegaon)|(gaya)|(tirupati)|(udaipur)|(kakinada)|(davanagere)|(kozhikode)|(maheshtala)|(rajpur sonarpur)|(bokaro)|(south dumdum)|(bellary)|(patiala)|(gopalpur)|(agartala)|(bhagalpur)|(muzaffarnagar)|(bhatpara)|(panihati)|(latur)|(dhule)|(rohtak)|(sagar)|(korba)|(bhilwara)|(berhampur)|(muzaffarpur)|(ahmednagar)|(mathura)|(kollam)|(avadi)|(kadapa)|(anantapuram)|(kamarhati)|(bilaspur)|(sambalpur)|(shahjahanpur)|(satara)|(bijapur)|(rampur)|(shimoga)|(chandrapur)|(junagadh)|(thrissur)|(alwar)|(bardhaman)|(kulti)|(nizamabad)|(parbhani)|(tumkur)|(khammam)|(uzhavarkarai)|(bihar sharif)|(panipat)|(darbhanga)|(bally)|(aizawl)|(dewas)|(ichalkaranji)|(karnal)|(bathinda)|(jalna)|(eluru)|(barasat)|(kirari suleman nagar)|(purnia)|(satna)|(mau)|(sonipat)|(farrukhabad)|(durg)|(imphal)|(ratlam)|(hapur)|(arrah)|(anantapur)|(karimnagar)|(etawah)|(ambarnath)|(north dumdum)|(bharatpur)|(begusarai)|(new delhi)|(gandhidham)|(baranagar)|(tiruvottiyur)|(pondicherry)|(sikar)|(thoothukudi)|(rewa)|(mirzapur)|(raichur)|(pali)|(ramagundam)|(silchar)|(haridwar)|(vijayanagaram)|(tenali)|(nagercoil)|(sri ganganagar)|(karawal nagar)|(mango)|(thanjavur)|(bulandshahr)|(uluberia)|(katni)|(sambhal)|(singrauli)|(nadiad)|(secunderabad)|(naihati)|(yamunanagar)|(bidhannagar)|(pallavaram)|(bidar)|(munger)|(panchkula)|(burhanpur)|(raurkela industrial township)|(kharagpur)|(dindigul)|(gandhinagar)|(hospet)|(nangloi jat)|(malda)|(ongole)|(deoghar)|(chapra)|(haldia)|(khandwa)|(nandyal)|(morena)|(amroha)|(anand)|(bhind)|(bhalswa jahangir pur)|(madhyamgram)|(bhiwani)|(berhampore)|(ambala)|(morbi)|(fatehpur)|(raebareli)|(khora, ghaziabad)|(chittoor)|(bhusawal)|(orai)|(bahraich)|(phusro)|(vellore)|(mehsana)|(raiganj)|(sirsa)|(danapur)|(serampore)|(sultan pur majra)|(guna)|(jaunpur)|(panvel)|(shivpuri)|(surendranagar dudhrej)|(unnao)|(chinsurah)|(alappuzha)|(kottayam)|(machilipatnam)|(shimla)|(adoni)|(udupi)|(katihar)|(proddatur)|(mahbubnagar)|(saharsa)|(dibrugarh)|(jorhat)|(hazaribagh)|(hindupur)|(nagaon)|(sasaram)|(hajipur)|(port blair)|(giridih)|(bhimavaram)|(kumbakonam)|(bongaigaon)|(dehri)|(madanapalle)|(siwan)|(bettiah)|(ramgarh)|(tinsukia)|(guntakal)|(srikakulam)|(motihari)|(dharmavaram)|(medininagar)|(gudivada)|(phagwara)|(pudukkottai)|(hosur)|(narasaraopet)|(suryapet)|(miryalaguda)|(tadipatri)|(karaikudi)|(kishanganj)|(jamalpur)|(ballia)|(kavali)|(tadepalligudem)|(amaravati)|(buxar)|(tezpur)|(jehanabad)|(aurangabad)|(gangtok)|(vasco da gama)')
    for match in re.finditer('(oxygen)|(cylinder)|(ventilator)|(plasma)|(bed)|(icu)|(refill)|(ambulance)|(food)|(remdisivir)|(hospital)|(remdesivir)', text):
        ret += ' #' + match.group()
    ret +="\n*Tags*:"
    for match in re.finditer('#[0-9A-Za-z]*', text):
        ret += ' ' + match.group()
    for match in re.finditer('(urgent)|(request)|(need)|(required)', text):
        ret += ' #' + match.group()
    ret += "\n*Location*:"
    for match in re.finditer(city_reg, text):
        ret += " #" + match.group()
    if ret == "*Contacts*: \n*Resources*:\n*Tags*:\n*Location*:":
        return ""
    return ret

def handle_photo(update, context):
    for img_dict in update.message['photo'][-1:]:
        file_id = img_dict['file_id']
        imgfile = context.bot.get_file(file_id)
        img_path = imgfile.download()
        image = cv2.imread(img_path)
        text = pytesseract.image_to_string(preprocess_img(image))
        text = process_text(text)
        if text != "":
            update.message.reply_text(text, parse_mode = ParseMode.MARKDOWN)
        os.remove(img_path)

def error(update, context):
    """Log Errors caused by Updates."""
    print(context.error)
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    import json
    with open('config.json') as fp:
        config = json.load(fp)
    persistence = PicklePersistence(filename='conversationbot')
    updater = Updater(config["API_TOKEN"], use_context=True, persistence=persistence)
    dp = updater.dispatcher
    
    # Add Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    login_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [
                #MessageHandler(Filters.regex('^(Oxygen)$'), handle_menu),
                MessageHandler(Filters.photo, handle_photo),
                #MessageHandler(Filters.regex('^(Oxygen Bed)$'), handle_menu),
                #MessageHandler(Filters.regex('^(Medicine)$'), handle_menu),
                #MessageHandler(Filters.regex('^(Plasma)$'), handle_menu),
                #MessageHandler(Filters.regex('^(Ambulance)$'), handle_menu)
            ],
            GET_LOCATION: [MessageHandler(Filters.text, fetch_info)],
        },
        fallbacks=[MessageHandler(Filters.regex('.*'), exit_convo)]
    )

    #dp.add_handler(login_handler)
    
    # log all errors
    dp.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
