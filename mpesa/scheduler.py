from apscheduler.schedulers.background import BackgroundScheduler

from mpesa.voldermort.utils import generate_access_token

def updateMpesaAccessToken():
    generate_access_token()


                
def start():
    schedule = BackgroundScheduler()
    schedule.add_job(updateMpesaAccessToken, 'interval', minutes=3)
    schedule.start()