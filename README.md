# Kumpulan kampuksen ihmis_haku_app

Tietokannat ja web-ohjelmointiprojekti 2024

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

