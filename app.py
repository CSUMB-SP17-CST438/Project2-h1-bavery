import os
import flask
import flask_socketio
import requests

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)


@app.route('/')
def hello():
    return flask.render_template('index.html', facebook_id = os.environ['facebook_app_id'], google_id = os.environ['google_client_id'])

@socketio.on('connect')
def on_connect():
    print 'Someone connected!'
    
    socketio.emit('all numbers', {
        'numbers': all_mah_numbers
    })
    

@socketio.on('disconnect')
def on_disconnect():
    print 'Someone disconnected!'

all_mah_numbers = []
user_list = []

@socketio.on('new number')
def on_new_number(data):
    if (data['facebook_user_token'] != ''):
        response= requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token='+data['facebook_user_token'])
        json= response.json()
        
        print "Got an event for new number with data:", data
        all_mah_numbers.append({
            'name': json['name'],
            'picture': json['picture']['data']['url'],
            'message':data['message'],
        })
        containsFlag = 0
        for x in user_list:
            if json['name'] == x['user']:
                containsFlag = 1
        if containsFlag == 0:
            user_list.append({'user': json['name']})
            
    elif (data['google_user_token'] != ''):
        response= requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='+data['google_user_token'])
        json= response.json()
        
        print "Got an event for new number with data:", data
        all_mah_numbers.append({
            'name': json['name'],
            'picture': json['picture'],
            'message':data['message'],
        })
        containsFlag = 0
        for x in user_list:
            if json['name'] == x['user']:
                containsFlag = 1
        if containsFlag == 0:
            user_list.append({'user': json['name']})
            
   
    socketio.emit('all numbers', {
        'numbers': all_mah_numbers
    })
    
    socketio.emit('user list', {
        'users': user_list
    })

socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
)

