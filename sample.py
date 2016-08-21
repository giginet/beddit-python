from beddit.client import BedditClient
from datetime import datetime, timedelta
import os

password = os.environ['BEDDIT_PASSWORD']
access_token = os.environ['BEDDIT_ACCESS_TOKEN']
if None: #access_token:
    client = BedditClient(access_token=access_token)
else:
    client = BedditClient(username="giginet.net@gmail.com", password=password)
sleeps = client.get_sleeps(start=datetime(2016, 8, 15), end=datetime(2016, 8, 16))
for sleep in sleeps:
    print(sleep.date.strftime('%Y-%m-%d') ,sleep.property.total_sleep_score)

#updated_after = datetime.now() - timedelta(7)
#sessions = client.get_sessions(updated_after=updated_after)
#for session in sessions:
#    print(session.start.strftime('%Y-%m-%d'))

user = client.get_user()
print(user.name)
print(client.invite_to_group(email="giginet.net@gmail.com"))
