from models import Task
from datetime import date
from views import db


#create the db and db table
db.create_all()

#insert data
#db.session.add(Task("Finish the turotial", date(2016, 9, 22), 10, 1))
#db.session.add(Task("Finish real python course", date(2016, 10, 3), 10, 1))

#commit the changes
db.session.commit()

