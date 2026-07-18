# Scalify 

* Trenutna verzija programa: 1
  
Aplikacija čija je namjena olakšati računanje prostora i vizualizaciju samog prostora, prilikom detaljnog analiziranja samog prostora biti će moguće vizualizirati cijelokupni prostor u 3D prostoru te koristiti ga kao model

## Sadržaj

1. Sadržaj
2. Opis programa
3. Opis programskog koda
4. Ideja rada
5. Ideja algoritma

## Opis programa

Scalify je program koji uzima točke u prostoru na temelju korisničkog unosa te formira graf koji simulira 2D oblik prostora isto kao što formira kalkulaciju broja kvadrata unutar tog prostora što je moguće primjeniti unutar nekih arhitektonskih računica primjerice oko renovacije prostora i saznanja o kakvom prostoru se radi točno.

## Opis programskog koda

Scalify se bazira na modalnom radu gdje je sve podijeljeno na više funkcija a potom pozvano u istoj funkciji main.

Uvodna sekcija uvozi sve potrebne pakete za rad sa podatcima unutar python progama,
programski kod:

```py
  import sys, numpy as np, matplotlib.pyplot as plt
```

Dodatna podsekcija je vezana uz varijabilna polja,
programski kod:

```py
    vis = []
    sir = []
```

Nakon uvodne sekcije se počinju formirati funkcije za zasebne funkcionalnosti programa,
programski kod:

```py
  def uvod():
    print("-----------------------------------------------------------------------------------------")
    print("Dobrodošli u Scalify aplikaciju!")
    print("Ova aplikacija omogućuje unos dimenzija slike i izračunavanje potrebnih vrijednosti za skaliranje.")
    print("Molimo unesite dimenzije slike u pikselima (širina i visina).")
    print("Nakon unosa dimenzija, aplikacija će izračunati kvadrat prostora koji zauzima slika.")
    print("Također, možete unijeti više dimenzija i aplikacija će ih sve zbrojiti.")
    print("Za izlazak iz aplikacije, unesite 'Ne' kada se pita želite li unijeti još jednu točku.")
    print("-----------------------------------------------------------------------------------------")
    print(" ")

  # Funkcija koja ispisuje izbornik za funkcionalnosti aplikacije
  
  def izbornik():
      print("Izbornik funkcionalnosti:")
      print("1. Unos dimenzija slike")
      print("2. Izračunavanje kvadrata prostora")
      print("3. Crtanje prostora prema dimenzijama")
      print("4. Izlaz iz aplikacije")
      print(" ")
  
  # Funkcija za unos dimenzija slike
  
  def unosenje():
      uneseno = False
      while True:
          if (uneseno):
              odg1 = input("Želite li unijeti još jednu točku?: ").lower()
              if odg1 in ["ne", "no", "nope", "ne hvala", "ne, hvala", "ne, molim", "ne, molim vas", "ne, ne hvala"]:
                  return vis, sir
              elif odg1 in ["da", "yes", "yep", "sure", "yea", "ok", "okay", "alright", "fine", "yeah", "može", "naravno", "sigurno", "da, naravno", "da, hvala", "da, molim"]:
                  uneseno = False
                  continue
              else:
                  print("Nevažeći unos. Molimo unesite 'da' ili 'ne'.")
                  continue
          x = int(input("unesite položaj širine: "))
          y = int(input("unesite položaj visine: "))
          vis.append(x)
          sir.append(y)
          uneseno = True
  
  # Funkcija za računanje kvadrata prostora
  
  def kalkulacija(x, y):
      n = len(x)
      povrsina = 0
      for i in range(n):
          j = (i + 1) % n
          povrsina += x[i] * y[j]
          povrsina -= x[j] * y[j]
      return abs(povrsina) / 2
  
  # Funkcija za crtanje grafičkog prikaza dimenzija slike
  
  def crtanje(a, b):
      y = a
      x = b
  
      x.append(x[0])
      y.append(y[0])
  
      plt.fill(x, y, alpha=0.3)
      plt.plot(x, y, marker="o")
      plt.show()
      return "Iscrtano!"
```

Nakon formiranja svih potrebnih funkcija počinje glavni dio, main funkcija gdje se pozivaju sve funkcionalnosti i tako se krećemo po programu,
programski kod:

```py
  def main():
      uvod()
      while True:
          izbornik()
          odgovor = input("Odaberite funkcionalnost (1, 2, 3 ili 4): ")
          if odgovor == "1":
              unosenje()
          elif odgovor == "2":
              rezultat = kalkulacija(vis, sir)
              print(f"Rezultat Kalkulacije kvadrata prostora: {rezultat}")
          elif odgovor == "3":
              crtanje(vis, sir)
          elif odgovor == "4":
              print("Izlaz iz aplikacije.")
              sys.exit()
          else:
              print("Nevažeći izbor. Molimo odaberite 1, 2 ili 3 4")
```

Finalni dio programskog koda poziva main funkciju te tako se pokreće rad cijelokupnog programa,
programski kod:

```py
  main()
```

## Ideja rada

Navedeni program je predviđen kao pomoć sa analizom prostora gdje glavna ideja jest da se prostor simulira i pridoda sugestija za radnje sa nekim prostorom gdje bi moglo se to primjeniti u građevinarstvu, dizajnu prostorija, ličenju prostorija i ostalim važnim poslovnim djelatnostima vezanim uz prostor.

## Ideja algoritma

  Algoritam se sastoji od više podalgoritma koji su formirani kao funkcije svaka funkcija radi kao jedna funkcionalnost pozvana u glavnoj funkciji main, funkcije koje su formirane: Funkcija koja ispisuje izbornik za funkcionalnosti aplikacije, Funkcija za unos dimenzija slike, Funkcija za računanje kvadrata prostora, Funkcija za crtanje grafičkog prikaza dimenzija slike.
  Glavni algoritam je koncizno namijenjen za pokrivanje svakog rubnog slučaja tokom korištenja progama.
  
