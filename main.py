
import re
from flask import Flask,render_template,request,session,redirect,url_for
import mysql.connector
from flask.templating import render_template_string


app = Flask(__name__)
app.config['SECRET_KEY'] = "RAF2021-2022"
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="",
	database="ispit2022" # iz phpmyadmin 
    )

from biciklista import Biciklista


def konverzija(element):
	n = len(element)
	element = list(element)
	for i in range(n):
		if isinstance(element[i], bytearray):
			element[i] = element[i].decode()
	return element
	
@app.route('/register', methods=['POST','GET'])
def register():
	if request.method == 'GET':
		return render_template(
			'register.html'
		)
	broj_prijave = request.form['broj_prijave']
	pol = request.form['pol']
	sifra = request.form['password']
	potvrda = request.form['confirm']
	prva_etapa = request.form['prva_etapa']
	druga_etapa= request.form['druga_etapa']

	cursor = mydb.cursor(prepared=True)
	sql = "SELECT * FROM biciklisti WHERE broj_prijave = ?"
	vrednost = (broj_prijave,)
	cursor.execute(sql,vrednost)
	rez = cursor.fetchone()
	
	if rez != None:
		return render_template(
			'register.html',
			broj_prijave_greska = 'Vec postoji korisnik sa tom prijavom'
		)

	if sifra != potvrda:
		return render_template(
			'register.html',
			confirm_greska = 'Ne poklapaju se sifre'
		)
	
	if int(prva_etapa) <= 0:
		return render_template(
			'register.html',
			prva_etapa_greska = "Mora biti pozitivan broj"
		)
	if int(druga_etapa) <= 0:
		return render_template(
			'register.html',
			druga_etapa_greska = "Mora biti pozitivan broj"
		)

	cursor = mydb.cursor(prepared=True)
	sql = 'INSERT INTO biciklisti VALUES(null,?,?,?,?,?)'
	vrednosti = (broj_prijave,sifra,pol,prva_etapa,druga_etapa)
	cursor.execute(sql,vrednosti)
	mydb.commit()

	return redirect(url_for('show_all'))

@app.route('/show_all')
def show_all():
	cursor = mydb.cursor(prepared=True)
	sql = "SELECT * FROM biciklisti"
	cursor.execute(sql)
	rez = cursor.fetchall()

	n = len(rez)
	for i in range(n):
		rez[i] = konverzija(rez[i])

	lista_objekata_biciklisti = []
	for element in rez:
		id = element[0]
		broj_prijave = element[1]
		sifra = element[2]
		pol = element[3]
		etapa_jedan = element[4]
		etapa_dva = element[5]
		trenutni_takmicar = Biciklista(id,broj_prijave,sifra,pol,etapa_jedan,etapa_dva)
		lista_objekata_biciklisti.append(trenutni_takmicar)
	if request.method == "GET":
		return render_template(
			'show_all.html',
			biciklisti = lista_objekata_biciklisti
		)

@app.route('/login', methods=['POST','GET'])
def login():
	if 'broj_prijave' in session:
		return redirect(url_for('show_all'))
	if request.method == 'GET':
		return render_template(
			'login.html'
		)
	
	broj_prijave = request.form['broj_prijave']
	sifra = request.form['password']

	cursor = mydb.cursor(prepared=True)
	sql = 'SELECT * FROM biciklisti WHERE broj_prijave = ?'
	vrednost = (broj_prijave,)
	cursor.execute(sql,vrednost)
	rez = cursor.fetchone()


	if rez == None:
		return render_template(
			'login.html',
			broj_prijave_greska = 'Ne postoji biciklista sa tom prijavom'
		)
	rez = konverzija(rez)

	if rez[2] != sifra:
		return render_template(
			'login.html',
			pass_greska = 'Ne poklapaju se sifre'
		)
	session['broj_prijave'] = broj_prijave
	return redirect(url_for('show_all'))

