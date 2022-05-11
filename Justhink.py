from pygame.locals import *
import pygame #pygame(pyhton ile oyun yapma motoru) kütüphanesi çağırıldı
from time import sleep
import sqlite3
from random import sample, randint, choice
import os
import webbrowser

pygame.init() #pygame başlatıldı
pygame.display.set_caption("Justhink") # pencere (oyunun) adı


##############      GÖRSELLER KISMI     ###############
#	ekran arkaplanları
ozelT_image = pygame.image.load("SpecialThanks-1.png.png")
ayarlar_image = pygame.image.load("Settings-1.png.png")
referanslar_image = pygame.image.load("References-1.png.png")
menuEkrani_image = pygame.image.load("Menuekranı.png")
dialogkutusu_image = pygame.image.load("DialogBox.png")
kullanici_image = pygame.image.load("UnknownPerson-1.png.png")
laptop_image = pygame.image.load("Laptop-1.png.png")
laptop_image = pygame.transform.scale(laptop_image,(800,600))
masaustu_image = pygame.image.load("ekran+MasaUstu.jpeg")
masaustu_image = pygame.transform.scale(masaustu_image,(800,600))
levelsec_image = pygame.image.load("Level_selection.png")
levelwall_image = pygame.image.load("levelwall.png")
level6_gizle_image = pygame.image.load("level6_gizle.png")
hacked_image = pygame.image.load("HackedWindow.png")
final_bg_image = pygame.image.load("Level_bg.png")
final_way_image = pygame.image.load("Level_way.png")

oyuncu_surf = pygame.image.load("Labirent(sen)-1.png.png")
block_surf = pygame.image.load("Labirent(bitis)-3.png.png")
bitis_surf = pygame.image.load("Labirent(bitis)-2.png.png")

yuz1_image = pygame.image.load('Face-1.png.png')
yuz2_image = pygame.image.load('Face-2.png.png')
yuz3_image = pygame.image.load('Face-3.png.png')
yuz4_image = pygame.image.load('Face-4.png.png')

dosya1_image = pygame.image.load('1_dosyasi.png')
dosya1_image = pygame.transform.scale(dosya1_image,(50,70))
dosya0_image = pygame.image.load('0_dosyasi.png')
dosya0_image = pygame.transform.scale(dosya0_image,(50,70))

#	Butonların görselleri
geri_butonu_yuzey = pygame.image.load("back_button.png")
geri_butonu_basilmis_yuzey = pygame.image.load("back_button_green.png")

oyna_butonu_yuzey = pygame.image.load("Oyna_ikonu.png")
oyna_butonu_basilmis_yuzey = pygame.image.load("Oyna_ikonu_basılı.png")

ozelt_butonu_yuzey = pygame.image.load("Ozelt_ikonu.png")
ozelt_butonu_basilmis_yuzey = pygame.image.load("Ozelt_ikonu_basılı-1.png.png")

ayarlar_butonu_yuzey = pygame.image.load("Ayarlar_ikonu.png")
ayarlar_butonu_basilmis_yuzey = pygame.image.load("Ayarlar_ikonu_basılı.png")

referanslar_butonu_yuzey = pygame.image.load("Referanslar_ikonu.png")
referanslar_butonu_basilmis_yuzey = pygame.image.load("Referanslar_ikonu_basılı.png")

dialog_butonu_yuzey = pygame.image.load("Dialogbutton.png")
dialog_butonu_basilmis_yuzey = pygame.image.load("Dialogbutton_basılı.png")

masaustu_butonu_yuzey = pygame.image.load("masaustu_butonu.png")
masaustu_butonu_basilmis_yuzey = pygame.image.load("masaustu_butonu_basili.png")

sesacik_butonu_yuzey = pygame.image.load("sound_on.png")
sesacik_butonu_basilmis_yuzey = pygame.image.load("sound_on_basilmis.png")

seskapali_butonu_yuzey = pygame.image.load("sound_off.png")
seskapali_butonu_basilmis_yuzey = pygame.image.load("sound_off_basilmis.png")

sifirla_butonu_yuzey = pygame.image.load("sifirla_butonu.png")
sifirla_butonu_basilmis_yuzey = pygame.image.load("sifirla_butonu_basilmis.png")

seckare_butonu_yuzey = pygame.image.load("seckare-1.png.png")
seckare_butonu_basilmis_yuzey = pygame.image.load("seckare_basilmis-2.png.png")

secfinal_butonu_yuzey = pygame.image.load("secfinal-2.png.png")
secfinal_butonu_basilmis_yuzey = pygame.image.load("secfinal_basilmis-1.png.png")

secunlem_butonu_yuzey = pygame.image.load("secunlem.png")
secunlem_butonu_basilmis_yuzey = pygame.image.load("secunlem_basilmis.png")

ok_butonu_yuzey = pygame.image.load("ok_basilmamis.png")
ok_butonu_basilmis_yuzey = pygame.image.load("ok_basilmis.png")

class DataBase():
	def __init__(self):
		#kullanıcı adı = (ka)
		self.eski_ka = ''
		#tamamlanan level = (tl)
		self.eski_tl = 0
		#muzik = (mz)
		self.eski_mz = 1

		self.dongu_sayi = 0

	def downdate(self):
		with sqlite3.connect("justhink.db") as con :
			cursor = con.cursor()
			try :
				con.execute("CREATE TABLE justhink_data(kullanici_adi TEXT,tamamlanan INT,muzik BOOL)")
				con.execute("INSERT INTO justhink_data(kullanici_adi,tamamlanan,muzik) VALUES(:b1,:b2,:b3)",{'b1':'','b2':0,'b3':1})
			except sqlite3.OperationalError:
				cursor.execute("SELECT * from justhink_data")
				for i in cursor.fetchall() :
					self.eski_ka = i[0]
					self.eski_tl = i[1]
					self.eski_mz = i[2]
				if self.eski_ka != '' :
					g.kullanici_adi = self.eski_ka
				if self.eski_tl != 0 :
					l.tamamlanan = self.eski_tl
					l.mevcut_level = l.tamamlanan +1
					l.tamamlanan = self.eski_tl
					l.mevcut_level = "level_sec"
				if self.eski_mz!= 1 :
					g.muzik = self.eski_mz
			con.commit()

	def update(self,kontrol):
		with sqlite3.connect("justhink.db") as con :
			cursor = con.cursor()
			if kontrol == 'ka'and g.kullanici_adi != self.eski_ka :
				cursor.execute("UPDATE justhink_data SET kullanici_adi=:b1",{'b1':g.kullanici_adi})
				self.eski_ka = g.kullanici_adi
			elif kontrol == 'tl'and l.tamamlanan > self.eski_tl :
				cursor.execute("UPDATE justhink_data SET tamamlanan=:b1",{'b1':l.tamamlanan})
				self.eski_tl = l.tamamlanan
			elif kontrol == 'mz'and g.muzik != self.eski_mz :
				cursor.execute("UPDATE justhink_data SET muzik=:b1",{'b1':g.muzik})
				self.eski_mz = g.muzik
			con.commit()

	def resetle(self):
		g.SCREEN = None
		g.pencere.fill(g.siyah)
		text_blit("İLERLEME SIFIRLANDI","ortala",285,30,"beyaz")
		if self.dongu_sayi <= 250 :
			self.dongu_sayi += 1
		else :
			ekran_gecisi_1.yap("beyaz")
			if ekran_gecisi_1.dongu == False :
				self.dongu_sayi = 0
				self.bolumekrani_dongu = 0
				sifirla_butonu.dongu = False
				self.dialog = True
				ekran_gecisi_2.__init__()
				geciken_blit_1.__init__()
				geciken_blit_2.__init__()
				player.__init__()
				g.SCREEN = 'menu'
				g.kullanici_adi = ''
				l.__init__()
				if self.eski_tl > 1 :
					soru_1.soru_cekildi = False
					if self.eski_tl > 2 :
						soru_4.soru_cekildi = False
						if self.eski_tl > 3 :
							hack_2.__init__()
							soru_7.soru_cekildi = False
							if self.eski_tl > 5 :
								binary_1.rastgele_soru()
								binary_2.rastgele_soru()
								binary_3.rastgele_soru()
								tablo_binary.rastgele_soru()
								if self.eski_tl > 6 :
									soru_10.soru_cekildi = False
									if self.eski_tl > 7 :
										soru_13.soru_cekildi = False
										otest.__init__()
										if self.eski_tl > 9:
											game.__init__()
				if g.muzik == 0 :
					seskapali_butonu.dongu = True
					g.muzik = 1
				with sqlite3.connect("justhink.db") as con :
					cursor = con.cursor()
					try :
						cursor.execute("DROP TABLE justhink_data")
						con.execute("CREATE TABLE justhink_data(kullanici_adi TEXT,tamamlanan INT,muzik BOOL)")
						con.execute("INSERT INTO justhink_data(kullanici_adi,tamamlanan,muzik) VALUES(:b1,:b2,:b3)",{'b1':'','b2':0,'b3':1})
						cursor.execute("DROP TABLE justhink_soru")
					except :
						pass
					con.commit()
				self.__init__()
				ekran_gecisi_1.__init__()
#database'i kullanmak için bir nesne
db=DataBase()


