from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import os
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

YOUR_PHONE = "+916380541445"  

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    name = request.form['name']
    message = request.form['message']
    # Normally you’d trigger Selenium or store the message
    print(f"Message from {name}: {message}")
    return f"<h1>Thanks, {name}! Your message has been received.</h1>"

def send_whatsapp_message(phone, message):
    options = Options()
    options.add_argument("--user-data-dir=C:/whatsapp_profile_data/")
    options.add_argument("--profile-directory=Default")
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(f"https://web.whatsapp.com/send?phone={phone}&text={message}")
        print("Waiting for WhatsApp Web to load...")
        time.sleep(10)
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]')))
        send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]')))
        send_btn.click()
        print("Message sent!")
        time.sleep(3)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
