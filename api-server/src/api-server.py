# coding: utf-8

import json
import logging
from flask import Flask
from flask import  render_template, current_app
from flask_restplus import Api, Resource
from python_terraform import *

from wrappers.ociapi import  OciWrapper
from wrappers.terraform import TerraformWrapper


logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')

app = Flask(__name__)
api = Api(app)

config_path = 'config.json'

# Check if config path is in input, otherwise look
# for config.json in working dir
if len(sys.argv) > 1:
    config_path = sys.argv[1]

cfg = None
try:
    with open(config_path) as config_file:
        cfg = json.load(config_file)
except Exception as e:
    logging.exception('Unable to load config file')

# Init Terraform wrapper
tf_wrapper = None
if cfg and cfg.get('terraform') and cfg.get('terraform').get('tf_path'):
    try:
        tf_wrapper = TerraformWrapper(cfg.get('terraform').get('tf_path'))
    except :
        logging.error('unable to load terraform wrapper')

# Init OCI wrapper
oci_wrapper = None
logging.info(cfg.get('oci'))
if cfg and cfg.get("oci"):
    try:
        oci_wrapper = OciWrapper(cfg.get("oci"))
    except:
        logging.error('unable to load OCI wrapper')
else:
    oci_wrapper = OciWrapper()

# **********************************
# *******   APP DEFINITIONS  *******
# **********************************

'''
 utility method to call api from app
 to be tested
'''
def get_json_response(view_name, *args, **kwargs):
    """
        Calls internal view method, parses json, and returns python dict.
    """
    view = current_app.view_functions[view_name]
    res = view(*args, **kwargs)

    js = json.loads(res.data)
    return js

@app.route('/gui/compartments/list')
def app_oci_compartment():
    r  = get_json_response('api_oci_compartment')
    return render_template('compartments.html.jinja2', compartments=r)


# **********************************
# *******   API DEFINITIONS  *******
# **********************************

@api.route('/compartments/list')
@api.doc()
class APIOciCompartment(Resource):
    """
        provide a list of compartments
    """
    def get(self):
        if not oci_wrapper:
            api.abort(501)
        else:
            compartment_list = oci_wrapper.list_compartments()
            return compartment_list


@api.route('/action/scale/<string:compartment>/<string:instance_name>/<string:shape>')
@api.doc()
class APIOciScale(Resource):
    def get(self,compartment, instance_name, shape):
        if not oci_wrapper:
            api.abort(501)
        else:

            instance_id = oci_wrapper.scale(new_shape=shape,compartment_name=compartment, instance_name=instance_name)
            return {'instance_ocid':instance_id}


# *******   TERRAFORM  ********

@api.route('/apply')
@api.doc()
class APITFApply(Resource):
    def get(self):
        if not tf_wrapper:
            api.abort(501)
        else:
            return_code, stdout, stderr = tf_wrapper.apply()
            if not stderr:
                return {'apply':stdout }
            else:
                return {'apply': return_code, 'error': stderr, 'output': stdout}

    @api.doc(responses={403: 'Not Authorized'})
    def post(self, id):
        api.abort(403)


@api.route('/plan')
class APITFPlan(Resource):
    def get(self):
        if not tf_wrapper:
            api.abort(501)
        else:
            return_code, stdout, stderr = tf_wrapper.plan()
            if not stderr:
                return {'plan': stdout}
            else:
                return {'plan': return_code, 'error': stderr, 'output': stdout}

    @api.doc(responses={403: 'Not Authorized'})
    def post(self, id):
        api.abort(403)


@api.route('/destroy')
class APITFDestroy(Resource):
    def get(self):
        if not tf_wrapper:
            api.abort(501)
        else:
            return_code, stdout, stderr = tf_wrapper.destroy()
            if not stderr:
                return {'destroy': stdout}
            else:
                return {'destroy': return_code, 'error': stderr, 'output': stdout}

    @api.doc(responses={403: 'Not Authorized'})
    def post(self, id):
        api.abort(403)



if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0',port=5000,debug=True,use_reloader=True)