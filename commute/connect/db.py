from sqlalchemy import create_engine, MetaData


engine = create_engine('mysql+pymysql://root:0623@turingx.kro.kr:3306/test')
meta = MetaData()
conn = engine.connect()
