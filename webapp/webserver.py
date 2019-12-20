# -*- coding: utf-8 -*-

import re
import sys
import json
import logging

from flask import Flask
from flask import request
from flask import render_template
from playhouse.shortcuts import model_to_dict

sys.path.append('../')

from src.conf import setting
from src.orm.message_model import MessageModel
from src.orm.group_model import GroupModel
from src.orm.user_model import UserModel
from src.util import util
from src.util.util import timestamp2datestring as t2d
from src.util.request import RemoteRequest
from src.log import init_log


app = Flask(__name__)


init_log('log/app')


@app.route('/', methods=['GET'])
def messages():
    messages = (MessageModel
                .select()
                .where(MessageModel.group_id == '454c1ad2'))

    for message in messages:
        message.type = setting.MSG_TYPES[message.type]
        message.question = 'Yes' if message.question else 'No'
        message.create_time = t2d(message.create_time)

    return render_template('messages.html', messages=messages)


@app.route('/questions', methods=['GET'])
def questions():
    messages = (MessageModel
                .select()
                .where(MessageModel.type == 0)
                .where(MessageModel.question == 1)
                .where(MessageModel.group_id == '454c1ad2'))

    for message in messages:
        message.type = setting.MSG_TYPES[message.type]
        message.question = 'Yes' if message.question else 'No'
        message.create_time = t2d(message.create_time)

    return render_template('questions.html', messages=messages)


@app.route('/message/<int:mid>', methods=['GET'])
def message(mid):
    try:
        message = (MessageModel
                   .select()
                   .where(MessageModel.message_id == mid)
                   .get())

    except Exception:
        return render_template('message.html')

    answers = (MessageModel
               .select()
               .where(MessageModel.question == 0)
               .where(MessageModel.answer == mid))

    answers2 = (MessageModel
                .select()
                .where(MessageModel.question == 0)
                .where(MessageModel.type == message.type)
                .where(MessageModel.create_time >= message.create_time)
                .where(MessageModel.group_name == message.group_name)
                .where(MessageModel.create_time <= message.create_time+3600))

    answers3 = []
    try:
        response = (RemoteRequest()
                    .get(setting.search_url.format(message.content)))
        response = json.loads(response)
        for answer in response['data']['search_list']:
            answer['create_time'] = t2d(answer['create_time'])
            answer['type'] = setting.search_type_name[answer['type']]
            answer['url'] = setting.article_url.format(answer['index_id'])
            answers3.append(answer)
    except Exception:
        logging.error('search community error of query {}'
                      .format(message.content))

    message.create_time = t2d(message.create_time)
    for answer in answers:
        answer.create_time = t2d(answer.create_time)
    for answer in answers2:
        answer.create_time = t2d(answer.create_time)

    return render_template('message.html',
                           message=message,
                           answers=answers,
                           answers2=answers2,
                           answers3=answers3)


@app.route('/user/<uid>', methods=['GET'])
def user(uid):
    try:
        user = (UserModel
                .select()
                .where(UserModel.user_id == uid)
                .get())
    except Exception:
        return render_template('user.html')

    user.avatar_url = 'stores{}'.format(
        user.avatar_url.split('downloads')[1])

    questions = (MessageModel
                 .select()
                 .where(MessageModel.user_id == user.user_id)
                 .where(MessageModel.type == 0)
                 .where(MessageModel.question == 1))
    answers = (MessageModel
               .select()
               .where(MessageModel.user_id == user.user_id)
               .where(MessageModel.type == 0)
               .where(MessageModel.question == 0))

    return render_template('user.html',
                           user=user,
                           questions=questions,
                           answers=answers)


@app.route('/answers', methods=['GET'])
def answers():
    answers = (MessageModel
               .select()
               .where(MessageModel.question == 0)
               .where(MessageModel.group_id == '454c1ad2'))

    for answer in answers:
        answer.create_time = t2d(answer.create_time)

    return render_template('answers.html', answers=answers)


def pure(content):
    user_name = None
    if content.find('@') or content.find('\u2005'):
        logging.info('at user_name[{}] content[{}]'
                     .format(user_name, content))
        result = re.search(r'@([\s\S]+?)\u2005', content)
        if result:
            user_name = result.group(1)
            content = content.replace(user_name, '')
        content = content.replace('@', '').replace('\u2005', '')
        logging.info('at user_name[{}] content[{}]'.
                     format(user_name, content))
    return user_name, content


def get_user_id(user_name):
    user_id = None
    if not user_name:
        return user_id
    try:
        user = (GroupModel
                .select()
                .where(GroupModel.user_display == user_name)
                .get())
        user_id = user.user_id
        if not isinstance(user_id, str):
            raise
    except Exception:
        # 解决特例
        if user_name.find('嘿嘿哟'):
            user_id = '1d996a78'
        if user_name.find('风轻云淡'):
            user_id = 'c5f3d975'
        logging.error('select user info {} fail. user_id[{}]'.
                      format(user_name, user_id))

    return user_id


@app.route('/doquestion', methods=['POST'])
def doquestion():
    messages = (MessageModel
                .select()
                .where(MessageModel.type == 0)
                .where(MessageModel.group_id == '454c1ad2'))

    new_messages = []
    question_id = None
    for message in messages:
        user_id = None
        user_name, content = pure(message.content)
        if user_name:
            user_id = get_user_id(user_name)
            if not user_id:
                continue
        message.question = util.question(content)
        if message.question:
            question_id = message.message_id
        if not message.answer:
            message.answer = question_id
        message.content = content
        if user_id and isinstance(user_id, str):
            message.receiver = user_id
        new_messages.append(model_to_dict(message))

    message.replace_many(new_messages).execute()

    result = {
        'code': 0,
        'msg': '',
        'data': new_messages
    }

    return json.dumps(result)


@app.route('/users', methods=['GET'])
def users():
    user_ids = []
    members = GroupModel.select().where(GroupModel.group_id == '454c1ad2')
    for member in members:
        user_ids.append(member.user_id)

    users = UserModel.select().where(UserModel.user_id << user_ids)
    for user in users:
        user.avatar_url = 'stores{}'.format(
            user.avatar_url.split('downloads')[1])

    return render_template('users.html', users=users)


@app.route('/groups', methods=['GET'])
def groups():
    members = (GroupModel.select(GroupModel, UserModel.nick_name)
               .join(UserModel, on=(GroupModel.user_id == UserModel.user_id))
               .where(GroupModel.group_id == '454c1ad2')
               .namedtuples())

    return render_template('groups.html', members=members)


@app.route('/group/<groupid>', methods=['GET'])
def group(groupid):
    members = GroupModel.select().where(GroupModel.group_id == groupid)

    return render_template('groups.html', members=members)


@app.route('/search', methods=['GET'])
def search():
    word = request.args.get('search', '')
    messages = (MessageModel
                .select(MessageModel, UserModel.nick_name)
                .join(UserModel,
                      on=(MessageModel.receiver == UserModel.user_id))
                .where(MessageModel.content % '%{}%'.format(word))
                .namedtuples())

    for message in messages:
        message.type = setting.MSG_TYPES[message.type]
        message.question = 'Yes' if message.question else 'No'
        message.create_time = t2d(message.create_time)

    return render_template('questions.html', messages=messages)


@app.route('/statistics', methods=['GET'])
def statistics():
    users = (MessageModel
             .select(MessageModel.user_id)
             .where(MessageModel.group_id == '454c1ad2')
             .group_by(MessageModel.user_id))

    active = 0
    for user in users:
        active = active + 1

    return render_template('statistics.html', active=active)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
