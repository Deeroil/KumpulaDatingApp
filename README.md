# Kumpulan kampuksen ihmis_haku_app

Tietokannat ja web-ohjelmointiprojekti 2024


Tämänhetkinen toiminnallisuus:

Voi lisätä uuden käyttäjän.
Voi valita kolmesta eri alasta yhden.
Ei validointia syötteelle.
Ei vielä swipeämis-funktionaalisuutta.



Taulujen luontia varten:

		CREATE TABLE studyfields (id SERIAL PRIMARY KEY, field TEXT);
		INSERT INTO studyfields (field) VALUES ('Computer Science');
		INSERT INTO studyfields (field) VALUES ('Math');
		INSERT INTO studyfields (field) VALUES ('Physics');

		CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT, studyfield_id INTEGER REFERENCES studyfields, bio TEXT);
		INSERT INTO users (name, studyfield_id, bio) VALUES ('Maija', '1', 'Moi oon Maija ja olen hauki');
		INSERT INTO users (name, studyfield_id, bio) VALUES ('Joonas', '3', 'gucci laif and all things topology');

		CREATE TABLE swipes (id SERIAL PRIMARY KEY, swiper_id INTEGER REFERENCES users, swipee_id INTEGER REFERENCES users);
		
		INSERT INTO swipes VALUES (1, 2);






Alla ajatuksia, keskeneräisiä:

- yksinkertainen UI

Käyttäjä:
- voi tehdä tilin ja kirjautua 
- voi selata muita käyttäjiä:
	- kaikkia käyttäjiä vai rajoitettu omien ominaisuuksien tai haettavan seuran mukaan?
- voi osoittaa kiinnostuksensa (klikata checkboxin tmv)
- tulee ilmoitus jos molemmat ovat valinneet toisensa
    - mahdollisesti näissä matchausjutuissa useita eri aihepiirejä (halailu, kaveri, seksi, jne)

Ehkä:
- tilin poistaminen
- keskusteluominaisuus, alustavasti ei suunniteltu
- Telegram-botti
- Jokainen käyttäjä voi millaista seuraa heistä voi hakea, eli kaikki eri matchausominaisuudet eivät automaattisesti valittavina
  - Ehkä tosin mahdollisesti ongelma jos edellisiä pyyhkiytyy pois?
	- vaihtoehtoisesti kaikilla kaikki checkboxit jos useammanlaisia vaihtoehtoja, mutta jos ei itse klikkaa niin sillä selviää


Lista pohdituista tauluista:

- käyttäjät:
	* uuid
	* rooli: admin/user? (mitä admin voi tehdä?)
	* nimi,
	* opiskeluala: reference,
	* aloitusvuosi: optional?
  * kuva (referenssi kuvatauluun)
  * profiiliteksti (vai nämä erilliseen tietokantaan ja referenssi?)
  * telegram-tunnus: ehkä jaettu vasta jos match

	* suhdetyyli (mono/poly/anarkisti/ambi/en tiedä): optional?
	* alkoholitaulukko: optional?

	* lempikurssi?
  * lempitapahtuma?

- opiskelualat: [kiinteä listaus]

- matchaus-taulu: liitostaulu (ketkä valinneet toisen)
	* ehkä useampia asioita joissa match, jokaisesta osiosta olisi oma taulunsa
		* cuddling, romantic, sexual, friendship? entä opiskeluseura?

- kuvat: tietokanta niille, blobeina säilöttynä tai path. ehkä vain yksi kuva per henkilö, onko optional?


Ajatuksia:
- olisiko mukavampi tietokannan käyttämisen suhteen, jos profiilin ei-kirjautumistiedot olisi eritelty "profiili"-tauluun, jossa mm. nimi, ala, aloitusvuosi, kuva, teksti ja muut tiedot

- muista lisätä UUID:t myöhemmin
- references vai foreign key?


ehkä validoi:
  - onks telegram_nikki tarpeeks pitkä/lyhyt
  - kans bioon

- mitä tapahtuu jos joku poistaa profiilin ja se on swipennyt tai sitä on swipetty?



MITÄ OIS HYVÄ TEHDÄ NYT:

- taulut
- taulujen initioiminen salee lmao
- se että tauluihin voi lisätä asioita wow
- voi klikata match
	- se tallentuu
	- jos molemmissa: joku ilmoituss