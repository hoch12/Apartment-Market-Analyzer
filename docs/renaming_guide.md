# Průvodce Přejmenováním Projektu

Protože se projekt kompletně změnil z "Car Market Analyzer" na "Apartment Market Analyzer", pravděpodobně budete chtít přejmenovat i složku projektu a Git repozitář.

Zde je bezpečný postup:

## 1. Přejmenování Lokální Složky

1. **Zavřete VS Code** a všechny běžící procesy (terminály, aplikace).
2. Otevřete Průzkumníka souborů (Finder na Macu).
3. Najděte složku `Car-Market-Analyzer`.
4. Přejmenujte ji na `Apartment-Market-Analyzer`.
5. Znovu otevřete tuto novou složku ve VS Code.

> **Poznámka**: Pokud používáte virtuální prostředí (`.venv`), může být nutné ho znovu vytvořit, protože v něm mohou být absolutní cesty ke staré složce.
> ```bash
> # Pokud .venv nefunguje:
> rm -rf .venv
> python3 -m venv .venv
> source .venv/bin/activate
> pip install -r requirements.txt
> ```

## 2. Přejmenování na GitHubu (Remote)

1. Jděte na stránku svého repozitáře na GitHubu.
2. Klikněte na **Settings** (Nastavení).
3. Hned nahoře v sekci **General** uvidíte pole **Repository name**.
4. Přepište `Car-Market-Analyzer` na `Apartment-Market-Analyzer`.
5. Klikněte na **Rename**.

## 3. Aktualizace Lokálního Gitu

Po přejmenování na GitHubu musíte svému lokálnímu Gitu říct, kde je nová adresa (i když GitHub často přesměrovává i starou adresu, je lepší to mít čisté).

Otevřete terminál v nové složce projektu a spusťte:

```bash
git remote set-url origin https://github.com/hoch12/Apartment-Market-Analyzer.git
```

Ověřte změnu:
```bash
git remote -v
```

HOTOVO! Nyní máte kompletně přejmenovaný projekt.
