# BirdWeather2eBird
Converts BirdWeather CSV Exports into eBird Record Format (Extended)

## 📋 Features

- Import .csv from BirdWeather
- Export .csv in eBird Extended Record Format

---

## 🐍 Requirements

- Python 3.11 or newer
- No external libraries required
  
---

## 🛠 Installation & Configuration

This project does not require any external dependencies and runs natively on Python **3.11+**.

### 1. Clone the Repository
```
bash
git clone https://github.com/spikelite/BirdWeather2eBird.git
cd BirdWeather2eBird
```

### 2. (Optional) Create a Virtual Environment
```
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Configure the script
At minimum you must configure the following values in `conf/config.py`<br>
`STATE` - 2-letter state code, leave blank if your country does not use state codes<br>
`COUNTRY` - 2-letter country code<br>
`PROTOCOL` - Select one: {`Stationary`, `Traveling`, `Incidental`, `Historical`}<br>
It is recommended that you also configure the following values in `conf/config.py`<br>
`CHECKLIST_COMMENTS` - Useful information about the data collection source, such as PUC ID#

---

## 🚀 Running the Application

TODO

---

## 📄 License

This software is provided for **personal, non-commercial use only**.  
You may view and run this software for personal educational or non-profit purposes.

You may **not**:
- Use this software in any commercial or enterprise context.
- Distribute modified or unmodified versions.
- Sell or include this software as part of a paid or monetized service or product.
- Use this software in any for-profit capacity.

All rights are reserved by the author.

---