####     EKRANA YAZI YAZDIRMA
def text_blit(text,yazikonumu_x,yazikonumu_y,yaziY=14,renk="siyah",ort_x = 0,ort = 800):
	font=pygame.font.SysFont("Helvetica",yaziY)
	if renk == "siyah":
		yazi = font.render(text,1,(0,0,0))
	elif renk == "beyaz":
		yazi = font.render(text,1,(255,255,255))
	elif renk == 'kirmizi':
		yazi = font.render(text,1,(204,0,0))
	elif renk == 'yesil':
		yazi = font.render(text,1,(0,204,0))
	yaziX = yazi.get_size()[0]
	if yazikonumu_x == "ortala":
		yazikonumu_x = ort_x + ((ort-yaziX) // 2)
	g.pencere.blit(yazi,(yazikonumu_x,yazikonumu_y))
class Geciken_yazi() :
	def __init__(self):
		self.dongu = True
		self.i = 0
		self.gecik = 0
		self.max_ = 0
		self.cumle = ""
		self.font=pygame.font.SysFont("Helvetica",18)
	def ciz(self,text,yazikonumu_x,yazikonumu_y) :
		if not (self.cumle in text):
			self.i = 0
			self.gecik = 0
			self.max_ = 0
			self.cumle = ""
		if self.gecik == self.max_ and self.dongu == True:
			self.cumle += text[self.i]
			if len(self.cumle) < len(text) :
				self.i += 1
			if self.cumle != text :
				self.max_+=4
		if self.cumle != text and self.i < len(text) and self.dongu == True:
			self.gecik+=1
			yazi = self.font.render(self.cumle,1,(255,255,255))
		else :
			self.dongu = False
			self.i = 0
			self.gecik = 0
			self.max_ = 0
			self.cumle = ""
			yazi = self.font.render(text,1,(255,255,255))
		g.pencere.blit(yazi,(yazikonumu_x,yazikonumu_y))

# geciken yazı komutunu vermek için bir nesne olusturdum
geciken_blit_1 = Geciken_yazi()
geciken_blit_2 = Geciken_yazi()

def tablo1():
	text_blit('Cevabınızı girip ENTER\'a basınız','ortala',292)
	text_blit('Aritmetik operatörler:',200,20,24)
	text_blit('+',200,48,24)
	text_blit('-',200,76,24)
	text_blit('*',200,104,24)
	text_blit('/',200,132,24)
	text_blit('%',200,160,24)
	text_blit('**',200,188,24)
	text_blit('//',200,216,24)

	text_blit('Toplama',320,48,24)
	text_blit('Çıkarma',320,76,24)
	text_blit('Çarpma',320,104,24)
	text_blit('Bölme',320,132,24)
	text_blit('Mod Alma',320,160,24)
	text_blit('Üs Alma',320,188,24)
	text_blit('Tam Bölme',320,216,24)

	text_blit('Örnek:',500,20,24)
	text_blit('2 + 3 = 5',500,48,24)
	text_blit('3 - 2 = 1',500,76,24)
	text_blit('3 * 2 = 6',500,104,24)
	text_blit('3 / 2 = 1.5',500,132,24)
	text_blit('5 % 2 = 1',500,160,24)
	text_blit('2 ** 3 = 8',500,188,24)
	text_blit('3 // 2 = 1',500,216,24)

def tablo2():
	pygame.draw.rect(g.pencere,(40,40,40),(400,20,2,112),0)
	text_blit('Cevabınızı girip ENTER\'a basınız','ortala',292)
	text_blit('İnput:',105,20,24)
	text_blit('~İşlenmesi için verilen bilgi.',105,48,24)
	text_blit('~Girdi, veri girişi.',105,76,24)
	text_blit('~Üretim faktörleri.',105,104,24)
	text_blit('Output:',412,20,24)
	text_blit('~İşlenmiş, alınan bilgi.',412,48,24)
	text_blit('~Çıktı, veri Çıkışı.',412,76,24)
	text_blit('~elde edilen Ürün.',412,104,24)

	text_blit('Örneğin:','ortala',132,24)
	text_blit('Yenilenebilir enerji kullanımı input, tükenmeyen enerji outputu;',95,160,24)
	text_blit('Fosil yakıt kullanımı input, küresel ısınma outputudur.',95,188,24)

def tablo3():
	text_blit('Cev□bın□zı girip ENTER\'a b□sınız','ortala',292)
	text_blit('İlişkisel operatörle□:',200,20,24)
	text_blit('==(is)',200,48,24)
	text_blit('!=(is not)',200,76,24)
	text_blit('>',200,104,24)
	text_blit('<',200,132,24)
	text_blit('>=',200,160,24)
	text_blit('<=',200,188,24)

	text_blit('Eşit□ir',320,48,24)
	text_blit('Eşit değ□ldir',320,76,24)
	text_blit('Büyüktür',320,104,24)
	text_blit('Küç□ktür',320,132,24)
	text_blit('Büyük\\eşittir',320,160,24)
	text_blit('Küçük\\e□ittir',320,188,24)

	text_blit('Örnek:',500,20,24)
	text_blit('(2 == 3) #Fal□e',500,48,24)
	text_blit('(2 != 3) #True',500,76,24)
	text_blit('(3 > 3) #False',500,104,24)
	text_blit('(7 < 4) #□alse',500,132,24)
	text_blit('(3 >= 3) #T□ue',500,160,24)
	text_blit('(2 <= 4) #True',500,188,24)

	text_blit("~İlişkis□l op□ratörlerde output(sonuç) sadec□ True(1) ya da False(0) olur.",95,224,18)
	text_blit("~İnput(Sö□lenen ilişki) doğruysa out□ut True'dur, yanlışsa False'dur.",95,246,18)

def tablo4():
	pygame.draw.rect(g.pencere,(40,40,40),(152,20,64,170),2)
	ort_x = 152
	kat = 7
	for i in range (0,8) :
		text_blit('2','ortala',26,32,'siyah',ort_x,64)
		text_blit('**','ortala',64,32,'siyah',ort_x,64)
		text_blit(f'{kat}','ortala',102,32,'siyah',ort_x,64)
		text_blit(f'{tablo_binary.cevap[-(kat+1)]}','ortala',150,32,'siyah',ort_x,64)
		kat -= 1
		ort_x += 62
	pygame.draw.rect(g.pencere,(40,40,40),(214,20,64,170),2)
	pygame.draw.rect(g.pencere,(40,40,40),(276,20,64,170),2)
	pygame.draw.rect(g.pencere,(40,40,40),(338,20,64,170),2)
	pygame.draw.rect(g.pencere,(40,40,40),(400,20,64,170),2)
	pygame.draw.rect(g.pencere,(40,40,40),(462,20,64,170),2)
	pygame.draw.rect(g.pencere,(40,40,40),(524,20,64,170),2)
	pygame.draw.rect(g.pencere,(40,40,40),(586,20,64,170),2)
	pygame.draw.rect(g.pencere,(40,40,40),(152,142,496,2),0)

	text_blit('İkili sayı sisitemi "Binary", onluk sisteme çevirme rastgele örnek:','ortala',4, 14)
	text_blit('Sayıların ikili sistem hallerini girip ENTER\'a basınız','ortala',292)
	text_blit(f"{tablo_binary.cevap[0]}(2**7)+{tablo_binary.cevap[1]}(2**6)+{tablo_binary.cevap[2]}(2**5)+{tablo_binary.cevap[3]}(2**4)+{tablo_binary.cevap[4]}(2**3)+{tablo_binary.cevap[5]}(2**2)+{tablo_binary.cevap[6]}(2**1)+{tablo_binary.cevap[7]}(2**0) ={tablo_binary.soru}'dur",'ortala',202,18)
	text_blit("Sondan başlayarak her sayı bulunduğu basamağa göre 2’nin üssü ile çarpılır,",85,224,18)
	text_blit("her sola gelindiğinde 2'nin üssü 1 artar ve bu üslü sayı input değeri(1/0) ile",85,246,18)
	text_blit("çarpılır en sonunda bu sayılar toplanarak output olan sayıya ulaşılır.",85,268,18)

def tablo5():
	text_blit('Cevabınızı girip ENTER\'a basınız','ortala',292)
	text_blit('Mantıksal operatörler:',100,20,24)
	text_blit('and(ve)',100,48,24)
	text_blit('or(veya)',100,104,24)
	text_blit('not(değil)',100,160,24)

	text_blit('~Her iki durumda doğruy-',220,48,24)
	text_blit('sa sonuç doğru.',220,76,24)
	text_blit('~Herhangi bir durum doğ-',220,104,24)
	text_blit('ruysa sonuç doğru.',220,132,24)
	text_blit('~Durumu ters çevir',220,160,24)

	text_blit('Örnek:',505,20,24)
	text_blit('1 and 0 #False',505,48,24)
	text_blit('2<3 and 1 #True',505,76,24)
	text_blit('1 or 0 #True',505,104,24)
	text_blit('2!=2 or 0 #False',505,132,24)
	text_blit('not 2>3 #True',505,160,24)
	text_blit('Çevreyi kirletme and kirletenleri uyar #True','ortala',216,24)
	text_blit('(1 ler, 0 lar "bool"dur ve bool olan 0(False) harici her şey doğruyu temsil eder)','ortala',244,18)
def tablo6():
	text_blit('Cevabınızı girip ENTER\'a basınız','ortala',292)
	text_blit('Fonksiyonlar:',100,20,24)
	text_blit('~Kelime anlamı; işlev, görevdir.',100,48,24)
	text_blit('~Matematikte değişken sayıları girdi olarak kabul edip bunlar-',100,76,24)
	text_blit('dan bir çıktı sayısı oluşmasını sağlayan kurallardır.',100,104,24)
	text_blit('~Bir işlem türüdür.',100,132,24)
	text_blit('~f(x) = x**2 ise f(4) = 16 olur. f(x) = x*(x-1) ise f(7) = 42 olur',95,188,24)
	text_blit('~Yazılımda fonksiyonların outputu "return" ile belirtilir',95,216,24)
def tablo7():
	pygame.draw.rect(g.pencere,(40,40,40),(400,350,2,112),0)
	text_blit('OYUN BAŞLIKLARINDAN SEÇTİĞİNİZE ÇİFT TIKLAYIN.','ortala',292)
	text_blit('Video oyunlarının çalışma prensibi:',100,20,24)
	text_blit(' ~Tüm video oyunlarında ana bir döngü vardır ve saniyede',100,48,24)
	text_blit('  (fps sınırına göre) yüzlerce kez bu döngü çalışır.',100,76,24)
	text_blit('Bu döngü şunlardan oluşur:',100,132,24)
	text_blit(' ~İnput(fare, klavye\'den) alınır, W Tuşuna tıklandı.',100,160,24)
	text_blit(' ~İnputlara göre işlem yapılır, Karakteri 10 adım ilerlet.',100,188,24)
	text_blit(' ~Seçilen outputlar ekrana yansıtılır, Karakteri çiz.',100,216,24)
	text_blit('Klasik Yılan oyunu !',100,350,24)
	text_blit('Yemler 10 puan kazandırır,',100,378,24)
	text_blit('1000 puan ol ve kazan.',100,406,24)
	text_blit('Yön Tuşlarını kullan !',100,434,24)
	text_blit('Klasik Pong oyunu !',412,350,24)
	text_blit('Bir zamalayıcı var,',412,378,24)
	text_blit('180 saniye dayan ve kazan.',412,406,24)
	text_blit('W, S ve Yön tuşlarını kullan !',412,434,24)
def tablo8():
	text_blit('BAŞLAMAK İÇİN ÇİFT TIKLAYIN.','ortala',500)
	text_blit('Video oyunlarının yayılma prensibi:',100,20,24)
	text_blit(' ~Yayılması erişiminin kolaylağı ile doğru orantılıdır.',100,48,24)
	text_blit('  İnternetteki, ücretsiz oyunu indirmek daha kolaydır.',100,76,24)
	text_blit('Senin yapman gerekense:',100,132,24)
	text_blit(' ~Bilgisayarın oyunu internete yüklerken onu korumak!',100,160,24)
	text_blit(' ~Virus, Trojen, Solucanlar rastgele aralıklarla,',100,188,24)
	text_blit(' ~Kendi özelliklerine(can,hasar,hız,hedef) göre,',100,216,24)
	text_blit(' ~Bilgisayarın kendilerine has Yerine saldırırlar.',100,244,24)
	text_blit('Şövalye\'nin Kontrolleri:',100,272,24)
	text_blit(' ~"A,D" tuşlarıyla ileri geri,',100,300,24)
	text_blit(' ~"W" tuşuyla zıplama(double-jump üst yola çıkarır),',100,328,24)
	text_blit(' ~"S" tuşuyla düşme(mevcutsa, alt yola indirir),',100,356,24)
	text_blit(' ~fare tuşlarıyla saldırı yapılır.',100,384,24)
	text_blit('Amacın %5 ile başlayan ilerlemeni tamamlamak.',100,440,24)
	text_blit('Düşman; ölürse artar, bilgisayara ulaşırsa azalır.',100,468,24)
def tablo9():
	text_blit('OYUNU TAMAMLADIN !!!',100,20,24)
	text_blit(' ~Sonuna kadar oynadığın için çok teşekkürler.',100,48,24)
	text_blit(' ~Mevcut sürüm burda bitiyor.',100,76,24)
	text_blit('HATIRLATMA !!!',100,132,24)
	text_blit(' ~Bu oyundaki bilgiler python dili esaslıdır.',100,160,24)
	text_blit(' ~Gerçek bir oyun kodlamak için internetten',100,188,24)
	text_blit('yazılım dili öğrenebilirsin.',100,216,24)
	text_blit('ÖNEMLİ !!!',100,272,24)
	text_blit(' ~Oyundaki ilerlemeni ayarlardan sıfırlayabilirsin!',100,300,24)
	text_blit(' ~Oyunu kapatıp açarak her bölümü oynayabilirsin.',100,328,24)
	text_blit(' ~Referanslar kısmından referanslara ulaşabilirsin!',100,356,24)


##############      LABİRENT SINIFLARI #############
class Maze() :
	def __init__(self):
		self.cikis = None
		self.duvarlar = []
		self.M = 40
		self.N = 30
		self.maze = [
		0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
		0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
		0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,
		0,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,
		0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,
		0,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,
		0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,1,
		0,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,
		0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,1,
		0,1,0,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,
		0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,
		0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,
		0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,
		0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,
		0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,1,
		0,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,
		0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,
		0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,
		0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,
		0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,
		0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,
		0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,
		0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,1,
		0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,0,1,
		0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,
		0,1,1,1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,
		0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,
		0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,
		0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,2,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,
		0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
			]

	def draw(self):
		bx = 0
		by = 0
		for i in range(0,self.M*self.N):
			if self.maze[ bx + (by*self.M) ] == 1:
				duvar_konumu = (bx * 20 , by * 20)
				g.pencere.blit(block_surf,duvar_konumu)
				self.duvarlar.append(duvar_konumu)
			elif self.maze[ bx + (by*self.M) ] == 2:
				self.cikis_konumu = bx * 20 , by * 20
				g.pencere.blit(bitis_surf,self.cikis_konumu)
			bx = bx + 1
			if bx > self.M-1:
				bx = 0 
				by = by + 1
maze = Maze()

class Player() :
	def __init__(self) :
		self.x = 360
		self.y = 560
		self.hiz = 20
		self.duvarlar = maze.duvarlar
		self.ilerle = 1
		self.dongu = True

	def kontrol(self,event):
		if (event.key == K_RIGHT):
			if (self.x + self.hiz,self.y) in self.duvarlar:
				self.ilerle = 0
			self.x = self.x + self.hiz*self.ilerle
		elif (event.key == K_LEFT):
			if (self.x - self.hiz,self.y) in self.duvarlar:
				self.ilerle = 0
			self.x = self.x - self.hiz*self.ilerle
		elif (event.key == K_UP):
			if (self.x,self.y - self.hiz) in self.duvarlar:
				self.ilerle = 0
			self.y = self.y - self.hiz*self.ilerle
		elif (event.key == K_DOWN):
			if (self.x,self.y + self.hiz) in self.duvarlar:
				self.ilerle = 0
			self.y = self.y + self.hiz*self.ilerle
		self.ilerle = 1
		if maze.cikis_konumu == (self.x,self.y) :
			self.dongu = False

player = Player()


##############      BUTON SINIFI     ###############
class Button():
	def __init__(self, image, basilmis_image, x_konum, y_konum,kontrol = False,center = True,ikili = False,baslangic = False):
		self.baslangic = baslangic
		self.dongu = False
		self.ikili = ikili

		self.kontrol = kontrol
		self.deger = False
		self.image = image
		self.basilmis_image = basilmis_image
		self.x_konum = x_konum
		self.y_konum = y_konum
		if center :
			self.rect = self.image.get_rect(center=(self.x_konum, self.y_konum))
		else :
			self.rect = self.image.get_rect(topleft=(self.x_konum, self.y_konum))

	def checkForInput(self, position):
		if self.kontrol == False :
			if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
				self.dongu = True
		elif self.kontrol == True :
			if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
				if self.deger == True :
					self.dongu = True
					self.deger = False
				else :
					self.deger = True
			else :
				self.deger = False

	def changeColor(self, position):
		if self.basilmis_image != None:
			if not self.ikili:
				if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
					g.pencere.blit(self.basilmis_image, self.rect)
				else:
					g.pencere.blit(self.image, self.rect)
			else :
				if self.baslangic :
					g.pencere.blit(self.image, self.rect)
				else:
					g.pencere.blit(self.basilmis_image, self.rect)
		else:
			g.pencere.blit(self.image, self.rect)

###  BUTONLARI OLUŞTURMA ###
oyna_butonu = Button(oyna_butonu_yuzey,oyna_butonu_basilmis_yuzey,399,300)
ozelt_butonu = Button(ozelt_butonu_yuzey,ozelt_butonu_basilmis_yuzey,149,535)
ayarlar_butonu = Button(ayarlar_butonu_yuzey,ayarlar_butonu_basilmis_yuzey,399,520)
referanslar_butonu = Button(referanslar_butonu_yuzey,referanslar_butonu_basilmis_yuzey,649,535)
geri_butonu = Button(geri_butonu_yuzey,geri_butonu_basilmis_yuzey,35,35)
dialog_butonu = Button(dialog_butonu_yuzey,dialog_butonu_basilmis_yuzey,455,578)
masaustu_butonu = Button(masaustu_butonu_yuzey,masaustu_butonu_basilmis_yuzey,386,305)
muzikacik_butonu = Button(masaustu_butonu_yuzey,masaustu_butonu_basilmis_yuzey,386,305)
sesacik_butonu = Button(sesacik_butonu_yuzey,sesacik_butonu_basilmis_yuzey,400,325)
seskapali_butonu = Button(seskapali_butonu_yuzey,seskapali_butonu_basilmis_yuzey,400,325)
ok_butonu = Button(ok_butonu_yuzey,ok_butonu_basilmis_yuzey,423,354)

sifirla_butonu = Button(sifirla_butonu_yuzey,sifirla_butonu_basilmis_yuzey,400,200,True)

level_butonlari = [
Button(seckare_butonu_yuzey,seckare_butonu_basilmis_yuzey,80,230,False,False) ,
Button(seckare_butonu_yuzey,seckare_butonu_basilmis_yuzey,170,328,False,False) ,
Button(secunlem_butonu_yuzey,secunlem_butonu_basilmis_yuzey,230,300,False,False) ,
Button(seckare_butonu_yuzey,seckare_butonu_basilmis_yuzey,261,328,False,False) ,
Button(seckare_butonu_yuzey,seckare_butonu_basilmis_yuzey,350,230,False,False) ,
Button(secunlem_butonu_yuzey,secunlem_butonu_basilmis_yuzey,410,202,False,False) ,
Button(seckare_butonu_yuzey,seckare_butonu_basilmis_yuzey,441,230,False,False) ,
Button(seckare_butonu_yuzey,seckare_butonu_basilmis_yuzey,441,328,False,False) ,
Button(seckare_butonu_yuzey,seckare_butonu_basilmis_yuzey,441,230,False,False) ,
Button(seckare_butonu_yuzey,seckare_butonu_basilmis_yuzey,530,230,False,False) ,
Button(seckare_butonu_yuzey,seckare_butonu_basilmis_yuzey,620,328,False,False) ,
Button(secfinal_butonu_yuzey,secfinal_butonu_basilmis_yuzey,712,0,False,False)
]


class soru_butonu() :
	def __init__(self,box_y,level,soru_sayisi,db=True):
		self.db = db
		self.level = level
		self.liste = []
		self.sayi = None
		self.soru = None
		self.cevap = None
		self.soru_sayisi = soru_sayisi
		self.tablodaki_sorular = 0

		self.girdi = ""
		self.sonuc = None
 
		self.box_y = box_y
		self.font = pygame.font.SysFont("helvetica",24)
		self.color_acik = pygame.Color('lightskyblue3')
		self.color_koyu = pygame.Color('gray30')
		self.color_yesil = pygame.Color('green3')
		self.color = self.color_koyu
		self.text_butonu_aktif = False
		self.box_x = 350
		self.box_w = 0
		if self.db :
			if self.soru_sayisi == 1 :
				self.soru_cekildi = False
				for i in range(1,10):
					self.liste.append(((self.level-1)*10)+i)
		self.rastgele_soru()

	def rastgele_soru(self):
		if self.db :
			if self.soru_sayisi == 1 :
				self.sorular = sample(self.liste,k=3)
				self.sayi = self.sorular[0]
		else :
			self.sonuc = None
			self.soru = 0
			self.cevap = ''
			self.kat = 1
			self.liste = []
			for i in range(0,8):
				self.liste.append(randint(0,1))
			for i in self.liste :
				self.soru += self.kat*i
				self.kat *= 2
				self.cevap = str(i) + self.cevap
			self.soru = str(self.soru)
	def soru_cek(self):
		if self.db :
			if self.soru_sayisi != 1 :
				if self.level == 1:
					self.sayi = soru_1.sorular[self.soru_sayisi-1]
					if self.soru_sayisi == 3 :
						soru_1.soru_cekildi = True
				elif self.level == 2:
					self.sayi = soru_4.sorular[self.soru_sayisi-1]
					if self.soru_sayisi == 3 :
						soru_4.soru_cekildi = True
				elif self.level == 3:
					self.sayi = soru_7.sorular[self.soru_sayisi-1]
					if self.soru_sayisi == 3 :
						soru_7.soru_cekildi = True
				elif self.level == 4:
					self.sayi = soru_10.sorular[self.soru_sayisi-1]
					if self.soru_sayisi == 3 :
						soru_10.soru_cekildi = True
				elif self.level == 5:
					self.sayi = soru_13.sorular[self.soru_sayisi-1]
					if self.soru_sayisi == 3 :
						soru_13.soru_cekildi = True
			with sqlite3.connect("justhink.db") as con :
				cursor = con.cursor()
				try:
					cursor.execute("SELECT * from justhink_soru")
					self.tablodaki_sorular = len(cursor.fetchall())
				except sqlite3.OperationalError:
					pass
				if self.soru_sayisi == 1 :
					try :
						con.execute("CREATE TABLE justhink_soru(soru TEXT,cevap TEXT,_id INT)")
						for i in range(1,10):
#						1. kurs sorular
							if i == 1 :
								bilgi_1,bilgi_2='Mario ((7-3) kere (5//2) adım ilerleyip) ,3 adım geri gelirse kaç adım ilerlemiş olur ?', '5'
							elif i == 2 :
								bilgi_1,bilgi_2='Mario (70//7,6) kere (3 adım geri 6 adım ileri) giderse kaç adım ilerlemiş olur ?', '27'
							elif i == 3 :
								bilgi_1,bilgi_2='Mario 3 adım ileri gidip (216-230) geri gelirse kaç adım ilerlemiş olur ?', '17'
							elif i == 4 :
								bilgi_1,bilgi_2='Mario ((3**2)*2 adım) geri gelip (8-33 kere) geri giderse kaç adım ilerlemiş olur ?', '7'
							elif i == 5 :
								bilgi_1,bilgi_2='Mario (2-5*2 adım) ilerleyip ((-3)*6/2 adım) geri gelirse kaç adım ilerlemiş olur ?', '1'
							elif i == 6 :
								bilgi_1,bilgi_2='Mario (5 adım) ileri (1*3-2/2) geri gelirse kaç adım gerilemiş olur ?', '-3'
							elif i == 7 :
								bilgi_1,bilgi_2='Mario (20*36)/(2*18) adım ileri ve (20 adım) geri gelirse kaç adım atmış olur ?', '40'
							elif i == 8 :
								bilgi_1,bilgi_2='Mario (2/3 kere 27 adım) ileri (10 adım) geri gelirse kaç adım atmış olur ?', '28'
							elif i == 9 :
								bilgi_1,bilgi_2='Mario 2(123%29 adım) ilerlerse kaç adım ilerlemiş olur ?', '14'

							con.execute("INSERT INTO justhink_soru(soru,cevap,_id) VALUES(:b1,:b2,:b3)",{'b1':bilgi_1,'b2':bilgi_2,'b3':i})
						con.commit()
					except sqlite3.OperationalError:
						if self.level == 2 and self.tablodaki_sorular <= 9:
							for i in range(11,20):
#							2. kurs sorular
								if i == 11 :
									bilgi_1,bilgi_2='Klavye hangisine bir örnektir ? (input, output)', 'input'
								elif i == 12 :
									bilgi_1,bilgi_2='Yazıcı hangisine bir örnektir ? (input, output)', 'output'
								elif i == 13 :
									bilgi_1,bilgi_2="inputu 5 ve 3 olduğunda, outputu -2 olabilen operatör(+, - ...vb) hangisidir ?", '-'	
								elif i == 14 :
									bilgi_1,bilgi_2='5 ve 7 inputuyla, 1 outputu elde edilebilecek operatör(+, - ...vb) hangisidir ?', '//'
								elif i == 15 :
									bilgi_1,bilgi_2='Gözlerimizin saniyede 60 fotoğraf çekmesi beyine ne sağlar ? (input, output)', 'input'
								elif i == 16 :
									bilgi_1,bilgi_2='Refleks, Beyincik sayesinde kısa sürede üretilen ... (inputtur,outputtur)', 'outputtur'
								elif i == 17 :
									bilgi_1,bilgi_2='İki tane rakam inputu ile çarpma operatöründen elde edilebilecek output sayısı kaçtır ?', '82'
								elif i == 18 :
									bilgi_1,bilgi_2='İki farklı çift sayı inputuyla 1 outputu verebilen operatör(+, - ...vb) hangisidir ?', '**'
								elif i == 19 :
									bilgi_1,bilgi_2='iki farklı sayı ve eksi operatörü ile yapılabilecek outputların toplamı kaçtır ?', '0'
								con.execute("INSERT INTO justhink_soru(soru,cevap,_id) VALUES(:b1,:b2,:b3)",{'b1':bilgi_1,'b2':bilgi_2,'b3':i})
							con.commit()
						elif self.level == 3 and self.tablodaki_sorular <= 18:
							for i in range(21,30):
#							3. kurs sorular
								if i == 21 :
									bilgi_1,bilgi_2='(Tasa□ruflu ampülün harcadığı enerji > Norm□l ampülün harcadığı enerji) = ?', 'False'
								elif i == 22 :
									bilgi_1,bilgi_2='(Işık □ızı == Ses hızı) = ?', 'False'
								elif i == 23 :
									bilgi_1,bilgi_2='"((2**3) _ (3**2)) = True" işlemind□ boşluğa hangi ilişkisel operatör gelm□lidir ?', '<'
								elif i == 24 :
									bilgi_1,bilgi_2='"((2//3) _ 0) = True" işlemi□de boşluğa hangi ilişkisel operatör gelmelidir ?', '=='
								elif i == 25 :
									bilgi_1,bilgi_2='"R□kamlar _ 0 = True" işleminde boşl□ğa hangi ilişkisel operatör gelmelidir ?', '>='
								elif i == 26 :
									bilgi_1,bilgi_2='"(x < 23) = Tr□e","(x < 12) = False" buna göre "x" kaç farklı tam sayı olabi□ir ?', '11'
								elif i == 27 :
									bilgi_1,bilgi_2='"(2<=x<12) = True","(x != 12) = □rue" buna gö□e "x" kaç farklı tam sayı olabilir ?', '10'
								elif i == 28 :
									bilgi_1,bilgi_2='"((x*2)-3) <= 63" buna göre "x" kaç farklı p□zitif tam sayı olabilir ?', '33'
								elif i == 29 :
									bilgi_1,bilgi_2='"1 Kb _ 1 byte" İşleminde boşluğa hangi il□şkisel operatör gelmelidir', '>'
								con.execute("INSERT INTO justhink_soru(soru,cevap,_id) VALUES(:b1,:b2,:b3)",{'b1':bilgi_1,'b2':bilgi_2,'b3':i})
							con.commit()
						elif self.level == 4 and self.tablodaki_sorular <= 27:
							for i in range(31,40):
#							4. kurs sorular
								if i == 31 :
									bilgi_1,bilgi_2='cevap "(False==1 or 1 _ 2)#True"için boşluğa gelebilecek bir operatördür.', '<'
								elif i == 32 :
									bilgi_1,bilgi_2='cevap "(False!=1 and 10**0 _ 2**1)#True" için boşluğa gelebilecek bir operatördür.', '>='
								elif i == 33 :
									bilgi_1,bilgi_2='"(x>2 or 12<=x+4)#True" için x kaç farklı tam sayı olabilir', '6'
								elif i == 34 :
									bilgi_1,bilgi_2='"not(x<2 and 12>x+4)#True" için x kaç farklı tam sayı olabilir', '7'
								elif i == 35 :
									bilgi_1,bilgi_2='"(not(2==2) or x)#False" için x hangi booldur(True/False) ?', 'False'
								elif i == 36 :
									bilgi_1,bilgi_2='"True != not(False) and 1" işleminin outputu nedir(True/False) ?', 'False'
								elif i == 37 :
									bilgi_1,bilgi_2='"((10/3)<2 and x)#False" için x kaç farklı bool olabilir ?', '1'
								elif i == 38 :
									bilgi_1,bilgi_2='"((3//10)<=0 or x)#True" için x kaç farklı bool olabilir ?', '2'
								elif i == 39 :
									bilgi_1,bilgi_2='"(a+x<2 ve a=-3)#True" için x kaç farklı pozitif tam sayı olabilir ?','4'
								con.execute("INSERT INTO justhink_soru(soru,cevap,_id) VALUES(:b1,:b2,:b3)",{'b1':bilgi_1,'b2':bilgi_2,'b3':i})
							con.commit()
						elif self.level == 5 and db.eski_tl <= 36:
							for i in range(41,50):
#							5. kurs sorular
								if i == 41 :
									bilgi_1,bilgi_2='f(q)=q*(1/3) ise kaç farklı rakam inputu ile tam sayı outputu elde edilebilir ?', '4'
								elif i == 42 :
									bilgi_1,bilgi_2='f(A)=A/(1/2) ise kaç farklı rakam inputu ile tam sayı outputu elde edilebilir ?', '10'
								elif i == 43 :
									bilgi_1,bilgi_2='f(2a+3)=(a**2)+10 ise f(7)\'nin outputu nedir?', '14'
								elif i == 44 :
									bilgi_1,bilgi_2='f(a**2)=(a**2)-a*2 ise f(16)\'nın outputu nedir?', '8'
								elif i == 45 :
									bilgi_1,bilgi_2='f(2a,b)=(2b/a) ise f(4,3)\'nin outputu nedir?', '3'
								elif i == 46 :
									bilgi_1,bilgi_2='f(konum,adım,uzunluk): return konum+(adım*uzunluk) ise f(20,5,12) = ?', '80'
								elif i == 47 :
									bilgi_1,bilgi_2='f(x)=x*2  ise f(5)*f(3) = ?', '60'
								elif i == 48 :
									bilgi_1,bilgi_2='f(y)=y//2 ve g(z)=z*2 ise g(g(6)) // f(g(3)) = ?', '8'
								elif i == 49 :
									bilgi_1,bilgi_2='f(y)=y*2 ve g(f(z))=(z+2)//2 ise g(6) = ?', '2'
								con.execute("INSERT INTO justhink_soru(soru,cevap,_id) VALUES(:b1,:b2,:b3)",{'b1':bilgi_1,'b2':bilgi_2,'b3':i})
							con.commit()

				cursor.execute("SELECT * from justhink_soru WHERE _id =:sayi",{'sayi':self.sayi})
				for i in cursor.fetchall() :
					self.soru = i[0]
					self.cevap = i[1]

	def mousedown_kontrol(self,position):
		if not self.sonuc :
			if self.input_rect.collidepoint(position) :
				self.text_butonu_aktif = True
			elif not self.input_rect.collidepoint(position) :
				self.text_butonu_aktif = False
	def key_kontrol(self,event):
		if not self.sonuc :
			if self.text_butonu_aktif == True :
				if event.key == pygame.K_BACKSPACE:
					self.girdi = self.girdi[:-1]
				elif event.key == pygame.K_RETURN :
					if self.girdi == self.cevap :
						self.sonuc = True
					else :
						self.sonuc = False
				elif len(self.girdi)<=10:
					self.girdi += event.unicode
	def ciz(self):
		text_blit(self.soru,'ortala',self.box_y - 40,18)
		if self.sonuc == True:
			self.color = self.color_yesil
			text_blit('Cevabınız Doğru !','ortala',self.box_y + 24,18,'yesil')
		else :
			if self.text_butonu_aktif :
				self.color = self.color_acik
			else :
				self.color = self.color_koyu
			if self.sonuc == False :
				text_blit('Cevabınız Yanlış !','ortala',self.box_y + 24,18,'kirmizi')
		if self.sonuc == True:
			g.pencere.blit(self.text_surface,(self.input_rect.x + 5,self.input_rect.y + 5))
			pygame.draw.rect(g.pencere,self.color,self.input_rect,2)
		else : 
			self.input_rect = pygame.Rect(self.box_x,self.box_y-16,self.box_w,32)
			self.text_surface = self.font.render(self.girdi,True,(0,0,0))
			pygame.draw.rect(g.pencere,self.color,self.input_rect,2)
			g.pencere.blit(self.text_surface,(self.input_rect.x + 5,self.input_rect.y + 5))
			self.box_x = 400 - max(50,self.text_surface.get_width() // 2)
			self.box_w = max(100,self.text_surface.get_width() + 10)

#	soru-cevap butonları :
soru_1 = soru_butonu(350,1,1)
soru_2 = soru_butonu(450,1,2)
soru_3 = soru_butonu(550,1,3)
soru_4 = soru_butonu(350,2,1)
soru_5 = soru_butonu(450,2,2)
soru_6 = soru_butonu(550,2,3)
soru_7 = soru_butonu(350,3,1)
soru_8 = soru_butonu(450,3,2)
soru_9 = soru_butonu(550,3,3)
soru_10 = soru_butonu(350,4,1)
soru_11 = soru_butonu(450,4,2)
soru_12 = soru_butonu(550,4,3)
soru_13 = soru_butonu(350,5,1)
soru_14 = soru_butonu(450,5,2)
soru_15 = soru_butonu(550,5,3)

binary_1 = soru_butonu(350,None,None,False)
binary_2 = soru_butonu(450,None,None,False)
binary_3 = soru_butonu(550,None,None,False)
tablo_binary = soru_butonu(0,None,None,False)


class ad_alma_butonu() :
	def __init__(self,box_y):
		self.dongu = True 
		self.box_y = box_y
		self.font = pygame.font.SysFont("helvetica",24)
		self.color_acik = pygame.Color('lightskyblue3')
		self.color_koyu = pygame.Color('gray30')
		self.color = self.color_koyu
		self.text_butonu_aktif = False
		self.box_x = 350
		self.box_w = 0
	
	def mousedown_kontrol(self,event,position):
		if self.input_rect.collidepoint(position) :
			self.text_butonu_aktif = True
		elif not self.input_rect.collidepoint(position) :
			self.text_butonu_aktif = False
	def key_kontrol(self,event):
		if self.text_butonu_aktif == True :
			if event.key == pygame.K_BACKSPACE:
				g.kullanici_adi= g.kullanici_adi[:-1]
			elif event.key == pygame.K_RETURN :
				self.dongu=False
			elif len(g.kullanici_adi)<=20:
				g.kullanici_adi += event.unicode
	def ciz(self):
		if self.text_butonu_aktif :
			self.color = self.color_acik
		else :
			self.color = self.color_koyu
		self.input_rect = pygame.Rect(self.box_x,self.box_y-16,self.box_w,32)
		self.text_surface = self.font.render(g.kullanici_adi,True,(255,255,255))
		pygame.draw.rect(g.pencere,self.color,self.input_rect,2)
		g.pencere.blit(self.text_surface,(self.input_rect.x+5,self.input_rect.y+5))
		self.box_x = 400 - max(50,self.text_surface.get_width()//2)
		self.box_w = max(100,self.text_surface.get_width() + 10)
		db.update('ka')
		
### Text inputu alan butonları oluşturma
ad_al_butonu = ad_alma_butonu(300)
ad_degis_butonu = ad_alma_butonu(500)


class Hack_2():
	def __init__(self):
		self.x,self.y = 175,40
		self.satir = 1
		self.istenen_1 = randint(2,25)
		self.sonuc = False
		self.baslangic = []
		for i in range(1,28):
			self.baslangic.append(randint(0,1))
		self.buton_list = []
		for i in range(1,28):
			self.buton_list.append(Button(dosya1_image, dosya0_image, self.x, self.y,False,False,True,self.baslangic[i-1]))
			if i == 5 or i == 11 or i == 16 or i == 22:
				self.y += 90 
				self.satir +=1
				if self.satir % 2 == 0 :
					self.x = 125
				else :
					self.x = 175
			else :
				self.x += 100
		if self.baslangic.count(1) == self.istenen_1 :
			self.__init__()
	def kontrol(self,pos):
		for i in range(0,27):
			self.buton_list[i].checkForInput(pos)
			if self.buton_list[i].dongu == True :
				if self.buton_list[i].baslangic :
					self.buton_list[i].baslangic = False
					self.baslangic.pop(i)
					self.baslangic.insert(i,0)
				else :
					self.buton_list[i].baslangic = True
					self.baslangic.pop(i)
					self.baslangic.insert(i,1)
				self.buton_list[i].dongu = False
				
	def ciz(self,pos):
		for i in range(0,27):
			self.buton_list[i].changeColor(pos)
		if self.baslangic.count(1) == self.istenen_1 :
			self.sonuc = True
hack_2 = Hack_2()


##############      LİNKLENMİŞ YAZI SINIFI     ###############
class buton_yazi():
	def __init__(self,yazi,x_konum,y_konum,link = None,yaziY = 18):
		self.link = link
		if self.link != None:
			self.link_rengi = (155,205,255)
		else :
			self.link_rengi = (0,0,0)
		self.link = link
		self.yazi = yazi
		self.x_konum = x_konum
		self.y_konum = y_konum
		self.yaziY = yaziY
		self.link_font=pygame.font.SysFont("Helvetica",self.yaziY)
		self.rect = None
		self.cizgi_koy = False
		self.deger = False
		self.sonuc = False

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			if self.deger == True :
				if self.link != None:
					webbrowser.open_new_tab(self.link)
				else:
					self.sonuc = True
				self.deger = False
				self.cizgi_koy = False
			else :
				self.deger = True
				self.cizgi_koy = True
		else :
			self.deger = False
			self.cizgi_koy = False
	def draw(self):
		self.rect = g.pencere.blit(self.link_font.render(self.yazi, True, self.link_rengi), (self.x_konum, self.y_konum))
		if self.cizgi_koy :
			pygame.draw.rect(g.pencere, self.link_rengi, (self.x_konum, self.y_konum + self.yaziY + 1, self.rect.width,3), 0)
link_list = [
buton_yazi('Python yazılım dilinin ana sitesi',60,120,'https://www.python.org/'),
buton_yazi('Günlük gifi referans linki',80,208,'www.pinterest.com/pin/413627547020018011/'),
buton_yazi('Bilgisayar görseli referans linki',80,252,'https://www.istockphoto.com/tr/vekt%C3%B6r/piksel-siyah-diz%C3%BCst%C3%BC-bilgisayar-detayl%C4%B1-izole-vekt%C3%B6r-gm1033906652-276850151'),
buton_yazi('System hacked görsel referans linki',80,296,'https://mystickermania.com/sticker-packs/into-the-web/windows-error-your-system-is-hacked'),
buton_yazi('Şövalye animasyonları referans linki',80,340,'https://www.artstation.com/artwork/WWzxJ'),
buton_yazi('Virus görselleri referans linki',80,384,'https://www.dreamstime.com/pixel-art-covid-virus-icon-set-animation-frame-process-steps-image200468657')]

otest_list =[buton_yazi('-> Yılan Oyunu <-',100,320,None,24), buton_yazi('-> Pong Oyunu <-',412,320,None,24)]
fgame_buton = buton_yazi('-> Oyunu internete yüklemeye başla <-',200,520,None,24)

########## Daha iyi görüntü için geçiş animasyon sınıfları
class ekran() :
	def __init__(self):
		self.gecis = 0
		self.dongu = True
		self.renk_6 = 0,0,0
		self.renk_5 = 55,55,55
		self.renk_4 = 105,105,105
		self.renk_3 = 155,155,155
		self.renk_2 = 205,205,205
		self.renk_1 = 230,230,230
	def yap(self,yon):
		if yon == "beyaz" :
			self.renk_1 = 25,25,25
			self.renk_2 = 50,50,50
			self.renk_3 = 100,100,100
			self.renk_4 = 150,150,150
			self.renk_5 = 200,200,200
			self.renk_6 = 255,255,255
		elif yon == "siyah" :
			self.renk_6 = 0,0,0
			self.renk_5 = 55,55,55
			self.renk_4 = 105,105,105
			self.renk_3 = 155,155,155
			self.renk_2 = 205,205,205
			self.renk_1 = 230,230,230
		if self.gecis <=180 :
			if self.gecis<=35:
				g.pencere.fill((self.renk_1))
			elif self.gecis<=70:
				g.pencere.fill((self.renk_2))
			elif self.gecis<=105:
				g.pencere.fill((self.renk_3))
			elif self.gecis<=140:
				g.pencere.fill((self.renk_4))
			elif self.gecis<=175:
				g.pencere.fill((self.renk_5))
			else:
				g.pencere.fill((self.renk_6))
			self.gecis += 1
		else :
			self.dongu = False
			self.gecis = 0
### ekran geçisi nesnesi
ekran_gecisi_1 = ekran()
ekran_gecisi_2 = ekran()


class Dialog_kutusu() :
	def __init__(self):
		self.dialogdongunun_sayisi = 0
		self.dialog_yapildi = False
		self.sayi = 21
	def ciz(self,konusan) :
		if dialog_butonu.dongu == True :
			if self.dialogdongunun_sayisi <= 7:
				g.pencere.blit(dialogkutusu_image,(0,429 + int(self.sayi)))
				self.dialogdongunun_sayisi += 0.2
				self.sayi += 5
			else :
				l.dialog = False
				self.dialogdongunun_sayisi = 0
				dialog_butonu.dongu = False
				self.sayi = 0
		else:
			l.dialog = True
			g.pencere.blit(dialogkutusu_image,(0,429))
			dialog_butonu.changeColor((g.x,g.y))
			if konusan == "kullanici" :
				g.pencere.blit(kullanici_image,(22,460))
			elif konusan == 'yuz_1' :
				g.pencere.blit(yuz1_image,(29,480))
			elif konusan == 'yuz_2' :
				g.pencere.blit(yuz2_image,(29,480))
			elif konusan == 'yuz_3' :
				g.pencere.blit(yuz3_image,(29,480))
			elif konusan == 'yuz_4' :
				g.pencere.blit(yuz4_image,(29,480))
	
#
dialog_kutusu = Dialog_kutusu()
dialog_kutusu_2 = Dialog_kutusu()


class level_sec() :
	def __init__(self):
		self.buton_sayisi = 1
		self.wall_x = 230
		self.deger_atandi = False

		self.cikti = None

	def girdi(self):
		for i in range(0,self.buton_sayisi+1) :
			if not (i == 6 and db.eski_tl > 5):
				level_butonlari[i].checkForInput((g.x,g.y))
				if level_butonlari[i].dongu == True :
					self.cikti = i
					level_butonlari[i].dongu = False
					break

	def boya(self):
		g.pencere.blit(levelsec_image,(0,0))
		if not self.deger_atandi :
			if db.eski_tl == 2 :
				self.buton_sayisi = 3
				self.wall_x = 320
			elif db.eski_tl == 3 :
				self.buton_sayisi = 4
				self.wall_x = 410
			elif db.eski_tl == 4 :
				self.buton_sayisi = 6
				self.wall_x = 500
			elif db.eski_tl == 5 :
				self.buton_sayisi = 7
				self.wall_x = 500
			elif db.eski_tl == 6 :
				self.buton_sayisi = 8
				self.wall_x = 500
			elif db.eski_tl == 7 :
				self.buton_sayisi = 9
				self.wall_x = 590
			elif db.eski_tl == 8 :
				self.buton_sayisi = 10
				self.wall_x = 680
			elif db.eski_tl >= 9 :
				self.buton_sayisi = 11

			self.deger_atandi = True
		if db.eski_tl == 4 :
			g.pencere.blit(level6_gizle_image,(441,300))
		for i in range(0,self.buton_sayisi+1) :
			if not (i == 6 and db.eski_tl > 5):
				level_butonlari[i].changeColor((g.x,g.y))
		if db.eski_tl < 9 :
			g.pencere.blit(levelwall_image,(self.wall_x,0))
#
levelsec = level_sec()


####    LEVEL 9 OYUN TESTİ SINIFLARI ####
#	#	#			SNAKE	GAME
class Snake():
	def __init__(self):
		self.sonuc=False
		self.snake_speed = 15
		self.fps = pygame.time.Clock()
		self.snake_position = [100, 50]
		self.snake_body = [[100, 50],[90, 50],[80, 50],[70, 50]]
		self.fruit_position = [randint(6, (800//10)-1) * 10,randint(8, (600//10)-1) * 10]
		self.fruit_spawn = True
		self.direction = 'RIGHT'
		self.change_to = self.direction
		self.score = 0
		self.score_font = pygame.font.SysFont('Helvetica',20)
		self.my_font = pygame.font.SysFont('Helvetica', 50)
	def show_score(self):
		self.score_surface = self.score_font.render('Skor : ' + str(self.score), 1, (255,255,255))
		self.score_rect = self.score_surface.get_rect()
		g.pencere.blit(self.score_surface, (self.score_rect[0]+70,self.score_rect[1]+20))
	def game_over(self):
		if self.score >= 1000:
			self.game_over_surface = self.my_font.render('Kazandın!', True, (0,255,0))
			self.sonuc = True
		else :
			self.game_over_surface = self.my_font.render('Kaybettin puanın : ' + str(self.score), True, (255,0,0))
		self.game_over_rect = self.game_over_surface.get_rect()
		self.game_over_rect.midtop = (800/2, 275)
		g.pencere.blit(self.game_over_surface, self.game_over_rect)
		pygame.display.flip()
		sleep(2)
		if self.score < 1000:
			self.__init__()
	def checkForInput(self, event):
		if event.key == pygame.K_UP:
			self.change_to = 'UP'
		if event.key == pygame.K_DOWN:
			self.change_to = 'DOWN'
		if event.key == pygame.K_LEFT:
			self.change_to = 'LEFT'
		if event.key == pygame.K_RIGHT:
			self.change_to = 'RIGHT'

	def dongu(self):
		self.fps.tick(15)
		if self.change_to == 'UP' and self.direction != 'DOWN':
			self.direction = 'UP'
		if self.change_to == 'DOWN' and self.direction != 'UP':
			self.direction = 'DOWN'
		if self.change_to == 'LEFT' and self.direction != 'RIGHT':
			self.direction = 'LEFT'
		if self.change_to == 'RIGHT' and self.direction != 'LEFT':
			self.direction = 'RIGHT'

		if self.direction == 'UP':
			self.snake_position[1] -= 10
		if self.direction == 'DOWN':
			self.snake_position[1] += 10
		if self.direction == 'LEFT':
			self.snake_position[0] -= 10
		if self.direction == 'RIGHT':
			self.snake_position[0] += 10

		self.snake_body.insert(0, list(self.snake_position))
		if self.snake_position[0] == self.fruit_position[0] and self.snake_position[1] == self.fruit_position[1]:
			self.score += 10
			self.fruit_spawn = False
		else:
			self.snake_body.pop()
		
		if not self.fruit_spawn:
			self.fruit_position = [randint(6,(800//10)-1) * 10,randint(6, (600//10)-1) * 10]

		self.fruit_spawn = True
		g.pencere.fill((0,0,0))
		self.sayi = 0
		for pos in self.snake_body:
			pygame.draw.rect(g.pencere, (min(255,self.sayi//2),255,0),pygame.Rect(pos[0], pos[1], 10, 10))
			self.sayi += 50
		pygame.draw.rect(g.pencere, (255,255,255), pygame.Rect(self.fruit_position[0], self.fruit_position[1], 10, 10))

		if self.score >= 1000:
			self.game_over()
		if self.snake_position[0] < 0 or self.snake_position[0] > 800-10:
			self.game_over()
		if self.snake_position[1] < 0 or self.snake_position[1] > 600-10:
			self.game_over()
		for block in self.snake_body[1:]:
			if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
				self.game_over()
		self.show_score()

#	#	#			PONG	GAME
p_WIDTH, 	p_HEIGHT = 800, 600

p_PADDLE_WIDTH, p_PADDLE_HEIGHT = 20, 100
p_BALL_RADIUS = 7

p_ZAMAN_FONT = pygame.font.SysFont("Helvetica", 50)


class p_Paddle:
	COLOR = (255,255,255)
	VEL = 6

	def __init__(self, x, y, width, height):
		self.x = self.original_x = x
		self.y = self.original_y = y
		self.width = width
		self.height = height

	def draw(self, win):
		pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

	def move(self, up=True):
		if up:
			self.y -= self.VEL
		else:
			self.y += self.VEL

	def reset(self):
		self.x = self.original_x
		self.y = self.original_y


class p_Ball:
	MAX_VEL = 7
	COLOR = (255,255,255)

	def __init__(self, x, y, radius):
		self.x = self.original_x = x
		self.y = self.original_y = y
		self.radius = radius
		self.x_vel = self.MAX_VEL
		self.y_vel = choice([-3,-2,-1,1,2,3])

	def draw(self, win):
		pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

	def move(self):
		self.x += self.x_vel
		self.y += self.y_vel

	def reset(self):
		self.x = self.original_x
		self.y = self.original_y
		self.y_vel = choice([-3,-2,-1,1,2,3])
		self.x_vel *= -1


def p_draw(win, paddles, ball, zaman):
	win.fill((0,0,0))

	zaman = p_ZAMAN_FONT.render(str(zaman//60),1,(255,255,255),(0,0,0))

	for paddle in paddles:
		paddle.draw(win)

	for i in range(10, p_HEIGHT, p_HEIGHT//20):
		if i % 2 == 1:
			continue
		pygame.draw.rect(win, (255,255,255), (p_WIDTH//2 - 5, i, 10, p_HEIGHT//20))

	win.blit(zaman, (p_WIDTH//2 - zaman.get_width()//2, 20))
	ball.draw(win)



def p_handle_collision(ball, left_paddle, right_paddle):
	if ball.y + ball.radius >= p_HEIGHT:
		ball.y_vel *= -1
	elif ball.y - ball.radius <= 0:
		ball.y_vel *= -1

	if ball.x_vel < 0:
		if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
			if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
				ball.x_vel *= -1

				middle_y = left_paddle.y + left_paddle.height / 2
				difference_in_y = middle_y - ball.y
				reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
				y_vel = difference_in_y / reduction_factor
				ball.y_vel = -1 * y_vel

	else:
		if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
			if ball.x + ball.radius >= right_paddle.x:
				ball.x_vel *= -1

				middle_y = right_paddle.y + right_paddle.height / 2
				difference_in_y = middle_y - ball.y
				reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
				y_vel = difference_in_y / reduction_factor
				ball.y_vel = -1 * y_vel


def p_handle_paddle_movement(keys, left_paddle, right_paddle):
	if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
		left_paddle.move(up=True)
	if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= p_HEIGHT:
		left_paddle.move(up=False)

	if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
		right_paddle.move(up=True)
	if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= p_HEIGHT:
		right_paddle.move(up=False)


class p_main():
	def __init__(self):
		self.run = True
		self.clock = pygame.time.Clock()

		self.left_paddle = p_Paddle(10, p_HEIGHT//2 - p_PADDLE_HEIGHT //2, p_PADDLE_WIDTH, p_PADDLE_HEIGHT)
		self.right_paddle = p_Paddle(p_WIDTH - 10 - p_PADDLE_WIDTH, p_HEIGHT //2 - p_PADDLE_HEIGHT//2, p_PADDLE_WIDTH, p_PADDLE_HEIGHT)
		self.ball = p_Ball(p_WIDTH // 2, p_HEIGHT // 2, p_BALL_RADIUS)

		self.zaman = 0

	def dongu(self):
		self.clock.tick(60)
		self.zaman +=1
		p_draw(g.pencere, [self.left_paddle, self.right_paddle], self.ball, self.zaman)


		keys = pygame.key.get_pressed()
		p_handle_paddle_movement(keys, self.left_paddle, self.right_paddle)

		self.ball.move()
		p_handle_collision(self.ball, self.left_paddle, self.right_paddle)

		if self.ball.x < 0:
			self.zaman = 0
			self.ball.reset()
		elif self.ball.x > p_WIDTH:
			self.zaman = 0
			self.ball.reset()

		if self.zaman//60 >= 180:
			self.zaman = 0
			text = p_ZAMAN_FONT.render("Kazandın !", 1, (0,204,0),(0,0,0))
			g.pencere.blit(text, (p_WIDTH//2 - text.get_width() //2, p_HEIGHT//2 - text.get_height()//2))
			pygame.display.update()
			sleep(2)
			self.ball.reset()
			self.left_paddle.reset()
			self.right_paddle.reset()
			otest.sonuc = True


class Otest():
	def __init__(self):
		self.secilen = None
		self.snake = Snake()
		self.sonuc = False
		self.pong = p_main()

	def girdi_mouse(self):
		if self.secilen == None:
			for i in [0,1] :
				otest_list[i].checkForInput((g.x,g.y))
				if otest_list[i].sonuc :
					self.secilen = i
					otest_list[i].dongu = False
					break
	def girdi_key(self,event):
		if self.secilen == 0:
			self.snake.checkForInput(event)

	def ciz(self):
		if self.secilen == None:
			for i in [0,1] :
				otest_list[i].draw()
		elif self.secilen == 0:
			self.snake.dongu()
			if self.snake.sonuc:
				self.sonuc = True
		elif self.secilen == 1:
			self.pong.dongu()

otest = Otest()


###   FİNAL   OYUNU   SINIFI

background = pygame.image.load("Level_bg.png")
upground = pygame.image.load("Level_way.png")

	#  Music/Sounds
	#music = pygame.mixer.music.load(os.path.join("Assets/Audio", "music.ogg"))
	#pop_sound = pygame.mixer.Sound(os.path.join("Assets/Audio", "pop.ogg"))
	#pygame.mixer.music.play(-1)

hero_images = [ [],[],[],[],[],[] ]

virus_images = []
horse_images = []
worm_images = [ [],[],pygame.image.load(f"worm_hurt-1.png.png"),[] ]

def indirmeler():
	for i in range(1,11):
		hero_images[1].append(pygame.transform.scale(pygame.image.load(f"Knight_run-{i}.png.png"),(120,80)))
		hero_images[5].append(pygame.transform.scale(pygame.image.load(f"Knight_death-{i}.png.png"),(120,80)))
		if i < 4:
			hero_images[2].append(pygame.transform.scale(pygame.image.load(f"Knight_jump-{i}.png.png"),(120,80)))
		elif i < 8:
			hero_images[3].append(pygame.transform.scale(pygame.image.load(f"Knight_jump-{i}.png.png"),(120,80)))
		if i < 10:
			hero_images[4].append(pygame.transform.scale(pygame.image.load(f"Knight_attack-{i}.png.png"),(120,80)))
			if i < 9:
				hero_images[0].append(pygame.transform.scale(pygame.image.load(f"Knight_idle-{i}.png.png"),(120,80)))
				if i < 6 :
					virus_images.append(pygame.transform.scale(pygame.image.load(f"Virus-{i}.png.png"),(64,64)))
					horse_images.append(pygame.image.load(f"horse_-{i}.png.png"))
					if i < 5:
						worm_images[0].append(pygame.image.load(f"worm_run-{i}.png.png"))
						if i < 4:
							worm_images[1].append(pygame.image.load(f"worm_attack-{i}.png.png"))
							worm_images[3].append(pygame.image.load(f"worm_death-{i}.png.png"))

class Hero:
	def __init__(self):
		# Walk
		self.x = 600-42
		self.y = 300-20
		self.velx = 10
		self.vely = 6
		self.vely_2 = 6
		self.vely_3 = 0
		self.idle_left = True
		self.idleIndex = 0

		self.face_left = False
		self.face_right = False
		self.face_up = False
		self.face_down = False

		self.stepIndex_x = 0
		self.stepIndex_up = 0
		self.stepIndex_down = 0
		self.ways = [100,300,500]
		self.current_way = self.ways[1]
		self.yol_gecildi = False
		self.dusebilir = False
		# Jump
		self.jump = 0
		# Sword
		self.attackable = False
		self.dmg_width = pygame.Rect(self.x+(int(not(self.idle_left))*60), self.y,60,80)
		self.attackIndex = 0
		self.cool_down_count = 0
		# Health
		self.hw = 31
		self.hh = 37
		self.hitbox = (self.x+42, self.y+40, self.hw, self.hh)
		self.health = 30
		self.lives = 3
		self.hurt = False
		self.hurtIndex = 0
		self.alive = True
		self.deathIndex = 0

	def yonu(self):
		if self.idle_left:
			return -1
		else:
			return 1
	def move_hero(self, userInput):
		if not self.attackable:
			if userInput[pygame.K_d]:
				if userInput[pygame.K_a]:
					self.face_right = False
					self.face_left = False
					self.stepIndex_x = 0
				elif self.x <= 615:
					self.x += self.velx
					self.face_right = True
					self.face_left = False
					self.idle_left = False
				else:
					self.face_right = False
					self.face_left = False
			elif userInput[pygame.K_a] and self.x >= -40:
				self.x -= self.velx
				self.face_right = False
				self.face_left = True
				self.idle_left = True
			else:
				self.face_right = False
				self.face_left = False
				self.stepIndex_x = 0

	def draw(self, win):
		self.hitbox = (self.x+42 , self.y+30, 31, 47)
		if self.stepIndex_x >= 10:
			self.stepIndex_x = 0
		if self.stepIndex_up >= 6:
			self.stepIndex_up = 0
		if self.stepIndex_down >= 3.5:
			self.stepIndex_down = 0
		if self.idleIndex >= 8:
			self.idleIndex = 0
		if self.alive:
			pygame.draw.rect(win, (255, 0, 0), (self.x+45 , self.y+15, 30, 10))
			pygame.draw.rect(win, (0, 255, 0), (self.x+45, self.y+15, self.health, 10))
			if self.hurt:
				win.blit(pygame.transform.flip(hero_images[5][self.hurtIndex//2],self.idle_left,False),(self.x,self.y))
				if not(game.kazandi):
					self.hurtIndex += 1
					if self.hurtIndex >=4:
						self.hurt = False
			elif self.face_left or self.face_right:
				if self.attackable:
					win.blit(pygame.transform.flip(hero_images[4][self.attackIndex],self.idle_left,False),(self.x,self.y))
					if not(game.kazandi):
						self.attackIndex += 1
				elif self.face_up:
					win.blit(pygame.transform.flip(hero_images[2][self.stepIndex_up//2],self.idle_left,False), (self.x,self.y))
					if not(game.kazandi):
						self.stepIndex_up += 1
				elif self.face_down:
					if self.yol_gecildi and self.y >= self.current_way-20:
						self.yol_gecildi = False
						self.y = self.current_way -20
						self.jump = 0
						self.vely = 6
						self.vely_2 = 6
						game.player_jumping = False
						self.face_down = False
						win.blit(pygame.transform.flip(hero_images[1][int(self.stepIndex_x)],self.idle_left,False), (self.x, self.y))
						self.stepIndex_x += 0.5
					else:
						win.blit(pygame.transform.flip(hero_images[3][self.stepIndex_down//2],self.idle_left,False), (self.x,self.y))
						if not(game.kazandi):
							self.stepIndex_down += 1
							for i in self.ways:
								if self.current_way > self.ways[0] and (self.y == i-36 or (self.y == i-20 or self.y == i-30)):
									self.yol_gecildi = True
									self.current_way = i
									self.y = self.current_way -20
				else:
					win.blit(pygame.transform.flip(hero_images[1][int(self.stepIndex_x)],self.idle_left,False), (self.x, self.y))
					if not(game.kazandi):
						self.stepIndex_x += 0.5
			else:
				if self.attackable:
					win.blit(pygame.transform.flip(hero_images[4][int(self.attackIndex)],self.idle_left,False), (self.x,self.y))
					if not(game.kazandi):
						self.attackIndex += 1
				elif self.face_up:
					win.blit(pygame.transform.flip(hero_images[2][self.stepIndex_up//2],self.idle_left,False), (self.x,self.y))
					if not(game.kazandi):
						self.stepIndex_up += 1
				elif self.face_down:
					if self.yol_gecildi and self.y >= self.current_way-20:
						self.yol_gecildi = False
						self.y = self.current_way -20
						self.jump = 0
						self.vely = 6
						self.vely_2 = 6
						game.player_jumping = False
						self.face_down = False
						win.blit(pygame.transform.flip(hero_images[0][int(self.idleIndex)//2],self.idle_left,False),(self.x,self.y))
						self.idleIndex += 0.5
					else:
						win.blit(pygame.transform.flip(hero_images[3][self.stepIndex_down//2],self.idle_left,False), (self.x,self.y))
						if not(game.kazandi):
							self.stepIndex_down += 1
							for i in self.ways:
								if self.current_way > self.ways[0] and (self.y == i-36 or (self.y == i-20 or self.y == i-30)):
									self.yol_gecildi = True
									self.current_way = i
									self.y = self.current_way -20
				else:
					win.blit(pygame.transform.flip(hero_images[0][int(self.idleIndex)//2],self.idle_left,False),(self.x,self.y))
					if not(game.kazandi):
						self.idleIndex += 0.5
		elif not(game.kazandi):
			win.blit(pygame.transform.flip(hero_images[5][(self.deathIndex//2)],self.idle_left,False),(self.x,self.y))
			if self.deathIndex <= 18:
				self.deathIndex += 1
			if self.lives == 3 and self.deathIndex >= 19:
				self.__init__()
				self.lives = 2
			elif self.lives == 2 and self.deathIndex >= 19:
				self.__init__()
				self.lives = 1
	def jumpped(self):
		if self.jump < 2 and not(self.attackable or self.dusebilir):
			self.idleIndex = 0
			self.stepIndex_x = 0
			game.player_jumping = True
			self.jump += 1
			self.face_up = True
			self.face_down = False

	def jump_motion(self):
		if self.jump:
			if self.jump == 1:
				self.y -= self.vely * 6
				self.vely -= 1
				if self.vely < -6:
					self.jump = 0
					self.vely = 6
					self.face_up = False
					self.face_down = False
					game.player_jumping = False
				elif self.vely < 1:
					self.face_up = False
					self.face_down = True
			if self.jump == 2:
				self.y -= self.vely_2 * 6
				self.vely_2 -= 1
				if self.vely_2 < -6 :
					self.jump = 3
					self.vely_2 = 6
					if self.vely > 0:
						self.vely += 1
					self.vely = ((abs(self.vely)) * -1)
				elif self.vely_2 < 1:
					self.face_up = False
					self.face_down = True
			if self.jump == 3:
				self.y -= self.vely * 6
				self.vely -= 1
				if self.vely < -6:
					self.jump = 0
					self.vely = 6
					game.player_jumping = False
					self.face_up = False
					self.face_down = False
				elif self.vely < 1:
					self.face_up = False
					self.face_down = True

	def fall(self):
		if self.y == self.current_way-20 and not (self.attackable or self.current_way == self.ways[2]):
			self.dusebilir = True
			self.face_up = False
			self.face_down = True

	def fall_motion(self):
		if self.dusebilir:
			self.y -= self.vely_3 * 6
			self.vely_3 -= 1
			if self.vely_3 < -7:
				self.vely_3 = 0
				self.face_up = False
				self.face_down = False
				self.dusebilir = False
				self.current_way = self.current_way + 200
				self.y = self.current_way-20

	def hasar_al(self,hasar):
		self.health -= hasar
		if self.health <= 0:
			self.alive = False
		else:
			self.hurt = True

	def mousedown(self):
		if not((self.face_up or self.face_down) or self.attackable):
			self.attackable = True
			self.attackIndex = 0

	def attack(self):
#pop_sound.play()
		if self.attackIndex >= 9 and self.attackable:
			self.dmg_width = pygame.Rect(self.x+(int(not(self.idle_left))*60), self.y,60,80)
			self.hit()
			self.attackIndex = 0
			self.attackable = False
			self.cool_down_count = 1

	def hit(self):
		for enemy in game.enemies:
			if enemy.current_way == self.current_way:
				enemy.hitbox_guncelle()
				if self.dmg_width.collidepoint(enemy.hitbox[0], enemy.hitbox[1]) or \
				self.dmg_width.collidepoint(enemy.hitbox[0], enemy.hitbox[1] + enemy.hh) or \
				self.dmg_width.collidepoint(enemy.hitbox[0] + enemy.hw, enemy.hitbox[1]) or \
				self.dmg_width.collidepoint(enemy.hitbox[0] + enemy.hw, enemy.hitbox[1] + enemy.hh):
					enemy.hasar_al()

class virus:
	def __init__(self,speed):
		self.current_way = game.player.ways[0]
		self.hw = 45 #hitbox width (uzunluk)
		self.hh = 46 #hitbox height (yükseklik)
		self.x = -self.hw -9
		self.y = (self.current_way+2) - (choice([1,-1])*randint(0,12))-9
		self.hitbox = pygame.Rect(self.x+9,self.y+9,self.hw,self.hh)
		self.alive = True
		self.sd = False
		self.patlaIndex = 0
		self.hasar_ver = False
		self.health = 30
		self.speed = speed
		self.hero_dmg = 30
		self.kule_dmg = 15
		self.ulasildi = False
		self.ekranda = True
		self.hurt = False
		self.hurtIndex = 0
		
	def hitbox_guncelle(self):
		self.hitbox = pygame.Rect(self.x+9,self.y+9,self.hw,self.hh)

	def draw(self, win):
		if self.alive:
			if self.hurt:
				if self.hurtIndex < 3:
					win.blit(virus_images[4], (self.x, self.y))
					if game.player.alive and not(game.kazandi):
						self.hurtIndex +=1
						self.x += self.speed
				else:
					if self.health <= 0:
						self.alive = False
					else:
						self.hurtIndex = 0
						self.hurt = False
			if not self.hurt:
				win.blit(virus_images[0], (self.x, self.y))
				if game.player.alive and not(game.kazandi):
					self.hit(False,True)
					self.x += self.speed
					if self.x+9+self.hw >= 710:
						self.reach_tower()
			if game.player.alive and not(game.kazandi):
				self.can_goster()
		else:
			win.blit(virus_images[(self.patlaIndex//3)], (self.x, self.y))
			if game.player.alive and not(game.kazandi):
				if self.patlaIndex >= 3:
					self.hit(True)
				if self.patlaIndex >= 9:
					self.ekranda = False
					if self.ulasildi:
						game.tower_health -= self.kule_dmg
					if self.hasar_ver:
						game.player.hasar_al(self.hero_dmg)
				else:
					self.patlaIndex += 1
			else:
				self.hasar_ver = False
	def can_goster(self):
		if self.health > 0 and self.alive:
			pygame.draw.rect(g.pencere, (255, 0, 0), (self.x + 10, self.y, 30, 10))
			pygame.draw.rect(g.pencere, (0, 255, 0), (self.x + 10, self.y, self.health, 10))

	def hasar_al(self,hasar=10):
		self.health -= hasar
		self.hurt = True

	def hit(self,hasar_ver=False, kill=False):
		self.hitbox_guncelle()
		if self.hitbox.collidepoint(game.player.hitbox[0], game.player.hitbox[1]) or \
		self.hitbox.collidepoint(game.player.hitbox[0], game.player.hitbox[1] + game.player.hh) or \
		self.hitbox.collidepoint(game.player.hitbox[0]+game.player.hw, game.player.hitbox[1]) or \
		self.hitbox.collidepoint(game.player.hitbox[0]+game.player.hw,game.player.hitbox[1] + game.player.hh):
			self.alive = False
			if hasar_ver:
				self.hasar_ver = True
			if kill:
				self.sd = True

	def reach_tower(self):
		self.ulasildi = True
		self.alive = False
		self.sd = True

class horse :
	def __init__(self,speed):
		self.x = -47
		self.current_way = game.player.ways[1]
		self.y = (self.current_way+2) - (choice([1,-1])*randint(0,12))
		self.hw = 47 #hitbox width (uzunluk)
		self.hh = 46 #hitbox height (yükseklik)
		self.hitbox = (self.x,self.y,self.hw,self.hh)
		self.stepIndex = 0
		self.health = 20
		self.sd = False
		self.speed = speed
		self.kule_dmg = 31
		self.ekranda = True
		self.hurt = False
		self.hurtIndex = 0

	def hitbox_guncelle(self):
		self.hitbox = (self.x,self.y,self.hw,self.hh)

	def draw(self, win):
		if self.health >= 0:
			pygame.draw.rect(win, (255, 0, 0), (self.x + 10, self.y, 20, 10))
			pygame.draw.rect(win, (0, 255, 0), (self.x + 10, self.y, self.health, 10))
		else:
			self.ekranda = False
		win.blit(horse_images[self.stepIndex // 3], (self.x, self.y))
		if game.player.alive and not(game.kazandi):
			if self.hurt:
				win.blit(horse_images[4], (self.x, self.y))
				self.hurtIndex +=1
				self.x += self.speed
				if self.hurtIndex >= 3 :
					if self.health <= 0:
						self.ekranda = False 
					else:
						self.hurtIndex = 0
						self.hurt = False
			else:
				self.stepIndex += 1
				self.x += self.speed
				if self.stepIndex >= 12 :
					self.stepIndex = 0
				if self.x >= 710:
					self.reach_tower()

	def hasar_al(self):
		self.health -= 10
		self.hurt = True

	def reach_tower(self):
		game.tower_health -= self.kule_dmg
		self.ekranda = False

class worm:
	def __init__(self,speed,lives=2, x = -56 -4, y = 'belirsiz'):
		self.current_way = game.player.ways[2]
		self.hw = 56 #hitbox width (uzunluk)
		self.hh = 56 #hitbox height (yükseklik)
		self.x = x
		if y == 'belirsiz':
			self.y = (self.current_way+2) - (choice([1,-1])*randint(0,12))-9
		else:
			self.y = y
		self.hitbox = pygame.Rect(self.x+4,self.y,self.hw,self.hh)
		self.alive = True
		self.lives = lives
		self.sd = False
		self.stepIndex = 0
		self.deathIndex = 0
		self.attackIndex = 0
		self.cooldown = 0
		self.health = 30
		self.hasar_ver = False
		self.saldir = False
		self.speed = speed
		self.hero_dmg = 10
		self.kule_dmg = 5
		self.ulasildi = False
		self.ekranda = True
		self.hurt = False
		self.hurtIndex = 0
		
	def hitbox_guncelle(self):
		self.hitbox = pygame.Rect(self.x+4,self.y,self.hw,self.hh)

	def draw(self, win):
		if self.alive:
			if self.saldir:
				if self.attackIndex < 9:
					win.blit(worm_images[1][self.attackIndex//3], (self.x, self.y))
					if game.player.alive and not(game.kazandi):
						self.attackIndex += 1
						if self.attackIndex >= 6:
							self.hit(True)
					else:
						self.attackIndex = 0
						self.saldir = False
				elif game.player.alive and not(game.kazandi):
					win.blit(worm_images[1][0], (self.x, self.y))
					if self.ulasildi:
						if self.cooldown >= 9:
							self.cooldown = 0
							self.attackIndex = 0
						else:
							if self.cooldown == 0:
								game.tower_health -= self.kule_dmg
							self.cooldown += 1
					else:
						if self.hasar_ver:
							game.player.hasar_al(self.hero_dmg)
							self.hasar_ver = False
						self.attackIndex = 0
						self.saldir = False
						self.hit()
			elif self.hurt:
				if self.hurtIndex < 3:
					win.blit(worm_images[2], (self.x, self.y))
					if game.player.alive and not(game.kazandi):
						self.hurtIndex +=1
				else:
					if self.health <= 0:
						self.lives -= 1
						self.alive = False
					else:
						self.hurtIndex = 0
						self.hurt = False
			if not (self.hurt or self.saldir):
				win.blit(worm_images[0][self.stepIndex//3], (self.x, self.y))
				if game.player.alive and not(game.kazandi):
					self.hit()
					self.stepIndex += 1
					if self.stepIndex >= 12:
						self.x += self.speed*2
						self.stepIndex = 0
					if self.stepIndex == 9:
						self.x += self.speed*2
					if self.x+self.hw >= 710:
						self.reach_tower()
			if game.player.alive and not(game.kazandi):
				self.can_goster()
		else:
			win.blit(worm_images[3][(self.deathIndex//3)], (self.x, self.y))
			if game.player.alive and not(game.kazandi):
				if self.deathIndex >= 8:
					self.ekranda = False
					if self.lives > 0:
						self.__init__(self.speed,self.lives,self.x,self.y)
				else:
					self.deathIndex += 1
			else:
				self.hasar_ver = False
	def can_goster(self):
		if self.health > 0 and self.alive:
			pygame.draw.rect(g.pencere, (255, 0, 0), (self.x + 18, self.y-12, 30, 10))
			pygame.draw.rect(g.pencere, (0, 255, 0), (self.x + 18, self.y-12, self.health, 10))

	def hasar_al(self,hasar=10):
		self.health -= hasar
		self.hurt = True

	def hit(self,hasar_ver= False):
		self.hitbox_guncelle()
		if self.hitbox.collidepoint(game.player.hitbox[0], game.player.hitbox[1]) or \
		self.hitbox.collidepoint(game.player.hitbox[0], game.player.hitbox[1] + game.player.hh) or \
		self.hitbox.collidepoint(game.player.hitbox[0]+game.player.hw, game.player.hitbox[1]) or \
		self.hitbox.collidepoint(game.player.hitbox[0]+game.player.hw,game.player.hitbox[1] + game.player.hh):
			self.saldir = True
			if hasar_ver:
				self.hasar_ver = True

	def reach_tower(self):
		self.ulasildi = True
		self.saldir = True


font_1 = pygame.font.SysFont('Helvetica', 18)
font_2 = pygame.font.SysFont('Helvetica', 32)
# Draw Game
def sirala(obje):
	return obje.y

def draw_game():
	global font_1, font_2, sirala
	g.pencere.fill((0,0,0))
	g.pencere.blit(background, (0, 0))
	if len(game.enemies) > 0:
		game.enemies.sort(key = sirala)
	for enemy in game.enemies:
		enemy.draw(g.pencere)
	game.player.draw(g.pencere)

	pygame.draw.rect(g.pencere, (0,0,0),(710,0,90,600))
	pygame.draw.rect(g.pencere, (255,255,255),(725,70,60,int(game.tower_health*4)))
	pygame.draw.rect(g.pencere, (255,255,255),(725,70,60,400),2)
	th_text = font_1.render('İlerleme:', True, (255, 255, 255))
	yuzde_text = font_1.render('% '+str(game.tower_health), True, (255, 255, 255))

	# Player Health
	if (game.player.deathIndex >= 19 and game.player.lives <= 1) or game.tower_health <= 0:
		game.player.lives = 0
		if game.tower_health > 0 :
			text = font_2.render('Canın bitti! baslamak için "R"ye bas', True, (255, 255, 255),(0,0,0))
		else :
			text = font_2.render('Zaman aşımı! baslamak için "R"ye bas', True, (255, 255, 255),(0,0,0))
		game.player.alive = False
		textRect = text.get_rect()
		textRect.center = (800 // 2, 600 // 2)
		g.pencere.blit(text, textRect)
		if pygame.key.get_pressed()[pygame.K_r]:
			game.__init__()
	elif game.tower_health >= 100:
		text = font_2.render('Kazandın! geçmek için "R"ye bas', True, (255, 255, 255),(0,0,0))
		game.kazandi = True
		textRect = text.get_rect()
		textRect.center = (800 // 2, 600 // 2)
		g.pencere.blit(text, textRect)
		if pygame.key.get_pressed()[pygame.K_r]:
			game.gecildi = True

	text_1 = font_1.render('Canın: ' + str(game.player.lives), True, (255, 255, 255))
	text_2 = font_1.render('ölü: '+ str(game.kills), True, (255, 255, 255))

	g.pencere.blit(text_1,(715,20))
	g.pencere.blit(text_2,(715,42))
	g.pencere.blit(th_text,(715,480))
	g.pencere.blit(yuzde_text,(715,502))
	g.pencere.blit(upground, (0, 0))

class Main():
	def __init__(self):
		indirmeler()
		self.dongu = 0
		self.player = Hero()
		self.player_jumping = False
		self.enemies = []
		self.enemyIndex = 0
		self.kills = 0
		self.tower_health = 5
		self.clock = pygame.time.Clock()
		self.kazandi = False
		self.gecildi = False

	def random_enemy(self):
		if self.dongu >= self.enemyIndex:
			self.enemies.append(choice([ virus(randint(randint(2,3),4)), horse(randint(3,5)), worm(randint(randint(1,2),3)) ]))
			self.enemyIndex = randint(randint(10,40),randint(120,180))
			self.dongu = 0

	def mouse_down(self):
			if (self.player.alive and not(self.kazandi)):
				self.player.mousedown()
	def key_down(self,event):
			if (self.player.alive and not(self.kazandi)):
				if event.key == pygame.K_w:
					self.player.jumpped()
				if event.key == pygame.K_s:
					self.player.fall()

	def main(self):
		if self.player.alive and not(self.kazandi):
			self.userInput = pygame.key.get_pressed()

			# saldırı
			self.player.attack()

			# hareket
			self.player.move_hero(self.userInput)
			self.player.jump_motion()
			self.player.fall_motion()


			# dusmanlar
			self.random_enemy()
			for enemy in self.enemies:
				if not enemy.ekranda:
					if not enemy.sd:
						self.tower_health += 1
						self.kills += 1
					self.enemies.remove(enemy)

		self.dongu += 1
		# Draw Game in Window
		draw_game()
		self.clock.tick(20)

game = Main()


###   1.BÖLÜM   GÜNLÜK   GİFİ
class Gunluk_gif(pygame.sprite.Sprite) :
	def __init__ (self) :
		super().__init__()
		self.sayi=1
# 	gif için görselleri indirme ve liste oluşturma
		self.sprites = []
		self.mevcut_sprite = 0

	def guncelle(self) :
		if self.sayi <= 18 :
			self.sprites.append(pygame.image.load(f'Diary-{self.sayi}.png.png'))
			self.sayi += 1
		self.image = self.sprites[int(self.mevcut_sprite)]
		self.mevcut_sprite += 0.3
		if self.mevcut_sprite >= len(self.sprites) :
			self.mevcut_sprite = 0
		self.image = self.sprites[int(self.mevcut_sprite)]
		g.pencere.blit(self.image,(0,-50))

# gunluk gifini kullanmak için nesne
gunluk = Gunluk_gif()





##############      OYUNU YÜRÜTME  SINIFI     ###############
class Game():
	def __init__(self):
		self.running ,self.playing ,self.oyunda = True,True,False
		self.SCREEN = "menu"
		self.kullanici_adi = ''
		self.muzik = 1
		self.clock = pygame.time.Clock()
		self.pencere = pygame.display.set_mode((800,600) , pygame.HWSURFACE) # 800 ,600 boyutunda video penceresi aç
		self.siyah,self.beyaz = (0,0,0),(255,255,255) # rgb renklerine değişken atandı
		self.mouseX,self.mouseY = None,None

	def check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running, self.playing = False,False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if self.SCREEN == "menu":
					oyna_butonu.checkForInput((self.x,self.y))
					ozelt_butonu.checkForInput((self.x,self.y))
					ayarlar_butonu.checkForInput((self.x,self.y))
					referanslar_butonu.checkForInput((self.x,self.y))
				else:
					if self.SCREEN != None :
						geri_butonu.checkForInput((self.x,self.y))
					if l.mevcut_level == "kullanici_adi_al" and self.oyunda == True:
						ad_al_butonu.mousedown_kontrol(event,(self.x,self.y))
					if self.SCREEN == "ayarlar" :
						ad_degis_butonu.mousedown_kontrol(event,(self.x,self.y))
						if self.muzik == 1 :
							sesacik_butonu.checkForInput((self.x,self.y))
						elif self.muzik == 0 :
							seskapali_butonu.checkForInput((self.x,self.y))
						sifirla_butonu.checkForInput((self.x,self.y))
					if self.SCREEN == "referanslar" :
						for i in range (0,6) :
							link_list[i].checkForInput((self.x,self.y))
					if self.oyunda == True :
						if l.dialog == True :
							dialog_butonu.checkForInput((self.x,self.y))
						if l.mevcut_level == 1 and self.oyunda == True and l.kisim == 4:
							masaustu_butonu.checkForInput((self.x,self.y))
						elif l.mevcut_level == 2 and l.kisim == 2 :
							soru_1.mousedown_kontrol((self.x,self.y))
							soru_2.mousedown_kontrol((self.x,self.y))
							soru_3.mousedown_kontrol((self.x,self.y))
						elif l.mevcut_level == 3 and l.kisim == 2 :
							soru_4.mousedown_kontrol((self.x,self.y))
							soru_5.mousedown_kontrol((self.x,self.y))
							soru_6.mousedown_kontrol((self.x,self.y))
						elif l.mevcut_level == 4 :
							if l.kisim == 2:
								soru_7.mousedown_kontrol((self.x,self.y))
								soru_8.mousedown_kontrol((self.x,self.y))
								soru_9.mousedown_kontrol((self.x,self.y))
							elif l.kisim == 'hack_2':
								hack_2.kontrol((self.x,self.y))
						elif l.mevcut_level == 5 and l.kisim == 2:
							ok_butonu.checkForInput((self.x,self.y))
						elif l.mevcut_level == 6 and l.kisim == 2:
							binary_1.mousedown_kontrol((self.x,self.y))
							binary_2.mousedown_kontrol((self.x,self.y))
							binary_3.mousedown_kontrol((self.x,self.y))
						elif l.mevcut_level == 7 and l.kisim == 2 :
							soru_10.mousedown_kontrol((self.x,self.y))
							soru_11.mousedown_kontrol((self.x,self.y))
							soru_12.mousedown_kontrol((self.x,self.y))
						elif l.mevcut_level == 8 and l.kisim == 2 :
							soru_13.mousedown_kontrol((self.x,self.y))
							soru_14.mousedown_kontrol((self.x,self.y))
							soru_15.mousedown_kontrol((self.x,self.y))
						elif l.mevcut_level == 9 and l.kisim == 2 :
							otest.girdi_mouse()
						elif l.mevcut_level == 10:
							if l.kisim == 'ara2':
								fgame_buton.checkForInput((self.x,self.y))
							if l.kisim == 2:
								game.mouse_down()
						elif l.mevcut_level == 'level_sec' :
							levelsec.girdi()
			if event.type == pygame.KEYDOWN :
				if l.mevcut_level == "kullanici_adi_al" and self.oyunda == True:
					ad_al_butonu.key_kontrol(event)
				if self.SCREEN == "ayarlar" :
					ad_degis_butonu.key_kontrol(event)
				if l.mevcut_level == 2 :
					if l.kisim == 2 :
						soru_1.key_kontrol(event)
						soru_2.key_kontrol(event)
						soru_3.key_kontrol(event)
					if l.kisim == 'hack_1' :
						player.kontrol(event)
				elif l.mevcut_level == 3 and l.kisim == 2 :
					soru_4.key_kontrol(event)
					soru_5.key_kontrol(event)
					soru_6.key_kontrol(event)
				elif l.mevcut_level == 4 and l.kisim == 2 :
					soru_7.key_kontrol(event)
					soru_8.key_kontrol(event)
					soru_9.key_kontrol(event)
				elif l.mevcut_level == 6 and l.kisim == 2:
					binary_1.key_kontrol(event)
					binary_2.key_kontrol(event)
					binary_3.key_kontrol(event)
				elif l.mevcut_level == 7 and l.kisim == 2 :
					soru_10.key_kontrol(event)
					soru_11.key_kontrol(event)
					soru_12.key_kontrol(event)
				elif l.mevcut_level == 8 and l.kisim == 2 :
					soru_13.key_kontrol(event)
					soru_14.key_kontrol(event)
					soru_15.key_kontrol(event)
				elif l.mevcut_level == 9 and l.kisim == 2 :
					otest.girdi_key(event)
				elif l.mevcut_level == 10 and l.kisim == 2 :
					game.key_down(event)

	def oyun_dongusu(self):
		while self.playing :
			self.x,self.y=pygame.mouse.get_pos()
			self.check_events()
			if self.oyunda == False :
				if self.SCREEN == 'ayarlar' or self.SCREEN == None :
					if sifirla_butonu.dongu == True :
						db.resetle()
					if self.SCREEN == 'ayarlar' :
						if self.muzik == 1 and sesacik_butonu.dongu == True:
							self.muzik = 0
							sesacik_butonu.dongu = False
							db.update('mz')
						elif self.muzik == 0 and seskapali_butonu.dongu == True:
							self.muzik = 1
							seskapali_butonu.dongu = False
							db.update('mz')
				if oyna_butonu.dongu == True:
					self.SCREEN = "mevcut_level"
					oyna_butonu.dongu=False
				if ozelt_butonu.dongu == True:
					self.SCREEN = "ozelt"
					ozelt_butonu.dongu=False
				if ayarlar_butonu.dongu == True:
					self.SCREEN = "ayarlar"
					ayarlar_butonu.dongu=False
				if referanslar_butonu.dongu == True:
					self.SCREEN = "referanslar"
					referanslar_butonu.dongu=False
				if geri_butonu.dongu == True:
					self.SCREEN = "menu"
					geri_butonu.dongu=False
			elif self.SCREEN == "mevcut_level":
				l.play_mevcut_level()
				if geri_butonu.dongu == True:
					self.SCREEN = "menu"
					geri_butonu.dongu=False


			self.ekrani_boya()
			pygame.display.update()

	def ekrani_boya(self):
		self.oyunda_mi()
		if self.SCREEN == "menu" :
			self.pencere.blit(menuEkrani_image,(0,0))
			text_blit("Oynadığınız için teşekkürler !","ortala",115,12)
			text_blit("Bu oyundaki yazılım bilgisi","ortala",216,12)
			text_blit("Python dili esaslıdır","ortala",230,12)
			text_blit("Justhink","ortala",400,30)
			oyna_butonu.changeColor((self.x,self.y))
			ozelt_butonu.changeColor((self.x,self.y))
			ayarlar_butonu.changeColor((self.x,self.y))
			referanslar_butonu.changeColor((self.x,self.y))
		else:
			if self.oyunda == False:
				if self.SCREEN == "ozelt":
					self.pencere.blit(ozelT_image,(0,0))
					text_blit('Ailelerimize,','ortala',188,32,"beyaz")
					text_blit('Oynayanlara,','ortala',224,32,"beyaz")
					text_blit('Kaan olarak Yağız Burak\'a,','ortala',260,32,"beyaz")
					text_blit('Yağız olarak Kaan Tekmen\'e,','ortala',296,32,"beyaz")
					text_blit('Engin Cüce Hocamıza,','ortala',332,32,"beyaz")
					text_blit('Referanslara','ortala',368,32,"beyaz")
					text_blit('TEŞEKKÜR EDERİZ.','ortala',404,32,"beyaz")
					
				elif self.SCREEN == "ayarlar":
					self.pencere.blit(ayarlar_image,(0,0))
					text_blit("Tıklayıp, adınızda değişiklik yapabilirsiniz","ortala",450,24,"beyaz")
					text_blit("Müzik Açma/Kapama","ortala",257,24,"beyaz")
					text_blit("İlerleme SIFIRLAMA (çift basın)","ortala",132,24,"beyaz")
					ad_degis_butonu.ciz()
					sifirla_butonu.changeColor((self.x,self.y))
					if self.muzik == 1 :
						sesacik_butonu.changeColor((self.x,self.y))
					elif self.muzik == 0 :
						seskapali_butonu.changeColor((self.x,self.y))
				elif self.SCREEN == "referanslar":
					self.pencere.blit(referanslar_image,(0,0))
					text_blit('Python diliyle yazılmıştır. (pygame,os,sqlite3,random,webbrowser kütüphaneleri kullanıldı)',40,98,18,"beyaz")
					text_blit('Kullanılan Görseller',40,164,18,"beyaz")
					text_blit('Giriş bölümünde kullanılan günlük gifi :',60,186,18,"beyaz")
					text_blit('Giriş bölümünde kullanılan Laptop görseli :',60,230,18,"beyaz")
					text_blit('5. bölümde kullanılan System hacked görseli :',60,274,18,"beyaz")
					text_blit('Final bölümünde kullanılan Şövalye animasyonları :',60,318,18,"beyaz")
					text_blit('Final bölümünde kullanılan Virüs görselleri :',60,362,18,"beyaz")
					
					text_blit('Kullanılan Fontlar',40,450,18,"beyaz")
					text_blit('Helvetica (Oyunun çoğu yazısının fontu)',60,472,18,"beyaz")
					text_blit('Porky\'s (Menü Başlıklarının fontu)',60,494,18,"beyaz")
					text_blit('Maximum Security (Level seçme ekranındaki yazıların fontu)',60,516,18,"beyaz")
					text_blit('(Linkleri çalıştırmak için üstüne çift tıklayınız)','ortala',576,14,"beyaz")
					for i in range (0,6) :
						link_list[i].draw()
			else:
				if l.mevcut_level == "kullanici_adi_al"and self.SCREEN == "mevcut_level":
					self.pencere.fill(self.siyah)
					ad_al_butonu.ciz()
					text_blit("GİRİŞ BÖLÜMÜ","ortala",168,24,"beyaz")
					text_blit("Adınızı giriniz (en fazla 20 karakter olarak)","ortala",202,24,"beyaz")
					text_blit("Her zaman ayarlardan değiştirilebilir","ortala",236,24,"beyaz")
					text_blit("Devam etmek için Enter'a basın","ortala",340,18,"beyaz")

				elif l.mevcut_level == 2 and l.kisim == 2 :
					soru_1.ciz()
					soru_2.ciz()
					soru_3.ciz()
				elif l.mevcut_level == 3 and l.kisim == 2 :
					soru_4.ciz()
					soru_5.ciz()
					soru_6.ciz()
				elif l.mevcut_level == 4 and l.kisim == 2:
					soru_7.ciz()
					soru_8.ciz()
					soru_9.ciz()
				elif l.mevcut_level == 6 and l.kisim == 2:
					binary_1.ciz()
					binary_2.ciz()
					binary_3.ciz()
				elif l.mevcut_level == 7 and l.kisim == 2 :
					soru_10.ciz()
					soru_11.ciz()
					soru_12.ciz()
				elif l.mevcut_level == 8 and l.kisim == 2 :
					soru_13.ciz()
					soru_14.ciz()
					soru_15.ciz()
			if self.SCREEN != None :
				geri_butonu.changeColor((self.x,self.y))

	def oyunda_mi(self):
		if self.SCREEN == "menu" or self.SCREEN == "ozelt" or self.SCREEN == "ayarlar" or self.SCREEN == "referanslar" or self.SCREEN == None :
			self.oyunda=False
		else :
			self.oyunda=True
class Game_level():
	def __init__(self):
		self.mevcut_level = "kullanici_adi_al"
		self.level_gecildi = False
		self.tamamlanan = 0

		self.dialog = True
		self.kisim = 1
		self.giris = 1
		self.bolumekrani_dongu = 0
	def play_mevcut_level(self):
		if type(self.mevcut_level) == int:
			if self.mevcut_level == 1:
				self.intro()
			elif self.mevcut_level == 2:
				self.level_2()
			elif self.mevcut_level == 3:
				self.level_3()
			elif self.mevcut_level == 4:
				self.level_4()
			elif self.mevcut_level == 5:
				self.level_5()
			elif self.mevcut_level == 6:
				self.level_6()
			elif self.mevcut_level == 7:
				self.level_7()
			elif self.mevcut_level == 8:
				self.level_8()
			elif self.mevcut_level == 9:
				self.level_9()
			elif self.mevcut_level == 10:
				self.final()
			if self.level_gecildi == True:
				self.tamamlanan = self.mevcut_level
				self.mevcut_level+=1
				self.kisim = 1
				self.giris = 1
				self.level_gecildi = False
				db.update('tl')
		
		elif self.mevcut_level == "kullanici_adi_al":
			if self.tamamlanan == 0 :
				self.kullanici_adi_al()
			else :
				self.mevcut_level = self.tamamlanan
	
		elif self.mevcut_level == "level_sec" :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				levelsec.boya()
				if levelsec.cikti != None :
					ekran_gecisi_1.dongu = True
					if levelsec.cikti <= 1 :
						self.mevcut_level = levelsec.cikti + 1
					elif levelsec.cikti >= 2 :
						self.mevcut_level = levelsec.cikti
						if levelsec.cikti == 2 :
							self.kisim = 'hack_1'
						elif levelsec.cikti >= 5 :
							self.mevcut_level = levelsec.cikti - 1
							if levelsec.cikti == 5 :
								self.kisim = 'hack_2'

	def kullanici_adi_al(self):
		self.mevcut_level = "kullanici_adi_al"
		if ad_al_butonu.dongu == False :
			ad_al_butonu.dongu = True
			self.mevcut_level = self.tamamlanan + 1

	def intro(self):
		if self.kisim == 1 :
			ekran_gecisi_1.yap("beyaz")
			if ekran_gecisi_1.dongu == False :
				g.pencere.fill(g.beyaz)
				gunluk.guncelle()
				if self.dialog == True :
					dialog_kutusu.ciz("kullanici")
				if dialog_butonu.dongu == False and self.dialog == True :
					text_blit(g.kullanici_adi + " :",180,465,18,"beyaz")
					geciken_blit_1.ciz("Günlüğüme bakıyordum ,her günümün aynı geçtiğini fark ettim. Büyü-",200,487)
					if geciken_blit_1.dongu == False : 
						geciken_blit_2.ciz("müştüm ,ama hiç üretken değildim. Bir amaç edinmek istiyordum.",200,509)
				elif self.dialog == False:
					self.kisim += 1
					self.dialog = True
					geciken_blit_1.dongu = True
					geciken_blit_2.dongu = True
					ekran_gecisi_1.dongu = True

		elif self.kisim == 2 :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				ekran_gecisi_2.yap("beyaz")
				if ekran_gecisi_2.dongu == False :
					g.pencere.fill(g.beyaz)
					g.pencere.blit(laptop_image,(0,0))
					text_blit("Justhink","ortala",176,30,"siyah")
					text_blit("asistan ile oyun yapımı !","ortala",210,24,"siyah")
					if self.dialog == True :
						dialog_kutusu.ciz("kullanici")
					if dialog_butonu.dongu == False and self.dialog == True :
						text_blit(g.kullanici_adi + " :",180,465,18,"beyaz")
						geciken_blit_1.ciz("kod yazmak bana mantıklı geldi. Ücretsiz kaynakları araştırdım ",200,487)
						if geciken_blit_1.dongu == False : 
							geciken_blit_2.ciz("ve kodlama temelleri ile oyun yapmak için JUSTHINK'i buldum",200,509)
					elif self.dialog == False:
						self.kisim += 1
						self.dialog = True
						geciken_blit_1.dongu = True
						geciken_blit_2.dongu = True
						ekran_gecisi_1.dongu = True
						ekran_gecisi_2.dongu = True
		elif self.kisim == 3 :
			g.pencere.fill(g.beyaz)
			g.pencere.blit(laptop_image,(0,0))
			text_blit("Justhink","ortala",176,30,"siyah")
			text_blit("asistan ile oyun yapımı !","ortala",210,24,"siyah")
			if self.dialog == True :
				dialog_kutusu.ciz("kullanici")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit(g.kullanici_adi + " :",180,465,18,"beyaz")
				text_blit("Justhink","ortala",176,30,"siyah")
				text_blit("asistan ile oyun yapımı !","ortala",210,24,"siyah")
				geciken_blit_1.ciz("Uygulamayı denesem ne kaybedebilirdim ,indirdim",200,487)
			elif self.dialog == False:
				self.kisim += 1
				self.dialog = True
				geciken_blit_1.dongu = True

		elif self.kisim == 4 :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				ekran_gecisi_2.yap("beyaz")
				if ekran_gecisi_2.dongu == False :
					g.pencere.fill(g.beyaz)
					g.pencere.blit(masaustu_image,(0,0))
					masaustu_butonu.changeColor((g.x,g.y))
					if self.dialog == True :
						dialog_kutusu.ciz("kullanici")
					if dialog_butonu.dongu == False and self.dialog == True :
						text_blit(g.kullanici_adi + " :",180,465,18,"beyaz")
						geciken_blit_1.ciz("Uygluma indi ve masaustume ekledim (dialog kutusunu kapatıp uygula-",200,487)
						if geciken_blit_1.dongu == False : 
							geciken_blit_2.ciz("maya basın ve Bölüm 2 başlasın)",200,509)
					elif self.dialog == False:
						if masaustu_butonu.dongu == True :
							masaustu_butonu.dongu = False
							self.dialog = True
							self.level_gecildi = True
							geciken_blit_1.dongu = True
							geciken_blit_2.dongu = True
							ekran_gecisi_1.dongu = True
							ekran_gecisi_2.dongu = True
	def level_2(self):
		if self.kisim == 1 :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				g.pencere.fill(g.siyah)
				text_blit("2. BÖLÜM","ortala",285,30,"beyaz")
				if self.bolumekrani_dongu <=250 :
					self.bolumekrani_dongu+=1
				else :
					ekran_gecisi_2.yap("beyaz")
				if ekran_gecisi_2.dongu == False :
					g.pencere.fill(g.beyaz)
					self.bolumekrani_dongu = 0
					self.kisim = 'ara1'
					ekran_gecisi_1.dongu = True
					ekran_gecisi_2.dongu = True
		elif self.kisim == 'ara1' :
			g.pencere.fill(g.beyaz)
			tablo1()
			if self.dialog == True :
				dialog_kutusu.ciz("yuz_1")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit("asistan :",180,465,18,"beyaz")
				geciken_blit_1.ciz("Justhink'e Hoşgeldin !",200,487)
				if geciken_blit_1.dongu == False : 
					geciken_blit_2.ciz("Oyun yapma eğitimi 6 kursdan oluşmakta.",200,509)
			elif self.dialog == False:
				self.kisim = 'ara2'
				self.dialog = True
				geciken_blit_1.dongu = True
				geciken_blit_2.dongu = True
		elif self.kisim == 'ara2' :
			g.pencere.fill(g.beyaz)
			tablo1()
			if self.dialog == True :
				dialog_kutusu.ciz("yuz_1")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit("asistan :",180,465,18,"beyaz")
				geciken_blit_1.ciz("Şuan 1. kurstasın .Bu Dialoğu kapattığında çıkacak soruların ,yukarıdaki",200,487)
				if geciken_blit_1.dongu == False : 
					geciken_blit_2.ciz("tabloya göre , doğru cevaplarını bul !",200,509)
			elif self.dialog == False:
				self.kisim = 2
				self.dialog = True
				geciken_blit_1.dongu = True
				geciken_blit_2.dongu = True
		elif self.kisim == 2 :
			if soru_1.soru_cekildi == False :
				soru_1.soru_cek()
				soru_2.soru_cek()
				soru_3.soru_cek()
			g.pencere.fill(g.beyaz)
			tablo1()
			if soru_1.sonuc and soru_2.sonuc and soru_3.sonuc :
				self.kisim = 'ara3'
				
		elif self.kisim == 'ara3' :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				g.pencere.fill(g.siyah)
				maze.draw()
				if self.dialog == True :
					dialog_kutusu.ciz("yuz_2")
				if dialog_butonu.dongu == False and self.dialog == True :
					text_blit("asistan :",180,465,18,"beyaz")
					geciken_blit_1.ciz("BİR ŞEYLER TERS GİDİYOR !!",200,487)
					if geciken_blit_1.dongu == False : 
						geciken_blit_2.ciz("SALDIRI ALTINDAYIZ ZAMAN AZ.",200,509)
				elif self.dialog == False:
					self.kisim = 'ara4'
					self.dialog = True
					geciken_blit_1.dongu = True
					geciken_blit_2.dongu = True
					ekran_gecisi_1.dongu = True
		elif self.kisim == 'ara4' :
			g.pencere.fill(g.siyah)
			maze.draw()
			if self.dialog == True :
				dialog_kutusu.ciz("yuz_2")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit("asistan :",180,465,18,"beyaz")
				geciken_blit_1.ciz("Dialoğu kapattığında bir an önce yön tuşlarıyla BİTİŞ'e ulaş",200,487)
				if geciken_blit_1.dongu == False : 
					geciken_blit_2.ciz("ve saldırıdan kurtul !!!",200,509)
			elif self.dialog == False:
				self.kisim = 'hack_1'
				self.dialog = True
				geciken_blit_1.dongu = True
				geciken_blit_2.dongu = True
		elif self.kisim == 'hack_1' :
			g.pencere.fill(g.siyah)
			maze.draw()
			g.pencere.blit(oyuncu_surf ,(player.x,player.y))
			if player.dongu == False :
				ekran_gecisi_1.dongu = True
				self.level_gecildi = True



	def level_3(self):
		if self.kisim == 1 :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				g.pencere.fill(g.siyah)
				text_blit("3. BÖLÜM","ortala",285,30,"beyaz")
				if self.bolumekrani_dongu <=250 :
					self.bolumekrani_dongu+=1
				else :
					ekran_gecisi_2.yap("beyaz")
				if ekran_gecisi_2.dongu == False :
					g.pencere.fill(g.beyaz)
					self.bolumekrani_dongu = 0
					self.kisim = 'ara1'
					ekran_gecisi_1.dongu = True
					ekran_gecisi_2.dongu = True
		elif self.kisim == 'ara1' :
			g.pencere.fill(g.beyaz)
			tablo2()
			if self.dialog == True :
				dialog_kutusu.ciz("yuz_1")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit("asistan :",180,465,18,"beyaz")
				if self.giris == 1:
					geciken_blit_1.ciz("Saldırıdan kurtuldun !",200,487)
					if geciken_blit_1.dongu == False : 
						geciken_blit_2.ciz("Bazen Justhink can sıkıcı saldırılara uğrayabiliyor.",200,509)
				elif self.giris == 2:
					geciken_blit_1.ciz("Başarıyla 2. kursa geçtin. Bu dialoğu kapattığında çıkacak soruların,",200,487)
					if geciken_blit_1.dongu == False : 
						geciken_blit_2.ciz("yukarıdaki bilgilere göre, doğru cevaplarını bul!",200,509)
			elif self.dialog == False:
				if self.giris == 1:
					self.giris = 2
				elif self.giris == 2:
					self.giris = 1
					self.kisim = 2
				self.dialog = True
				geciken_blit_1.dongu = True
				geciken_blit_2.dongu = True
		elif self.kisim == 2 :
			if soru_4.soru_cekildi == False :
				soru_4.soru_cek()
				soru_5.soru_cek()
				soru_6.soru_cek()
			g.pencere.fill(g.beyaz)
			tablo2()
			if soru_4.sonuc and soru_5.sonuc and soru_6.sonuc :
				self.level_gecildi = True

	def level_4(self):
		if self.kisim == 1 :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				g.pencere.fill(g.siyah)
				text_blit("4. BÖLÜM","ortala",285,30,"beyaz")
				if self.bolumekrani_dongu <=250 :
					self.bolumekrani_dongu+=1
				else :
					ekran_gecisi_2.yap("beyaz")
				if ekran_gecisi_2.dongu == False :
					g.pencere.fill(g.beyaz)
					self.bolumekrani_dongu = 0
					self.kisim = 'ara1'
					ekran_gecisi_1.dongu = True
					ekran_gecisi_2.dongu = True
		elif self.kisim == 'ara1' :
			g.pencere.fill(g.beyaz)
			tablo3()
			if self.dialog == True :
				dialog_kutusu.ciz("yuz_3")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit("asistan :",180,465,18,"beyaz")
				if self.giris == 1 :
					geciken_blit_1.ciz("Küçük saldır□ları ben çözüyo□um ama ısındım bazen harfleri",200,487)
					if geciken_blit_1.dongu == False : 
						geciken_blit_2.ciz("sö□leyemiyorum ve yakınd□ büyük bir saldırı his□ediyorum.",200,509)
				elif self.giris == 2 :
					geciken_blit_1.ciz("Artık 3. kurst□sın. Bu dialoğu kapattı□ında çıkacak sorula□ı□,",200,487)
					if geciken_blit_1.dongu == False :
						geciken_blit_2.ciz("□ukarıdaki bilgilere g□re, doğru cevapları□ı bul!",200,509)
			elif self.dialog == False:
				if self.giris == 1 :
					self.giris = 2
				elif self.giris == 2 :
					self.kisim = 2
					self.giris = 1
				self.dialog = True
				geciken_blit_1.dongu = True
				geciken_blit_2.dongu = True
		elif self.kisim == 2 :
			if soru_7.soru_cekildi == False :
				soru_7.soru_cek()
				soru_8.soru_cek()
				soru_9.soru_cek()
			g.pencere.fill(g.beyaz)
			tablo3()
			if soru_7.sonuc and soru_8.sonuc and soru_9.sonuc :
				self.kisim = 'ara2'
		elif self.kisim == 'ara2' :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				ekran_gecisi_1.yap("siyah")
				if ekran_gecisi_1.dongu == False :
					g.pencere.fill(g.beyaz)
					hack_2.ciz((g.x,g.y))
					if self.dialog == True :
						dialog_kutusu.ciz("yuz_2")
					if dialog_butonu.dongu == False and self.dialog == True :
						text_blit("asistan :",180,465,18,"beyaz")
						geciken_blit_1.ciz("Sen sorularla ilgilenirken soğudum ve düzeldi- , BİR SANİYE",200,487)
						if geciken_blit_1.dongu == False : 
							geciken_blit_2.ciz("YOKSA ?? HAYIIRR, YİNE SALDIRI ALTINDAYIZ.",200,509)
					elif self.dialog == False:
						self.kisim = 'ara3'
						self.dialog = True
						geciken_blit_1.dongu = True
						geciken_blit_2.dongu = True
						ekran_gecisi_1.dongu = True
						ekran_gecisi_2.dongu = True
		elif self.kisim == 'ara3' :
			g.pencere.fill(g.beyaz)
			hack_2.ciz((g.x,g.y))
			if self.dialog == True :
				dialog_kutusu.ciz("yuz_3")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit("asistan :",180,465,18,"beyaz")
				geciken_blit_1.ciz("BU SEFER SALDIRIDAN KURTULMAK İÇİN, SANA VERECEĞİM İPUÇLARINA",200,487)
				if geciken_blit_1.dongu == False : 
					geciken_blit_2.ciz("GÖRE DOSYALARI ÜSTLERİNE TIKLAYARAK DÜZENLE !!!",200,509)
			elif self.dialog == False:
				self.kisim = 'hack_2'
				self.dialog = True
				geciken_blit_1.dongu = True
				geciken_blit_2.dongu = True
		elif self.kisim == 'hack_2' :
			g.pencere.fill(g.beyaz)
			hack_2.ciz((g.x,g.y))
			if self.giris == 1 :
				if hack_2.istenen_1 > 13:
					text_blit('İpucu: Doğru olan dosya sayısı > Yanlış olan dosya sayısı','ortala',490,18)
				else:
					text_blit('İpucu: Yanlış olan dosya sayısı > Doğru olan dosya sayısı','ortala',490,18)
			elif self.giris == 2 :
				text_blit(f'İpucu: (Doğru dosya sayısı) * (Yanlış dosya sayısı) = {(hack_2.istenen_1)*(27-hack_2.istenen_1)}','ortala',490,18)
			elif self.giris == 3 :
				text_blit(f'İpucu: (Doğru dosya sayısı) // (Yanlış dosya sayısı) = {(hack_2.istenen_1)//(27-hack_2.istenen_1)}','ortala',490,18)
			elif self.giris == 4 :
				text_blit('İpucu: (hata: ipucu bulunamadı) Şansını kullan !','ortala',490,18)
			if hack_2.sonuc == True :
				self.kisim = 'ara4'
		elif self.kisim == 'ara4' :
			g.pencere.fill(g.beyaz)
			hack_2.ciz((g.x,g.y))
			if self.dialog == True :
				dialog_kutusu.ciz("yuz_2")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit("asistan :",180,465,18,"beyaz")
				if self.giris == 1 :
					geciken_blit_1.ciz("Biraz daha hızlı olabilir misin ?? Saldırgan bizden hızlı",200,487)
					if geciken_blit_1.dongu == False : 
						geciken_blit_2.ciz("davranırsa sisteme zarar verebilir.",200,509)
				if self.giris == 2 :
					geciken_blit_1.ciz("Harikaydı ama daha iyi olabilir! unutma yavaş kalırsak",200,487)
					if geciken_blit_1.dongu == False :
						geciken_blit_2.ciz("kurslar bile silinebilir.",200,509)
				if self.giris == 3 :
					geciken_blit_1.ciz("Görünüşe göre dosya kombinasyonu bulmakta iyisin! Hemen",200,487)
					if geciken_blit_1.dongu == False : 
						geciken_blit_2.ciz("devam edelim.",200,509)
				if self.giris == 4 :
					geciken_blit_1.ciz("Hızlı olmalısın, daha çok fazla bulunması gereken dosya",200,487)
					if geciken_blit_1.dongu == False : 
						geciken_blit_2.ciz("kombinasyonu var.",200,509)
			elif self.dialog == False:
				if self.giris < 4 :
					self.kisim = 'hack_2'
					self.giris += 1
					hack_2.__init__()
				else :
					self.giris = 1
					self.level_gecildi = True
				self.dialog = True
				geciken_blit_1.dongu = True
				geciken_blit_2.dongu = True

	def level_5(self):
		if self.kisim == 1 :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				g.pencere.fill(g.siyah)
				text_blit("5. BÖLÜM","ortala",285,30,"beyaz")
				if self.bolumekrani_dongu <=250 :
					self.bolumekrani_dongu+=1
				else :
					ekran_gecisi_2.yap("beyaz")
				if ekran_gecisi_2.dongu == False :
					g.pencere.fill(g.beyaz)
					self.bolumekrani_dongu = 0
					self.kisim = 'ara1'
					ekran_gecisi_1.dongu = True
					ekran_gecisi_2.dongu = True
		elif self.kisim == 'ara1' :
			g.pencere.blit(masaustu_image,(0,0))
			g.pencere.blit(hacked_image,(254,200))
			ok_butonu.changeColor((g.x,g.y))
			if self.dialog == True :
				dialog_kutusu.ciz("yuz_4")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit("asistan :",180,465,18,"beyaz")
				if self.giris == 1:
					geciken_blit_1.ciz("Ne yazık ki saldırgan kazandı, 4. kursu sistemde bulamıyorum !?",200,487)
					if geciken_blit_1.dongu == False :
						geciken_blit_2.ciz("Bulabilmem için bana yardımcı olman gerekecek.",200,509)
				elif self.giris == 2:
					geciken_blit_1.ciz("Dialoğu kapattığında ekrandaki bildirimin OK tuşuna bas ve 4.",200,487)
					if geciken_blit_1.dongu == False :
						geciken_blit_2.ciz("kursu kurtarmaya başlayalım.",200,509)
			elif self.dialog == False :
				if self.giris == 1 :
					self.giris = 2
				elif self.giris == 2 :
					self.giris = 1
					self.kisim = 2
				self.dialog = True
				geciken_blit_1.dongu = True
				geciken_blit_2.dongu = True
		elif self.kisim == 2 :
			g.pencere.blit(masaustu_image,(0,0))
			g.pencere.blit(hacked_image,(254,200))
			ok_butonu.changeColor((g.x,g.y))
			if ok_butonu.dongu == True :
				ok_butonu.dongu = False
				self.level_gecildi = True

	def level_6(self):
		if self.kisim == 1 :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				g.pencere.fill(g.siyah)
				text_blit("KURTARMA BÖLÜMÜ","ortala",285,30,"beyaz")
				if self.bolumekrani_dongu <=250 :
					self.bolumekrani_dongu+=1
				else :
					ekran_gecisi_2.yap("beyaz")
				if ekran_gecisi_2.dongu == False :
					g.pencere.fill(g.beyaz)
					self.bolumekrani_dongu = 0
					self.kisim = 'ara1'
					ekran_gecisi_1.dongu = True
					ekran_gecisi_2.dongu = True
		elif self.kisim == 'ara1' :
			g.pencere.fill(g.beyaz)
			tablo4()
			if self.dialog == True :
				if self.giris == 1 :
					dialog_kutusu.ciz("yuz_2")
				else :
					dialog_kutusu.ciz("yuz_1")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit("asistan :",180,465,18,"beyaz")
				if self.giris == 1:
					geciken_blit_1.ciz("Tabloya göre sana söyleyeceğim sayıları ikili sisteme çevir,",200,487)
					if geciken_blit_1.dongu == False :
						geciken_blit_2.ciz("Böylece 4. kurs için gerekli verilerin yerini bul.",200,509)
				elif self.giris == 2:
					geciken_blit_1.ciz("4. kursun sistemde yeri bulundu yardımların için teşekkürler!",200,487)
					if geciken_blit_1.dongu == False :
						geciken_blit_2.ciz("Hadi 4. kurstan devam edelim.",200,509)
			elif self.dialog == False:
				if self.giris == 1:
					self.kisim = 2
					self.giris = 2
				elif self.giris == 2 :
					self.level_gecildi = True
				self.dialog = True
				geciken_blit_1.dongu = True
				geciken_blit_2.dongu = True
		elif self.kisim == 2 :
			g.pencere.fill(g.beyaz)
			tablo4()
			if binary_1.sonuc and binary_2.sonuc and binary_3.sonuc :
				self.kisim = 'ara1'

	def level_7(self):
		if self.kisim == 1 :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				g.pencere.fill(g.siyah)
				text_blit("7. BÖLÜM","ortala",285,30,"beyaz")
				if self.bolumekrani_dongu <=250 :
					self.bolumekrani_dongu+=1
				else :
					ekran_gecisi_2.yap("beyaz")
				if ekran_gecisi_2.dongu == False :
					g.pencere.fill(g.beyaz)
					self.bolumekrani_dongu = 0
					self.kisim = 'ara1'
					ekran_gecisi_1.dongu = True
					ekran_gecisi_2.dongu = True
		elif self.kisim == 'ara1' :
			g.pencere.fill(g.beyaz)
			tablo5()
			if self.dialog == True :
				dialog_kutusu.ciz("yuz_1")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit("asistan :",180,465,18,"beyaz")
				if self.giris == 1:
					geciken_blit_1.ciz("5. kurstasın. Son 2 kurs kaldı buraya kadar gelmen beni çok mutlu",200,487)
					if geciken_blit_1.dongu == False : 
						geciken_blit_2.ciz("etti, umarım anlayarak gelmişsindir.",200,509)
				elif self.giris == 2:
					geciken_blit_1.ciz('Bu kursta çoğu oyunda kullanılan "mantıksal opertörler" konusu var.',200,487)
			elif self.dialog == False:
				if self.giris == 1:
					self.giris = 2
				elif self.giris == 2:
					self.giris = 1
					self.kisim = 2
				self.dialog = True
				geciken_blit_1.dongu = True
				geciken_blit_2.dongu = True
		elif self.kisim == 2 :
			if soru_10.soru_cekildi == False :
				soru_10.soru_cek()
				soru_11.soru_cek()
				soru_12.soru_cek()
			g.pencere.fill(g.beyaz)
			tablo5()
			if soru_10.sonuc and soru_11.sonuc and soru_12.sonuc :
				self.level_gecildi = True

	def level_8(self):
		if self.kisim == 1 :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				g.pencere.fill(g.siyah)
				text_blit("8. BÖLÜM","ortala",285,30,"beyaz")
				if self.bolumekrani_dongu <=250 :
					self.bolumekrani_dongu+=1
				else :
					ekran_gecisi_2.yap("beyaz")
				if ekran_gecisi_2.dongu == False :
					g.pencere.fill(g.beyaz)
					self.bolumekrani_dongu = 0
					self.kisim = 'ara1'
					ekran_gecisi_1.dongu = True
					ekran_gecisi_2.dongu = True
		elif self.kisim == 'ara1' :
			g.pencere.fill(g.beyaz)
			tablo6()
			if self.dialog == True :
				dialog_kutusu.ciz("yuz_1")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit("asistan :",180,465,18,"beyaz")
				if self.giris == 1:
					geciken_blit_1.ciz("6. yani son kurstasın!! Basit de olsa oyun yapabileceksin, test edip",200,487)
					if geciken_blit_1.dongu == False : 
						geciken_blit_2.ciz("paylaşman için Bilmen gereken çoğu şeyi öğrendin",200,509)
				elif self.giris == 2:
					geciken_blit_1.ciz("Hatta hemen son kursu bitir ve oyununu yap.",200,487)
			elif self.dialog == False:
				if self.giris == 1:
					self.giris = 2
				elif self.giris == 2:
					self.giris = 1
					self.kisim = 2
				self.dialog = True
				geciken_blit_1.dongu = True
				geciken_blit_2.dongu = True
		elif self.kisim == 2 :
			if soru_13.soru_cekildi == False :
				soru_13.soru_cek()
				soru_14.soru_cek()
				soru_15.soru_cek()
			g.pencere.fill(g.beyaz)
			tablo6()
			if soru_13.sonuc and soru_14.sonuc and soru_15.sonuc :
				self.level_gecildi = True

	def level_9(self):
		if self.kisim == 1 :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				g.pencere.fill(g.siyah)
				text_blit("9. BÖLÜM","ortala",285,30,"beyaz")
				if self.bolumekrani_dongu <=250 :
					self.bolumekrani_dongu+=1
				else :
					ekran_gecisi_2.yap("beyaz")
				if ekran_gecisi_2.dongu == False :
					g.pencere.fill(g.beyaz)
					self.bolumekrani_dongu = 0
					self.kisim = 'ara1'
					ekran_gecisi_1.dongu = True
					ekran_gecisi_2.dongu = True
		elif self.kisim == 'ara1' :
			g.pencere.fill(g.beyaz)
			tablo7()
			if self.dialog == True :
				dialog_kutusu.ciz("yuz_1")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit("asistan :",180,465,18,"beyaz")
				if self.giris == 1:
					geciken_blit_1.ciz("Kursu tamamladın tebrikler! Şimdi ise istediğin bir oyunu hediye",200,487)
					if geciken_blit_1.dongu == False : 
						geciken_blit_2.ciz("edeceğim. Oyunu test et, eğer bitirebiliyorsan paylaş.",200,509)
				elif self.giris == 2:
					geciken_blit_1.ciz("İki seçeneğin var Yılan oyunu ya da pong oyunu, hangisini paylaşmak",200,487)
					if geciken_blit_1.dongu == False :
						geciken_blit_2.ciz("istersin ?(dialoğu kapatıp çift tıklayarak seçin.)",200,509)
			elif self.dialog == False:
				if self.giris == 1:
					self.giris = 2
				elif self.giris == 2:
					self.giris = 1
					self.kisim = 2
				self.dialog = True
				geciken_blit_1.dongu = True
				geciken_blit_2.dongu = True
		elif self.kisim == 2 :
			g.pencere.fill(g.beyaz)
			tablo7()
			otest.ciz()
			if otest.sonuc == True:
				self.level_gecildi = True

	def final(self):
		if self.kisim == 1 :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				g.pencere.fill(g.siyah)
				text_blit("FİNAL","ortala",285,30,"beyaz")
				if self.bolumekrani_dongu <=250 :
					self.bolumekrani_dongu+=1
				else :
					ekran_gecisi_2.yap("beyaz")
				if ekran_gecisi_2.dongu == False :
					g.pencere.fill(g.beyaz)
					self.bolumekrani_dongu = 0
					self.kisim = 'ara1'
					ekran_gecisi_1.dongu = True
					ekran_gecisi_2.dongu = True
		elif self.kisim == 'ara1' :
			g.pencere.fill(g.beyaz)
			tablo8()
			if self.dialog == True :
				dialog_kutusu.ciz("yuz_1")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit("asistan :",180,465,18,"beyaz")
				if self.giris == 1:
					geciken_blit_1.ciz("Son olarak, oyununu internete yükle! Oyunun intenete yüklenirken",200,487)
					if geciken_blit_1.dongu == False : 
						geciken_blit_2.ciz("sana düşen görevler var.",200,509)
				elif self.giris == 2:
					geciken_blit_1.ciz("Oyunların korunması hakkında, Sana biraz bilgi vereceğim. Dialoğu",200,487)
					if geciken_blit_1.dongu == False :
						geciken_blit_2.ciz("kapat ve bilgileri okuyunca oyununu internete yüklemeye hazırsın!",200,509)
			elif self.dialog == False:
				if self.giris == 1:
					self.giris = 2
				elif self.giris == 2:
					self.giris = 1
					self.kisim = 'ara2'
				self.dialog = True
				geciken_blit_1.dongu = True
				geciken_blit_2.dongu = True
		elif self.kisim == 'ara2' :
			g.pencere.fill(g.beyaz)
			fgame_buton.draw()
			tablo8()
			if fgame_buton.sonuc:
				fgame_buton.sonuc = False
				self.kisim = 'ara3'
		elif self.kisim == 'ara3' :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				ekran_gecisi_1.dongu = True
				self.kisim = 2
		elif self.kisim == 2 :
			g.pencere.fill(g.beyaz)
			if not game.gecildi :
				game.main()
			else:
				self.kisim = 'ara4'
		elif self.kisim == 'ara4' :
			g.pencere.fill(g.beyaz)
			ekran_gecisi_1.yap("beyaz")
			if ekran_gecisi_1.dongu == False :
				ekran_gecisi_1.dongu = True
				self.kisim = 'ara5'
		elif self.kisim == 'ara5' :
			g.pencere.fill(g.beyaz)
			tablo9()
			if self.dialog == True :
				dialog_kutusu.ciz("yuz_1")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit("asistan :",180,465,18,"beyaz")
				if self.giris == 1:
					geciken_blit_1.ciz("Oyunun internete başarıyla yüklendi tebrikler. Kursumuz henüz",200,487)
					if geciken_blit_1.dongu == False :
						geciken_blit_2.ciz("bu kadar bilgiyi kapsamakta.",200,509)
				elif self.giris == 2:
					geciken_blit_1.ciz("Unutma her zaman internetten bile gerçek bir yazılım dili",200,487)
					if geciken_blit_1.dongu == False :
						geciken_blit_2.ciz("öğrenip dilediğin oyunu yapabilirsin!",200,509)
			elif self.dialog == False:
				if self.giris == 1:
					self.giris = 2
				elif self.giris == 2:
					self.giris = 1
					self.kisim = 'ara6'
				self.dialog = True
				geciken_blit_1.dongu = True
				geciken_blit_2.dongu = True
		elif self.kisim == 'ara6' :
			g.pencere.fill(g.beyaz)
			tablo9()



g = Game() #oyun döngüsünde kullanmak için Game sınıfından nesne oluşturuldu
l = Game_level()
db.downdate()
while g.running :
	g.oyun_dongusu()
pygame.quit()
