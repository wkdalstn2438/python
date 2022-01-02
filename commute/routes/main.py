from sqlalchemy import select
from models.model import persons, commutes, payments
from connect.db import conn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import uvicorn
import time


app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get('/')
def fetch_all():
    return conn.execute(persons.select()).fetchall()


@app.get('/person/create')
def create_person(request: Request):
    return templates.TemplateResponse("person/create.html", {"request": request})


@app.post('/person/create')
def create_person(request: Request,  ssn: str = Form(...), name: str = Form(...), age: int = Form(...),
                  tel: str = Form(...)):
    conn.execute(persons.insert().values(ssn=ssn, name=name, age=age, tel=tel))
    return templates.TemplateResponse('person/create.html', {"request": request})


@app.get('/person/show')
def show_person(request: Request):
    result = conn.execute(persons.select()).fetchall()
    return templates.TemplateResponse('person/show.html', {'request': request, 'result': result})


@app.get('/person/update')
def update_person(request: Request):
    return templates.TemplateResponse("person/update.html", {"request": request})


@app.post('/person/update')
def update_person(request: Request,  ssn: str = Form(...), name: str = Form(...), age: int = Form(...),
                  tel: str = Form(...)):
    conn.execute(persons.update().values(name=name, age=age,
                                         tel=tel).where(persons.c.ssn == ssn))
    return templates.TemplateResponse('person/update.html', {"request": request})


@app.get('/person/delete')
def delete_person(request: Request):
    return templates.TemplateResponse('person/delete.html', {"request": request})


@app.post('/person/delete')
def delete_person(request: Request, ssn: str = Form(...)):
    conn.execute(persons.delete().where(persons.c.ssn == ssn))
    return templates.TemplateResponse('person/delete.html', {"request": request})


@app.get('/person/format')
def truncate_person():
    return conn.execute(persons.delete())


@app.get('/commute/in')
def go_to_work(request: Request):
    return templates.TemplateResponse("commute/in.html", {"request": request})


@app.post('/commute/in')
def go_to_work(request: Request,  ssn: str = Form(...)):
    st = time.strftime('%Y-%m-%d %H:%M:%S')
    cid = st[:4] + st[5:7] + st[8:10] + ssn
    conn.execute(commutes.insert().values(id=cid, ssn=ssn, st=st, et=None))
    return templates.TemplateResponse('commute/in.html', {"request": request})


@app.get('/commute/out')
def off_work(request: Request):
    return templates.TemplateResponse("commute/out.html", {"request": request})


@app.post('/commute/out')
def off_work(request: Request,  ssn: str = Form(...)):
    et = time.strftime('%Y-%m-%d %H:%M:%S')
    cid = et[:4] + et[5:7] + et[8:10] + ssn
    conn.execute(commutes.update().values(et=et).where(commutes.c.id == cid))
    return templates.TemplateResponse('commute/out.html', {"request": request})


@app.get('/commute/show')
def show_commute(request: Request):
    result = conn.execute(select([persons.c.ssn, persons.c.name, commutes.c.st, commutes.c.et]).
                          select_from(persons.join(commutes))).fetchall()
    return templates.TemplateResponse('commute/show.html', {'request': request, 'result': result})


@app.get('/payment/pay')
def pay_salary(request: Request):
    return templates.TemplateResponse("payment/pay.html", {"request": request})


@app.post('/payment/pay')
def pay_salary(request: Request,  ssn: str = Form(...), money: int = Form(...)):
    pay_date = time.strftime('%Y-%m-%d %H:%M:%S')
    conn.execute(payments.insert().values(ssn=ssn, money=money, date=pay_date))
    return templates.TemplateResponse('payment/pay.html', {"request": request})


@app.get('/payment/show')
def show_pay(request: Request):
    result = conn.execute(select([persons.c.ssn, persons.c.name, payments.c.money, payments.c.date]).
                          select_from(persons.join(payments))).fetchall()
    return templates.TemplateResponse('payment/show.html', {'request': request, 'result': result})


@app.get('/payment/search')
def show_one_pay(request: Request):
    return templates.TemplateResponse('payment/search.html', {'request': request})


@app.post('/payment/search')
def show_one_pay(request: Request, ssn: str = Form(...)):
    result = conn.execute(select([persons.c.ssn, persons.c.name, payments.c.money, payments.c.date]).
                          select_from(persons.join(payments)).where(payments.c.ssn == ssn)).fetchall()
    return templates.TemplateResponse('payment/show.html', {'request': request, 'result': result})


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True, workers=4)

# unicorn routes.main:app --reload
