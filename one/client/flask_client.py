######################################################
#        > File Name: flask_client.py
#      > Author: GuoXiaoNao
 #     > Mail: 250919354@qq.com 
 #     > Created Time: Mon 20 May 2019 11:52:00 AM CST
 ######################################################

from flask import Flask, send_file
import sys


app = Flask(__name__)

@app.route('/index')
def index():
    #首页
    return send_file('templates/index.html')

@app.route('/login')
def login():
    #登录
    return send_file('templates/login.html')

@app.route('/login_callback')
def login_callback():
    #授权登录
    return send_file('templates/oauth_callback.html')

@app.route('/register')
def register():
    #注册

    return send_file('templates/register.html')

@app.route('/<username>/info')
def info(username):
    #个人信息
    return send_file('templates/about.html')

@app.route('/<username>/change_info')
def change_info(username):
    #修改个人信息
    return send_file('templates/change_info.html')

# @app.route('/<username>/change_password')
# def change_password(username):
#     #修改密码
#     return send_file('templates/change_password.html')


@app.route('/<username>/topic/release')
def topic_release(username):
    #发表博客
    return send_file('templates/release.html')


@app.route('/<username>/topics')
def topics(username):
    #个人博客列表
    return send_file('templates/list.html')

@app.route('/<username>/topics/detail/<t_id>')
def topics_detail(username, t_id):
    #博客内容详情
    return send_file('templates/detail.html')


@app.route('/test_api')
def test_api():
    #测试
    return send_file('templates/test_api.html')

@app.route('/abcd')
def abcd():
    #个人信息
    return send_file('templates/abcd.html')



@app.route('/info_img')
def info_img():
# 修改个人头像
    return send_file('templates/infoImg.html')

@app.route('/change_password')
def change_password():
    #修改密码
    return send_file('templates/changePassword.html')

@app.route('/email')
def email ():
# 邮箱绑定
    return send_file('templates/email.html')

@app.route('/phone')
def phone():
# 手机号更换
    return send_file('templates/phone.html')


@app.route('/amend_name')
def amend_name():
# 修改用户名
    return send_file('templates/amendName.html')


@app.route('/video_consume')
def video_consume ():
# 视频消费记录
    return send_file('templates/videoConsume.html')

@app.route('/video_matter')
def video_matter():
# 问答消费记录
    return send_file('templates/videoMatter.html')

@app.route('/video_app_consume')
def video_app_consume():
# APP离线消费
    return send_file('templates/videoAppConsume.html')

@app.route('/VBi')
def VBi():
# v币充值
    return send_file('templates/VBi.html')



@app.route('/flack_intro')
def flack_intro():
# 修活动介绍
    return send_file('templates/flackIntro.html')

@app.route('/flack_means')
def flack_means():
# 宣传方法
    return send_file('templates/flackMeans.html')

@app.route('/flack_origin')
def flack_origin():
# 宣传来路
    return send_file('templates/flackOrigin.html')

@app.route('/no_note')
def no_note():
# 没有笔记
    return send_file('templates/classroomNoNote.html')

@app.route('/learn_info')
def learn_info():
    # 个人学习信息
    return send_file('templates/attention.html')

@app.route('/attention')
def attention():
    # 个人学习信息 我的学习进度
    return send_file('templates/attention2.html')

@app.route('/look_note')
def look_note():
# 课堂查看笔记
    return send_file('templates/classroomLookNote.html')

@app.route('/note')
def note ():
# 课堂笔记
    return send_file('templates/classroomNote.html')

@app.route('/progress')
def progress():
# 我的关注的课程
    return send_file('templates/progress.html')

@app.route('/comment')
def comment():
# 我的评论
    return send_file('templates/comment.html')
if __name__ == '__main__':
    app.run(debug=True)

