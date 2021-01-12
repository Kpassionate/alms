#!/user/bin/python
# _*_ coding:utf-8 _*_
# author: yk.guan

from app.my_app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
