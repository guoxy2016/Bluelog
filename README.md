# guoblog
博客网站, bootstrap-flask, flask-login, 分享评论, 数据库关联删除.\
需要设置.env文件保存内容:
```.env
MAIL_SERVER=
MAIL_USERNAME=
MAIL_PASSWORD=
GUOBLOG_EMAIL=网站站长邮箱与MAIL_SERVER邮箱不同
SECRET_KEY=
DATABASE_URI=
```

运行方法:
~~~
cd /path/to/guoblog
pip3 install pipenv
pipenv install --dev
pipenv shell
flask init 
flask run
~~~