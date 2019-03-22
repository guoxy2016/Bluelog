from threading import Thread

from flask import current_app, url_for
from flask_mail import Message

from bluelog.extensions import mail


def send_email(subject, to, html):
    app = current_app._get_current_object()
    message = Message(subject, recipients=[to], html=html)
    t = Thread(target=_send_async_mail, args=(app, message))
    t.start()


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + '#comments'
    html = '<p>博客<i>%s</i>收到一条新评论, 点击查看详细信息</p>' \
           '<p><a href="%s">%s</a></p>' \
           '<p><small style="color: #868e96;">默认发送不必回复</small></p>' % (post.title, post_url, post_url)
    send_email('新的评论', to=current_app.config['BLOG_ADMIN_EMAIL'], html=html)


def send_new_reply_email(comment):
    post_url = url_for('blog.show_post', post_id=comment.post_id, _external=True) + '#comments'
    html = '<p>你评论的博客<i>%s</i>收到了一条新的回复, 点击这里查看详情:</p>' \
           '<p><a href="%s">%s</a></p>' \
           '<p><small style="color: #868e96;">默认发送不必回复</small></p>' % (comment.post.title, post_url, post_url)
    send_email('新的回复', to=comment.email, html=html)
