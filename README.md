# 🚀 Gra Tekstowa RPG z GUI (Tkinter)

## **📜 Opis projektu**
Stwórz tekstową grę RPG z graficznym interfejsem użytkownika (GUI) opartym na bibliotece Tkinter, w której gracz podejmuje decyzje wpływające na rozwój fabuły i postaci. Gra powinna być zorganizowana zgodnie z wzorcem MVC (Model-View-Controller), podzielona na moduły/pliki oraz wykorzystywać mechanizmy dziedziczenia i pracy z plikami.

---

## **🧱 Struktura projektu (zgodnie z MVC + podział na pliki)**

---

## **🎮 Funkcjonalności**
**🌍 Lokacje**:
- Minimum trzy unikalne lokacje: Las, Zamek, Wioska.
- Każda lokacja oferuje różne interakcje:
- Eksploracja
- Walka
- Rozmowa z NPC
- Losowe wydarzenia

**⚔️ System walki**:
- Mechanika walki turowej z losowymi obrażeniami (1–10).
- Zarówno gracz, jak i przeciwnik mają punkty HP.
- Możliwość używania przedmiotów (np. mikstury, bronie).
- Dziedziczenie klas przeciwników (np. Goblin, Rycerz, Smok dziedziczą po klasie Enemy).

**🛡️ Przedmioty**:
- Różne typy przedmiotów (dziedziczenie z klasy bazowej Item):
- HealthPotion
- Sword
- Armor
- Możliwość zbierania, przechowywania (ekwipunek) i używania przedmiotów.

**📖 Fabuła i decyzje**:
- Nieliniowa fabuła z co najmniej dwoma różnymi zakończeniami.
- Decyzje gracza wpływają na przebieg gry (moralność, lojalność, wybory fabularne).

**📈 System postaci**:
- Rozwój postaci: zdobywanie doświadczenia (EXP), awans na wyższe poziomy.
- Wzrost statystyk (atak, obrona, zdrowie) wraz z poziomem.
- Klasa postaci do dziedziczenia (PlayerCharacter), z rozszerzalnością (np. Wojownik, Mag).

**🗃️ System zapisu gry**:
- Możliwość zapisu i wczytania gry do/z pliku .json lub .txt.
- Zapisuje: statystyki postaci, ekwipunek, aktualną lokację, postęp fabularny.

**🖥️ Graficzny interfejs użytkownika**:
- Zbudowany z wykorzystaniem Tkinter.
- Dynamiczne GUI:
- Panel statystyk
- Opis aktualnej lokacji
- Okno dialogowe
- Przyciskowe menu akcji (walka, eksploracja, ekwipunek, rozmowa)
- GUI oddzielone w warstwie View zgodnie z MVC.

---

## **🛠️ Technologie**
- Python 3.8+
- Biblioteka **Tkinter**

---

## **📋 Wymagania**
- Python zainstalowany na komputerze.
- Środowisko IDE lub edytor tekstu (np. VS Code, PyCharm).
- Opcjonalnie: Wirtualne środowisko Python (`venv`).

---

## **💡 Pomysły na rozszerzenia (opcjonalne)** :
- System reputacji lub moralności.
- Mini-gra handlowa z kupcami.
- Wrogowie z AI (np. różne zachowania w zależności od HP).
- Losowe generowanie lokacji.
- Tryb „Nowa Gra+”.

---

## **📦 Instalacja**
1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/uzytkownik/gra-rpg-tkinter.git
   cd gra-rpg-tkinter
