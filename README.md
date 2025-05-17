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
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install 3rd Party Libraries
```
python -m pip install -r requirements.txt
```

### 4. Configure the script
At minimum you must configure the following values in `conf/config.py`<br>
`STATE` - 2-letter state code, leave blank if your country does not use state codes<br>
`COUNTRY` - 2-letter country code<br>
`PROTOCOL` - Select one: {`Stationary`, `Traveling`, `Incidental`, `Historical`}<br>
It is recommended that you also configure the following values in `conf/config.py`<br>
`CHECKLIST_COMMENTS` - Useful information about the data collection source, such as PUC ID#

---

## 🚀 Running the Application

1. Create an account on BirdWeather (https://app.birdweather.com/signup) if you do not have one, or login to your account if you do
Note: you must use a valid email address as exports are emailed to this account
2. Go to the Data Explorer on BirdWeather (https://app.birdweather.com/data)
3. Add filters on the left hand side to limit the data to your desired scope, and press "Update Filters".<br>
Note: This will typically include setting the `Stations` and `Time Range`/`Time of Day`<br>
![image](https://github.com/user-attachments/assets/be4448d4-6048-4b8e-ad2b-811172b48024)<br>
5. Press the "Export" button, in the top right of the window<br>
![image](https://github.com/user-attachments/assets/a1451421-72d7-4cb9-8701-b481a225ff01)<br>
6. Validate your email address, and press the "Submit" button<br>
![image](https://github.com/user-attachments/assets/d1373967-77e1-491e-968c-b1137c8f0c68)<br>
7. Check your email, there should be an email with the Subject `BirdWeather Notifications` which contains a link to download the .csv, download it<br>
![image](https://github.com/user-attachments/assets/38af973b-4200-4603-8ddd-a830c75e448c)<br>
8. Run the script, replace `PATH_TO_BIRDWEATHER` with the file path to the file you downloaded in the previous step, set any additional CLI arguments you wish (see `--help`)<br>
```
python BirdWeather2eBird.py -i PATH_TO_BIRDWEATHER
```
i.e.
```
python BirdWeather2eBird.py -i 'C:\Users\BirdWatcher\Desktop\Detections-1234567890-1-abcd123.csv' -o 'C:\Users\BirdWatcher\Desktop\ebird_upload.csv'
```
9. Create an eBird account (https://secure.birds.cornell.edu/identity/account/create) if you do not have one, or login to your account if you do
10. Go to the eBird `Import a file` page (https://ebird.org/import/upload.form)
11. Select the processed file that was output by BirdWatcher2eBird, and set the format to `eBird Record Format (Extended)`, then press "Import File"<br>
![image](https://github.com/user-attachments/assets/0919c778-6003-4f3e-8561-ddf6ba18465c)
![image](https://github.com/user-attachments/assets/a44abac9-8720-4f95-806a-1b2e8c4a8a3c)
12. Once successful, you will be redirected to the `My imports` section where you should see your import listed as `Completed`<br>
![image](https://github.com/user-attachments/assets/61bc0ad7-5aef-4ef7-ad81-462431ed2432)




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
