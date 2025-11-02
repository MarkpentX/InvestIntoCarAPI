from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import UserModel

URL = "postgresql://car_invest_db_user:ltf13EyjtMt4Fca9L2CcD9kzHzJysLxj@dpg-d410ic8dl3ps73dd6r1g-a.oregon-postgres.render.com/car_invest_db"

engine = create_engine(URL)
Session = sessionmaker(bind=engine)
session = Session()

session.query(UserModel).delete()
session.commit()
session.close()