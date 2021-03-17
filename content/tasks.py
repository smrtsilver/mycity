
from jdatetime import timedelta

from content.models import base_content
import schedule
import time

def delete_old_foos(jmodels=None):
    # Query all the foos in our database
    foos = base_content.objects.all()

    # Iterate through them
    for foo in foos:

        # If the expiration date is bigger than now delete it
        if foo.expiration_date < jmodels.timezone.now():
            foo.delete_post()
            # log deletion

schedule.every(10).seconds.do(delete_old_foos)
# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

