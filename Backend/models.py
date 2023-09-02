from codeDir import database as db


class User(db.Model):

    userID = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    userPin = db.Column(db.Integer, nullable=False)
    userPlans = db.Column(db.Text, default='{"userPlans": []}')
    userConfirms = db.Column(db.Integer, default=0)
    userCancels = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'{self.userID} : {self.username}'
    

class Plan(db.Model):

    planID = db.Column(db.String, primary_key=True)
    planName = db.Column(db.String(20), nullable=False)
    planDesc = db.Column(db.Text)
    planTime = db.Column(db.DateTime, nullable=False)
    planLoc = db.Column(db.String(), nullable=False)
    planCreatorID = db.Column(db.String(), nullable=False)
    planMembers = db.Column(db.String(), default='')
    planConfirms = db.Column(db.Integer, default=0)
    planCancels = db.Column(db.Integer, default=0)


    def __repr__(self):
        return f'{self.planID} : {self.planName} \nCreator : {self.planCreatorID}'
    