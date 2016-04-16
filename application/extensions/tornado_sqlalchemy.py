# coding=utf-8
from tornado.web import HTTPError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


class DeclarativeBase(object):
    """
    在 application 初始化之后,给该类进行赋值操作
    以便在Model实例中获得 Context 或访问其他全局对象
    eg. DeclarativeBase.db = mysql_session
    """

    query = None
    db = None

    def save(self):
        try:
            self.db.add(self)
            self.db.commit()
        except:
            self.db.rollback()

    def remove(self):
        try:
            self.db.delete(self)
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False


class TornadoORMQueryMixin(DeclarativeBase):
    """
    依赖 tornado 查询扩展
    """
    @classmethod
    def first_or_404(cls, **kwargs):
        obj = cls.query.filter_by(**kwargs).first()
        if not obj:
            raise HTTPError(404)
        return obj

    @classmethod
    def get_or_404(cls, **kwargs):
        result = cls.query.filter_by(**kwargs).all()
        if not result:
            raise HTTPError(404)
        return result


class TornadoSQLAlchemy:
    def __init__(self, app=None):
        self.app = app
        self.base_model = declarative_base(cls=TornadoORMQueryMixin)

    def init_app(self, app):
        if not self.app:
            self.app = app
        config_url = 'mysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DBNAME}'.format(**app.settings)
        engine = create_engine(config_url)
        self.Model.metadata.create_all(engine)
        session = scoped_session(sessionmaker(bind=engine))
        self.Model.db = session
        self.Model.query = session.query_property()
        app.mysql_db = session
        return session

    @property
    def Model(self):
        """
        定义模型时需继承 db.Model
        用法:
            class Model(db.Model):
                column_name = Column()
        """
        return self.base_model

db = TornadoSQLAlchemy()
