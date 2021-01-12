# alms
audio  library  management  system  听书管理系统  use flask

摸索中成长

- flask项目启动阶段相关配置及说明
- 第一步：flask相关配置信息 configs.py文件
    - 
- 第二步：app/models/base.py  实例化SQLAlchemy,并编写Base基类模型
    -
- 第三步：创建模型，如models/book 
    -
- 第四步：配置app/my_app.py  中的create_app函数
    -  
    - 1、实例化Flask: app = Flask(__name__) 
    - 2、加载配置: app.config.from_object(DevConfig) 
    - 3、初始化数据库: 采用 db.init_app(app)方式，除此之外还有一种方式（db=SQLAlchemy(app)）
    - 4、实例化manager对象： manager = Manager(app)
    - 5、执行迁移： migrate = Migrate(app, db)
    - 6、生成migrations迁移文件夹： manager.add_command('db', MigrateCommand)
    - 7、注册蓝图

- 第五步：manage.py 启动项目
    -

#注：
- 使用flask-migrate的好处：
    - 1、未使用之前需要用传统的方式生成数据库表结构，且修改模型后无法知晓变更前模型，无法回退等
    - 2、未使用时需要将整个model文件导入到my_app.py文件中才能使用db.create_all(app=app)完成首次创建所有模型
    - 3、反之方便，有记录，不用使用db.create_all(app=app)等命令

- flask-migrate的使用方法：
    - 在Windows中先实例化项目控制台运行：set FLASK_APP = manage.py

    - 此时 运行 flask run 为 启动项目
    - 初始化数据库，并生成migrations文件(仅需执行一次) ：flask db init 
    - 生成迁移文件（包括数据库更新） ： flask db migrate
    - 执行迁移（创建数据库表结构）： flask db upgrade
    - 查看帮助：  flask db --help
    
    
JWT的使用方法：
    - pip install flask-jwt-extended
    - 在configs文件中配置JWT秘钥、过期时间等（更多配置查看源码）
    - 在my_app 文件中挂载jwt ,在加载配置后jwt = JWTManager(app)
    - 登录接口中，登录成功后返回token值
          if user.check_password(password):
              access_token = create_access_token(identity=email)
              # 返回用户email 和 token值
              return jsonify(email=email, token=access_token)
              
    -- 使用验证时：
    
        @mod.route('/all', methods=['GET'])
        @jwt_required
        def get_all_books():
            # current_user为使用token创建的email
            current_user = get_jwt_identity()
            books = Book.query.all()
            return jsonify(books)
            
            
    - @jwt_required 验证用户token信息既验证用户登录状态
    - create_access_token(identity=email) 创建token
    - @jwt_required 验证token
    - get_jwt_identity()获取token值中的identity 等等
    
    
handle.py 文件中创建服务器返回值