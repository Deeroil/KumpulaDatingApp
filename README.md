# Kumpulan kampuksen ihmis_haku_app

Tietokannat ja web-ohjelmointiprojekti 2024


### Tämänhetkinen toiminnallisuus:
* Voi rekisteröityä.
* Voi kirjautua.
* Voi kirjautuneena katsoa listaa muista käyttäjistä.
* Voi klikata checkboxia ja lähettää lomakkeen, jolla tykätään käyttäjästä.
* Molemminpuoliset tykkäykset näkyvät profiilirivin vieressä sekä erillisellä sivullaan
* Matchia ja tykkäystä ei voi poistaa
* Validointia toteutettu, ja virheviestejä
* Omaa profiilia voi muokata (nimi, profiiliteksti)
* Orientaatioita voi lisätä profiiliin tai poistaa

### Käyttöohje:

Luo juureen tiedosto `.env` ja aseta sinne `DATABASE_URL` sekä `SECRET_KEY`

Lataa riippuvuudet `pip install -r requirements.txt`

Luo tietokantataulut `psql < schema.sql`

Jos haluat poistaa sovelluksen taulut, käytä `psql < drop.sql`

`psql < userdata.sql` sisältää useita valmiita profiileja, joiden kaikkien salasana on `salasana`.
(huom: sovelluksen sisällä tehdyissä profiileissa kyseinen salasana olisi liian lyhyt)



#### Kehitysideoita
- UI:n parantaminen
	- virheidenhallintaa enemmän samalle sivulle
	- profiileille omat sivut, tyyliä /:username (tätä varten enemmän profiiliin?)
- UUID:t
- kuvien lisääminen: tietokanta niille, blobeina säilöttynä tai path. ehkä vain yksi kuva per henkilö, optional?
- ehkä useampia like-tauluja, joka kategorialle olisi oma taulunsa
	- cuddling, romantic, sexual, friendship? entä opiskeluseura?
- käyttäjistä vain osan näyttäminen (esim: älä näy tietyn orientaation ihmisille)
- keskusteluominaisuus
- Telegram-botti
- salasanat
	- erikoismerkkien vaatiminen tai vastaava
	- salasanan vaihtaminen