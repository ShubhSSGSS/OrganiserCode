from codeDir import app, database, utils
from codeDir.forms import signUpForm, logInForm, planForm
from flask import url_for, render_template, redirect, session, request
from codeDir.models import User, Plan
import json


def loggedIn():
    try:
        sessionUserID =  session['logged-in-user-id']
        return True if not sessionUserID == True else False
    except:
        return False


@app.route('/')
@app.route('/info')
def info():
    #if not loggedIn() == True: return redirect(url_for('login'))

    return render_template('info.html', title='Info')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    signup = signUpForm()

    if signup.validate_on_submit():
        newUser = User(userID = utils.hashGen('UID'),username=signup.usernameField.data, userPin=signup.pinField.data)
        database.session.add(newUser)
        database.session.commit()
        return redirect(url_for('login'))
    else:
        print(signup.errors)

    if loggedIn():
        return redirect(url_for('myplans', planid='all'))
    else:
        return render_template('login.html', title='Log In', form=signup)


@app.route('/login', methods=['POST', 'GET'])
def login():

    logIn = logInForm()
    if logIn.validate_on_submit():
        session['logged-in-user-id'] = User.query.filter_by(username=logIn.usernameField.data).with_entities(User.userID).first()[0]
        return redirect(url_for('myplans', planid='all'))
    else:
        print(logIn.errors)

    if loggedIn():
        return redirect(url_for('myplans', planid='all'))
    else:
        return render_template('login.html', title='Log In', form=logIn)


@app.route('/logout')
def logout():
    session['logged-in-user-id'] = False
    return redirect(url_for('login'))


@app.route('/newplan', methods=['POST', 'GET'])
def newPlan():

    newPlan = planForm()
    if newPlan.validate_on_submit():
        currentUserID = session['logged-in-user-id']
        currentUserPlans = User.query.filter_by(userID=currentUserID).with_entities(User.userPlans).first()[0]    #json string
        plan = Plan(planName=newPlan.planNameField.data, planDesc=newPlan.planDescField.data,
                    planTime=newPlan.planTimeField.data, planLoc=newPlan.planLocField.data,
                    planCreatorID=currentUserID, planMembers=json.dumps({'planMembers':[currentUserID]}),
                    planID = utils.hashGen('PID'))

        User.query.filter_by(userID=currentUserID).update({User.userPlans:utils.dataMerge(currentUserPlans, plan.planID)})
       
        database.session.add(plan)
        database.session.commit()

        return redirect(url_for('myplans', planID='all'))
    else:
        print(newPlan.errors)

    if not loggedIn() == True: return redirect(url_for('login')) 

    return render_template('newplanform.html', form=newPlan)
    
    
@app.route('/myplans')
def myplans():
    #/myplans?planid=value, value=all means allplans

    if not loggedIn() == True: return redirect(url_for('login'))
    
    currentUserID = session['logged-in-user-id']
    planID = request.args.get('planid')
    planObject = None

    userPlans = User.query.filter_by(userID=currentUserID).with_entities(User.userPlans).first()[0]

    if planID == 'all':
        userPlanIDs = [planID for planID in json.loads(userPlans)['userPlans']]
        planObject = Plan.query.filter(Plan.planID.in_(userPlanIDs)).all()
    else:
        if planID in utils.extractData(userPlans, 'userPlans'):
            planObject = Plan.query.get_or_404(planID)
        else:
            return 'You don\'t have access to that plan/The specified plan does not exist.'
        
    return render_template('myplans.html', title='My Plans', plans=planObject, all=planID=='all', inPlan=True)
    

@app.route('/shareplan')
def shareplan():
    #invites if not in, redirects to plan if in

    if not loggedIn() == True: return redirect(url_for('login'))
    
    currentUserID = session['logged-in-user-id']
    planID = request.args.get('planid')
    planObject = Plan.query.get_or_404(planID)

    if currentUserID in utils.extractData(planObject.planMembers, 'planMembers'):
        return redirect(url_for('myplans', planid=planID))
    else:
        return render_template('myplans.html', plans=planObject, host=User.query.get(planObject.planCreatorID).username,
                                inPlan=False, all=False, title='Join Plan', userID = currentUserID)

@app.route('/tasks', methods=['POST', 'GET'])
def tasks():
    #a route built to deal with requests from the front end

    if request.method == 'POST':
        if request.headers.get('task') == 'add-user-to-plan':
            requestBody = request.json
            planID = requestBody['planID']
            userID = requestBody['userID']

            currentPlanMembers = Plan.query.filter_by(planID=planID).with_entities(Plan.planMembers).first()[0]
            currentUserPlans = User.query.filter_by(userID=userID).with_entities(User.userPlans).first()[0]

            Plan.query.filter_by(planID=planID).update({Plan.planMembers:utils.dataMerge(currentPlanMembers, userID)})
            User.query.filter_by(userID=userID).update({User.userPlans:utils.dataMerge(currentUserPlans, planID)})
            database.session.commit()

    else:        
        return json.dumps({'success':False, 'rInfo':'Method/Headers were invalid.'})
    

    


