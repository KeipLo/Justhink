import sqlite3


def db_islem(islem ,is_degeri = None ,islem_bilgi_1 = None ,islem_bilgi_2 = None ,islem_bilgi_3 = None) :
	if islem == 'sil' :
		deger_sil()

	if islem == 'ekle' :
		deger_ekle(islem_bilgi_1,islem_bilgi_2,islem_bilgi_3)

	if islem == 'cek' :
		deger_cek()

	if islem == 'degistir' :
		deger_degistir(is_degeri,islem_bilgi_1)


	con.commit()


def tablo_olustur() :
	con.execute("CREATE TABLE IF NOT EXISTS justhink_data(kullanici_adi TEXT,tamamlanan INT,muzik BOOL)")

def deger_ekle(bilgi_1,bilgi_2,bilgi_3) :
	if bilgi_3 == 'True':
		bilgi_3 = True
	elif bilgi_3 == 'False':
		bilgi_3 = False
	con.execute("INSERT INTO justhink_data(kullanici_adi,tamamlanan,muzik) VALUES(:b1,:b2,:b3)",{'b1':bilgi_1,'b2':bilgi_2,'b3':bilgi_3})

def deger_cek() :
	cursor.execute("SELECT * from justhink_data")

	for i in cursor.fetchall() :
		print(i)

def deger_degistir(is_,b1) :
	if is_ == 'kullanici_adi' :
		cursor.execute("UPDATE justhink_data SET kullanici_adi=:b1",{'b1':b1})
	elif is_ == 'tamamlanan' :
		cursor.execute("UPDATE justhink_data SET tamamlanan=:b1",{'b1':b1})
	elif is_ == 'muzik' :
		if b1 == 'True':
			b1 = True
		elif b1 == 'False':
			b1 = False
		cursor.execute("UPDATE justhink_data SET muzik=:b1",{'b1':b1})

def deger_sil() :
	cursor.execute("DELETE FROM justhink_data")

with sqlite3.connect("justhink.db") as con :
	cursor = con.cursor()
	run = True
	tablo_olustur()
	while run :
		islem = input("islem girin (iptal/sil/ekle/cek/degistir): ")

		if islem == 'iptal':
			run = False
		elif islem == 'ekle':
			b1 = input("kullanici adi : ")
			b2 = int(input("tamamlanan leveller : "))
			b3 = input("muzik tercihi (True/False) : ")
			db_islem(islem,None,b1,b2,b3)
		elif islem == 'degistir':
			is_degeri = input("degistirmek istenilen ( kullanici_adi / tamamlanan(sonraki soruda sayı girin) / muzik(sonraki soruda 0/1 girin)) :") 
			b1 = input("olması istenen :")
			if is_degeri == "tamamlanan" :
				b1 = int(b1)
			db_islem(islem,is_degeri,b1)
		else:
			db_islem(islem)
	














	
