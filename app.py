import datetime
from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Person, Base


#конфигурируем движок и сессию для работы с базой
engine = create_engine('sqlite:///people_rest_db.sqlite')
Session = sessionmaker()
Session.configure(bind=engine)

#привязываем модель к таблицам БД
Base.metadata.create_all(engine)

#инициализиурем парсер для обработки данных http запросов
parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('id')
parser.add_argument('salary')
parser.add_argument('birthday')


def person_doesnt_exist():
    return make_response(jsonify({'error':'This person does not exist in the database!'}), 404)


class PeopleOne(Resource):
    def get(self, person_id):
        session = Session()
        person = None
        try:
            person = session.query(Person).filter(Person.id == int(person_id)).first()
        except:
            return make_response(jsonify({'error': 'You submitted incorrect data!'}), 400)
        if not person:
            return person_doesnt_exist()
        else:
            result = {'data':[{'id':person.id,'name':person.name,'salary':str(person.salary),'birthday':person.birthday}]}
            session.close()
            return jsonify(result)


    def delete(self, person_id):
        session = Session()
        person = session.query(Person).filter(Person.id == int(person_id)).first()
        if not person:
            return person_doesnt_exist()
        else:
            result = {'id':person.id,'name':person.name,'salary':str(person.salary),'birthday':person.birthday}
            session.delete(person)
            session.commit()
            session.close()
            return make_response(jsonify(result), 204)


class People(Resource):
    def post(self):
        args = parser.parse_args()
        if args['birthday']:
            args['birthday'] = datetime.datetime.strptime(args['birthday'],'%d-%m-%Y').date()
        try:
            person = Person(id=int(args['id']), name=args['name'], salary=float(args['salary']), birthday=args['birthday'])
        except:
            return make_response(jsonify({'error':'You submitted incorrect data!'}), 400)
        result = {'id':person.id,'name':person.name,'salary':str(person.salary),'birthday':person.birthday}
        session = Session()
        try:
            session.add(person)
            session.commit()
        except IntegrityError:
            return make_response(jsonify({'error': 'Person already exists in the database!'}), 303)
        session.close()
        return make_response(jsonify(result), 201)

    def put(self):
        args = parser.parse_args()
        session = Session()
        person = None
        try:
            person = session.query(Person).filter(Person.id == int(args['id'])).first()
        except:
            return make_response(jsonify({'error': 'You submitted incorrect data!'}), 400)
        if not person:
            return person_doesnt_exist()
        else:
            try:
                if args['birthday']:
                    args['birthday'] = datetime.datetime.strptime(args['birthday'],'%d-%m-%Y').date()
                person.name = args['name'] if args['name'] is not None else person.name
                person.salary = args['salary'] if args['salary'] is not None else person.salary
                person.birthday = args['birthday'] if args['birthday'] is not None else person.birthday
            except:
                make_response(jsonify({'error': 'You submitted incorrect data!'}), 400)

            result = {'id':person.id,'name':person.name,'salary':str(person.salary),'birthday':person.birthday}
            session.add(person)
            session.commit()
            session.close()
            return make_response(jsonify(result), 201)



app = Flask(__name__)
api = Api(app)

api.add_resource(People, '/people')
api.add_resource(PeopleOne, '/people/<person_id>')

