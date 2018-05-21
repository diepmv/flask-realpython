# project/api/views.py


from functools import wraps
from flask import flash, redirect, jsonify, \
    session, url_for, Blueprint, make_response, request

from project import db
from project.models import Task
import openstack

from openstack.exceptions import NotFoundException


################
#### config ####
################

api_blueprint = Blueprint('api', __name__)


##########################
#### helper functions ####
##########################

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap


def open_tasks():
    return db.session.query(Task).filter_by(
        status='1').order_by(Task.due_date.asc())


def closed_tasks():
    return db.session.query(Task).filter_by(
        status='0').order_by(Task.due_date.asc())


def create_connection():
    return openstack.connect(cloud='vccloud')

################
#### routes ####
################

@api_blueprint.route('/api/v1/tasks/')
def api_tasks():
    results = db.session.query(Task).limit(10).offset(0).all()
    json_results = []
    for result in results:
        data = {
            'task_id': result.task_id,
            'task name': result.name,
            'due date': str(result.due_date),
            'priority': result.priority,
            'posted date': str(result.posted_date),
            'status': result.status,
            'user id': result.user_id
            }
        json_results.append(data)
    return jsonify(items=json_results)


@api_blueprint.route('/api/v1/tasks/<int:task_id>')
def task(task_id):
    result = db.session.query(Task).filter_by(task_id=task_id).first()
    if result:
        result = {
            'task_id': result.task_id,
            'task name': result.name,
            'due date': str(result.due_date),
            'priority': result.priority,
            'posted date': str(result.posted_date),
            'status': result.status,
            'user id': result.user_id
        }
        code = 200
    else:
        result = {"error": "Element does not exist"}
        code = 404
    return make_response(jsonify(result), code)


###################
#### Openstack ####
###################



@api_blueprint.route('/api/v1/volumes/', methods=['GET', 'POST'])
def api_volumes():
    conn  = create_connection()

    if request.method == 'GET':
        volumes = conn.block_storage.volumes()
        json_results = []

        for volume in volumes:
            data = {
                'status' : volume.status,
                'name': volume.status,
                'type': volume.volume_type,
                'size': volume.size,
                'created_at': volume.created_at,
                'is_bootable': volume.is_bootable,
                'attachments': volume.attachments
            }
            json_results.append(data)

        return jsonify({'volumes': json_results})

    elif request.method == 'POST':
        attrs = request.get_json()
        try:
            conn.block_storage.create_volume(attrs)
        except:
            pass

        return jsonify({'code': 200})



@api_blueprint.route('/api/v1/volumes/<volume_id>', methods=['GET', 'DELETE', 'POST'])
def volume(volume_id):
    conn = create_connection()
    code = 200
    try:
        volume = conn.block_storage.get_volume(volume_id)
    except NotFoundException:
        data = {"error": "Element does not exist"}
        code = 404
        return make_response(jsonify(data), code)

    if request.method == 'GET':
        data = {
            'status': volume.status,
            'name': volume.status,
            'type': volume.volume_type,
            'size': volume.size,
            'created_at': volume.created_at,
            'is_bootable': volume.is_bootable,
            'attachments': volume.attachments
        }

    elif request.method == 'DELETE':
        conn.block_storage.delete_volume(volume)
        data = {'status': 'success'}
        code = 204

    #tang dung luong
    elif request.method == 'POST':
        attrs = request.get_json()
        import requests
        url = 'http://10.5.9.58:5000/v3/{project_id}/volumes/{volume_id}/action'.format(project_id='9737fcb6f88d4d85a1348fcdbcccf163',
                                                                   volume_id=volume_id)
        r = requests.post(url=url, json=attrs)
        print(r, 111111111111111111111)

    return make_response(jsonify(data), code)

def increase_volume():
    pass




@api_blueprint.route('/api/v1/snapshots/', methods=['GET'])
def snapshots():
    conn = create_connection()
    snapshots = conn.block_storage.snapshots()
    json_results = []

    for snapshot in snapshots:
        data = {
            'status': snapshot.status,
            'name': snapshot.name,
            'type': 'not found',
            'size': snapshot.size,
            'created_at': snapshot.created_at,
            'metadata' : snapshot.metadata

        }
        json_results.append(data)

    return jsonify({'snapshots': json_results})


@api_blueprint.route('/api/v1/snapshots/<int:snapshot_id>', methods = ['GET', 'DELETE'])
def snapshot(snapshot_id):
    conn = create_connection()
    snapshot = conn.block_storage.get_snapshot(snapshot_id)
    if request.method == 'DELETE':
        conn.block_storage.delete_snapshot(snapshot)
    elif request.method == 'GET':
        data = {
            'status': snapshot.status,
            'name': snapshot.name,
            'type': 'not found',
            'size': snapshot.size,
            'created_at': snapshot.created_at,
            'metadata': snapshot.metadata
        }

        return jsonify({'snapshot': data})

@api_blueprint.route('/api/v1/wan_ips/', methods = ['GET'])
def list_wan_ips():
    conn = create_connection()



















































