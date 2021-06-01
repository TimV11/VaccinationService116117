# Set "Impfzentren" on those towns where you would like to check.
# The "executable_path" of your webdriver needs to point on your geckodriver.exe


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

from whatsapp_message import send_wa

class BiontechBot:
    
    def __init__(self,):
        self.bot = webdriver.Firefox(executable_path =  "geckodriver.exe")
        self.wait_time = 4

    def login(self, impfzentrum_nr):
        bot = self.bot
        try:
            ## Seite öffnen
            bot.get("https://www.impfterminservice.de/impftermine")
            time.sleep(5)

            ## Cookies bestätigen
            bot.find_element_by_xpath("/html/body/app-root/div/div/div/div[2]/div[2]/div/div[2]/a").click()

            ## Bundesland auswählen
            bot.find_element_by_xpath('/html/body/app-root/div/app-page-its-center/div/div[2]/div/div/div/div/form/div[3]/app-corona-vaccination-center/div[1]/label/span[2]/span[1]/span').click()
            bundeslaender = bot.find_elements_by_class_name("select2-results__option")
            bundeslaender[1].click()

            ## Impfzentrum auswählen
            bot.find_element_by_xpath('/html/body/app-root/div/app-page-its-center/div/div[2]/div/div/div/div/form/div[3]/app-corona-vaccination-center/div[2]/label/span[2]/span[1]/span').click()
            impfzentren = bot.find_elements_by_class_name("select2-results__option")
            impfzentren[impfzentrum_nr].click()

            ## Button "Zum Impfzentrum"
            bot.find_element_by_xpath("/html/body/app-root/div/app-page-its-center/div/div[2]/div/div/div/div/form/div[4]/button").click()
            time.sleep(2)

            ## Warteraum?
            try:
                if bot.find_element_by_xpath("/html/body/section/div[2]/div/div/h1").text == "Virtueller Warteraum des Impfterminservice":
                    print("Waiting Room " + str(impfzentrum_nr))
                    bot.close()
                    return

            ## Cookies bestätigen
            except NoSuchElementException:
                bot.find_element_by_xpath("/html/body/app-root/div/div/div/div[2]/div[2]/div/div[2]/a").click()
            
            ## Impfanspruch prüfen
                bot.find_element_by_xpath("/html/body/app-root/div/app-page-its-login/div/div/div[2]/app-its-login-user/div/div/app-corona-vaccination/div[2]/div/div/label[2]/span").click()
                termin_da = False
                time.sleep(self.wait_time)
            
            ## Ist lila Feld da?
                try: text = bot.find_element_by_xpath("/html/body/app-root/div/app-page-its-login/div/div/div[2]/app-its-login-user/div/div/app-corona-vaccination/div[3]/div/div/div/div[2]/div/div/div").text
                except NoSuchElementException: 
                    print("Termin")
                    termin_da = True
                else:
                    if text == "Bitte warten, wir suchen verfügbare Termine in Ihrer Region.":
                        print("braucht zu lange")
                        self.wait_time += 0.5
                    elif text.startswith("Es wurden keine"):
                        print("keine Termine")
                    else:
                        termin_da = True
                bot.close()

                if termin_da:
                    send_wa("Termin! Zentrum:{" + impfzentrum_nr + "}")
        except Exception as e:
            print(e)
            send_wa("116117 not available - check Internet connection")


send_wa("start")
impfzentren = [7,8,12]
while True:
    try:
        for i in impfzentren:
            bot = BiontechBot()
            bot.login(i)
    except Exception as e:
        send_wa(e)

### NOTES ###