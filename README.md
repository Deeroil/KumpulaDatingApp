# Kumpulan kampuksen ihmis_haku_app

Tietokannat ja web-ohjelmointiprojekti 2024


### Tämänhetkinen toiminnallisuus:
* Voi rekisteröityä.
* Voi kirjautua.
* Voi kirjautuneena katsoa listaa muista käyttäjistä.
* Voi klikata checkboxia ja lähettää lomakkeen, jolla tykkäys lähetetään tietokantaan. Tämä ei tosin vielä vaikuta mihinkään.

#### Mitä esim puuttuu:
* Ei validointia syötteelle.
* Ei vielä profiilin muokkaamista jne.


### Käyttöohje:

Luo juureen tiedosto `.env` ja aseta sinne `DATABASE_URL` sekä `SECRET_KEY`

Lataa riippuvuudet `pip install -r requirements.txt`

Luo tietokantataulut `psql > schema.sql`

Jos haluat poistaa sovelluksen taulut, käytä `psql > drop.sql`

`psql > userdata.sql` sisältää useita valmiita profiileja, joiden kaikkien salasana on `salasana`.



#### TODO:
- yksinkertainen UI
- tekstikenttien validointi jne
- UUID:t

Käyttäjä:
- voi selata muita käyttäjiä (toteutettu)
	- kaikkia käyttäjiä? vai rajoitettu omien ominaisuuksien tai haettavan seuran mukaan?
- ilmoitus jos molemmat ovat tykänneet toisensa

Ehkä:
- tilin poistaminen
- keskusteluominaisuus, alustavasti ei suunniteltu
- Telegram-botti
- Jokainen käyttäjä voi millaista seuraa heistä voi hakea, eli kaikki eri matchausominaisuudet eivät automaattisesti valittavina
  - Ehkä tosin mahdollisesti ongelma jos edellisiä pyyhkiytyy pois?
	- vaihtoehtoisesti kaikilla kaikki checkboxit jos useammanlaisia vaihtoehtoja, mutta jos ei itse klikkaa niin sillä selviää


Lista pohdituista tauluista:
* ehkä useampia like-tauluja jokaisesta osiosta olisi oma taulunsa
	* cuddling, romantic, sexual, friendship? entä opiskeluseura?

- kuvat: tietokanta niille, blobeina säilöttynä tai path. ehkä vain yksi kuva per henkilö, onko optional?


Ajatuksia:
- olisiko mukavampi tietokannan käyttämisen suhteen, jos profiilin ei-kirjautumistiedot olisi eritelty "profiili"-tauluun, jossa mm. nimi, ala, aloitusvuosi, kuva, teksti ja muut tiedot
- mitä tapahtuu jos joku poistaa profiilin ja on "matchatty"?