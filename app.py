from flask import Flask, request, redirect
import os, json
from flask_cors import CORS
from Data.actionsDatabase import insertUser, authLogin, insertUserNetwork, authNetworksLogin, savesScheduleDatabase, saveScheduleFiles, getIdQueue, nextSchedules, allSchedules, completedSchedules, deleteScheduleDatabase, updateScheduleDatabase, deleteNetworkDatabase, updateNetworkDatabase
from AutomacaoInstagram.ExtrairInfos import userAutenticateInstagram, alterFilename, validateIsVideos
from werkzeug.utils import secure_filename
import  AutoInstagram
import ssl

app = Flask(__name__)

context = ssl.SSLContext()
context.load_cert_chain('192.168.15.3+4.pem', '192.168.15.3+4-key.pem')

UPLOAD_FOLDER = './temp'
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'SECRET KEY'


cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/auth/social_network", methods=["GET"])
def userAutenticate():
      user = request.args.get('user')
      password = request.args.get('password')
      network = request.args.get('network')

      if network == 'instagram':
            return userAutenticateInstagram(user, password)
      else:
            return userAutenticateInstagram("teste", "teste1234")


@app.route("/auth", methods=["GET"])
def login():
      return authLogin()


@app.route("/register/user_account", methods=["POST"])
def registerUser():
      user = request.json['user']
      password = request.json['password']
      email = request.json['email']
      name = request.json['name']

      return insertUser(user, password, name, email)


@app.route("/register/user_network", methods=["POST"])
def registerUserNetwork():
      user = request.json['user']
      password = request.json['password']
      network = request.json['network']
      id_login = request.json['id_login']

      if network == 'instagram':
            network = 1
      elif network == 'twitter':
            network = 2

      return insertUserNetwork(user, password, network, id_login)


@app.route('/save_schedule', methods=['POST'])
def upload_file():
      if request.method == 'POST':

            isVideos = False
            legend =request.form['input-options-legend']
            date = request.form['input-options-date']
            time = request.form['input-options-time']
            typeSchedule = request.form['input-options-type-schedule']
            networkActive = request.form['input-options-network-active']
            idLogin = request.form['input-options-user-autenticate']

            for file in request.files.getlist('filesSchedules'):           
                  filename = alterFilename(idLogin, date, time, networkActive, secure_filename(file.filename))
                  file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                  if validateIsVideos(filename):
                        isVideos = True

            savesScheduleDatabase(UPLOAD_FOLDER, legend, date, time, typeSchedule, networkActive, idLogin, isVideos)

            id_queue_json = json.loads(getIdQueue(idLogin, date, time, networkActive))

            id_queue = id_queue_json[0]['id_queue']

            for file in request.files.getlist('filesSchedules'):           
                  filename = alterFilename(idLogin, date, time, networkActive, secure_filename(file.filename))
                  saveScheduleFiles(id_queue, filename)

            return redirect('http://187.34.201.58:5000/#/Homepage')


@app.route("/auth/social_network_save", methods=["GET"])
def userNetworkSave():
      id_login = request.args.get('id_login')
      return authNetworksLogin(id_login)


@app.route("/search_next_schedules", methods=["GET"])
def searchNextsSchedules():
      id_login = request.args.get('id_login')
      network_active = request.args.get('network_active')
      return nextSchedules(id_login, network_active)


@app.route("/search_all_schedules", methods=["GET"])
def searchAllSchedules():
      id_login = request.args.get('id_login')
      network_active = request.args.get('network_active')
      return allSchedules(id_login, network_active)


@app.route("/search_completed_schedules", methods=["GET"])
def searchCompletedSchedules():
      id_login = request.args.get('id_login')
      network_active = request.args.get('network_active')
      return completedSchedules(id_login, network_active)


@app.route("/delete_schedule/<idqueue>", methods=["DELETE"])
def deleteSchedule(idqueue):
      return deleteScheduleDatabase(idqueue)


@app.route("/delete_network/<user_login>/<network>", methods=["DELETE"])
def deleteNetwork(user_login, network):
      return deleteNetworkDatabase(user_login, network)


@app.route('/update_schedule', methods=["PUT", "POST"])
def updateSchedule():
      if request.method == 'PUT':
            id_queue = request.json['idqueue']
            date = request.json['date']
            time = request.json['time']
            legend = request.json['legend']
            return updateScheduleDatabase(id_queue, date, time, legend)


@app.route('/update_network', methods=["PUT", "POST"])
def updateNetwork():
      if request.method == 'PUT':
            user = request.json['user']
            network = request.json['network']
            password = request.json['pass']
            return updateNetworkDatabase(user, network, password)


@app.route('/home', methods=["GET"])
def home():
      AutoInstagram.home()
      return 'Sucessfull'


@app.route('/run', methods=["GET"])
def running():
      return 'API is Running'

if __name__ == "__main__":
      app.run (host = '192.168.15.4', port="3000", debug=False)