@app.route('/logout')
def logout():
	if 'broj_prijave' in session:
		session.pop('broj_prijave')
		return redirect(url_for('login'))
	else:
		return redirect(url_for('show_all'))
	
@app.route('/profili/<broj_prijave>')
def profili(broj_prijave):
	cursor = mydb.cursor(prepared=True)
	sql = 'SELECT * FROM biciklisti WHERE broj_prijave = ?'
	vrednost = (broj_prijave,)
	cursor.execute(sql,vrednost)
	rez = cursor.fetchone()

	rez = konverzija(rez)
	
	id = rez[0]
	broj_prijave = rez[1]
	sifra = rez[2]
	pol = rez[3]
	etapa_jedan = rez[4]
	etapa_dva = rez[5]
	biciklista = Biciklista(id,broj_prijave,sifra,pol,etapa_jedan,etapa_dva)

	if request.method == 'GET':
		return render_template(
			'profili.html',
			biciklista = biciklista
		)

@app.route('/delete/<broj_prijave>')
def delete(broj_prijave):
	cursor = mydb.cursor(prepared=True)
	sql = 'DELETE FROM biciklisti WHERE broj_prijave = ?'
	vrednost = (broj_prijave,)
	cursor.execute(sql,vrednost)
	mydb.commit()

	return redirect(url_for('show_all'))

@app.route('/rang_lista_po_etapi/<broj_etape>')
def rang_lista_po_etapi(broj_etape):
	cursor = mydb.cursor(prepared=True)
	if int(broj_etape) != 1 and int(broj_etape) != 2:
		return redirect(url_for('show_all'))
	elif broj_etape == 1:
		sql = 'SELECT * FROM biciklisti ORDER BY etapa_jedan'
	else:
		sql = 'SELECT * FROM biciklisti ORDER BY etapa_dva'
	cursor.execute(sql)
	rez = cursor.fetchall()

	n = len(rez)
	for i in range(n):
		rez[i] = konverzija(rez[i])
	
	lista_biciklista = []
	for i in rez:
		id = i[0]
		broj_prijave = i[1]
		sifra = i[2]
		pol = i[3]
		etapa_jedan = i[4]
		etapa_dva = i[5]
		trenutni_biciklista = Biciklista(id,broj_prijave,sifra,pol,etapa_jedan,etapa_dva)
		lista_biciklista.append(trenutni_biciklista)

	return render_template(
		'show_all.html',
		biciklisti = lista_biciklista
	)

@app.route('/update/<broj_prijave>', methods=['POST','GET'])	
def update(broj_prijave):
	cursor = mydb.cursor(prepared=True)
	sql = 'SELECT * FROM biciklisti WHERE broj_prijave = ?'
	vrednost = (broj_prijave,)
	cursor.execute(sql,vrednost)
	rez = cursor.fetchone()
	rez = konverzija(rez)	

	
	id = rez[0]
	broj_prijave = rez[1]
	sifra = rez[2]
	pol = rez[3]
	etapa_jedan = rez[4]
	etapa_dva = rez[5]
	biciklista = Biciklista(id,broj_prijave,sifra,pol,etapa_jedan,etapa_dva)
	

	if request.method == 'GET':
		return render_template(
			'update.html',
			biciklista = biciklista
		)

	sifra = request.form['password']
	pol = request.form['pol']
	etapa_jedan = request.form['prva_etapa']
	etapa_dva = request.form['druga_etapa']
	broj_prijave = request.form['broj_prijave']

	cursor = mydb.cursor(prepared=True)
	sql = 'UPDATE biciklisti SET sifra = ?, pol = ?, etapa_jedan = ?, etapa_dva = ?  WHERE broj_prijave = ?'
	vrednosti = (sifra,pol,etapa_jedan,etapa_dva,broj_prijave)
	cursor.execute(sql,vrednosti)
	mydb.commit()

	return redirect(url_for('show_all'))
	
app.run(debug=True)
