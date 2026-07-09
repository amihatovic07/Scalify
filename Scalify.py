# Scalify 
# Ova aplikacija omogućuje korisniku da unese dimenzije slike i izračuna potrebne vrijednosti za skaliranje.

# Funkcija koja ispisuje uvodnu poruku i upute za korištenje aplikacije

import sys, numpy as np, matplotlib.pyplot as plt


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

# Globalna varijabilna polja

vis = []
sir = []

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

# Glavna funkcija koja pokreće cijeli program

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
            
main()