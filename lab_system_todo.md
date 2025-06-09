# ✅ TO-DO LISTA: System zleceń i wymiany danych laboratoryjnych

---

## 🔹 I. Wymagania ogólne

- [ ] Określenie ról użytkowników:

  - Administrator
    Możliwości:
    - Zarządzanie użytkownikami (lekarze, technicy), ✅
    - Resetowanie haseł, 
    - Przegląd aktywności, 
    - Weryfikacja logów. [?] - opcjonalnie
    Panel:
    - Tabela użytkowników, ✅
    - Ustawienia systemowe,
    - Statystyki. [?] - opcjonalnie

  - Lekarz
    Możliwości:
    - Składanie nowych zleceń laboratoryjnych dla pacjentów, ✅
    - Podgląd wyników badań pacjentów, 
    - Przegląd historii zleceń. ✅
    Panel:
    - Formularz nowego zlecenia, ✅
    - Lista pacjentów, ✅
    - Wyniki badań. ✅

  - Laborant / Technik
    Możliwości:
    - Odbieranie zleceń, ✅
    - Dodawanie informacji o próbkach, 
    - Wprowadzanie wyników badań, ✅
    - Zatwierdzanie / aktualizacja statusów. ✅
    Panel:
    - Lista otwartych zleceń, ✅
    - Formularz rejestracji próbki, ✅
    - Formularz dodawania wyników. ✅

  - Pacjent
    Możliwości:
    - Podgląd wyników swoich badań (po zalogowaniu),
    - Powiadomienia o dostępnych wynikach.
    Panel:
    - Lista wykonanych badań,
    - Szczegóły wyników,
    - Możliwość pobrania PDF.

- [ ] Spisanie scenariuszy użycia dla każdej roli
- [ ] Zaprojektowanie przepływu danych (workflow: zlecenie → próbka → wynik)

---

## 🔹 II. Technologie (proponowane)

| Warstwa          | Technologia              |
| ---------------- | ------------------------ |
| Frontend         | React + Tailwind CSS     |
| Backend          | FastAPI (Python)         |
| Baza danych      | PostgreSQL (dev: SQLite) |
| Autoryzacja      | JWT (z rolami)           |
| ORM              | SQLAlchemy               |
| Haszowanie haseł | passlib (bcrypt)         |
| Testy            | pytest                   |
| API dokumentacja | Swagger (FastAPI)        |
| Inne             | Docker, Git              |

---

## 🔹 III. Backend – Moduły i funkcje

### 🔐 Autoryzacja / uwierzytelnianie

- [x] Rejestracja użytkowników z rolami (`/register`)
- [ ] Logowanie (`/login`) + JWT z rolą
- [ ] Middleware weryfikujący role przy dostępie do endpointów
- [x] Zatwierdzanie roli `doctor` przez admina (`/admin/approve_doctor/{id}`)

### 📋 Zarządzanie zleceniami

- [ ] Tworzenie zlecenia (doctor)
- [ ] Lista zleceń przypisanych do pacjentów (doctor, lab_tech)
- [ ] Pobieranie szczegółów zlecenia

### 🧪 Obsługa próbek i wyników

- [x] Dodawanie próbki (lab_tech)
- [x] Dodawanie wyników (lab_tech)
- [x] Oznaczanie wyników jako „poza normą”
- [x] Zakończenie badania / zlecenia

### 📤 Wymiana danych

- [ ] JSON-owe API wyników (`/results`)
- [ ] Eksport danych w formacie:
  - [ ] HL7 ORU^R01
  - [ ] FHIR (Observation)
- [ ] Pobieranie wyników przez pacjenta (tylko swoje)

---

## 🔹 IV. Frontend – Interfejsy

### 💼 Panel administracyjny

- [ ] Zatwierdzanie lekarzy
- [ ] Zarządzanie użytkownikami
- [ ] Statystyki / logi

### 👨‍⚕️ Panel lekarza

- [ ] Tworzenie zleceń
- [ ] Lista pacjentów
- [ ] Historia wyników badań

### 🧑‍🔬 Panel laboranta

- [ ] Rejestracja próbek
- [ ] Wprowadzanie wyników
- [ ] Zlecenia oczekujące na wynik

### 👤 Panel pacjenta

- [ ] Podgląd wyników
- [ ] Pobieranie wyników (PDF / HL7 / FHIR)

---

## 🔹 V. Dodatki i bezpieczeństwo

- [ ] Logowanie z JWT + wygasanie sesji
- [ ] Rejestracja z walidacją adresu email (opcjonalnie)
- [ ] Audyt zmian (kto dodał, edytował wynik)
- [ ] Wersjonowanie API (v1, v2...)
- [ ] Testy jednostkowe i integracyjne
- [ ] Docker – uruchamianie całego systemu w kontenerze

---

## 🔹 VI. Minimalne wymagania

✅ System powinien zawierać:

- Zarządzanie użytkownikami z różnymi rolami i poziomem uprawnień,
- Możliwość składania i przetwarzania zleceń,
- Przechowywanie i prezentację wyników badań,
- Możliwość wymiany danych w standardzie HL7/FHIR lub JSON API,
- Obsługę próbek i ich statusów,
- Bezpieczne logowanie, autoryzacja i prywatność danych pacjenta.


