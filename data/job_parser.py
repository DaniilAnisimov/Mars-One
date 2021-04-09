from flask_restful import reqparse
from datetime import datetime

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('job', required=True, type=str)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True, type=str)
parser.add_argument('start_date', type=datetime)
parser.add_argument('end_date', type=datetime)
parser.add_argument('is_finished', required=True, type=bool)
