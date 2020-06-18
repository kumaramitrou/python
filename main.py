from flask import Flask, render_template, request, redirect
import smtplib
import secrets
import pandas

details = dict()
msg = "Your OTP is {}, please use this before it expire. (Expiration Time = 5 minutes)"  
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

secretsgen = secrets.SystemRandom()

app = Flask(__name__)

data = pandas.read_excel("employee.xlsx")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/email', methods=["GET", "POST"])
def getmail():
    if request.method == "POST":
        req = request.form
        print(req)
        email = req.get('email')

        emprecord = data.loc[data['Email ID'] == email]

        print(emprecord)

        if emprecord.empty:
            return render_template("invalidemail.html")

        else:
            otp = sendmail(email)
            details[email] = otp
            return render_template("validate.html", email= email)            

        print(otp)

    return render_template("validate.html", email = email)

@app.route('/validate', methods=["POST"])
def validate():
    val = request.form
    key = val.get('email')
    res = val.get('otp')
    print(details[key])
    print(res)
    if details[key] == int(res):
        voucher = data.loc[data['Email ID'] == key, "voucher Code"].tolist()
        print(voucher[0])
        return render_template("voucher.html", voucher = voucher[0])

    print(val)
    return render_template('invalidotp.html', email = key)


def sendmail(email):
    otp = secretsgen.randrange(100000,999999)
    server.login("swparotpforrandomtestsmtp@gmail.com", "Welcome@123")
    server.sendmail(
               "swparotpforrandomtestsmtp@gmail.com", 
               email, 
               msg.format(str(otp)))
    server.quit()
    return otp

if __name__ == "__main__":
    app.run(debug=True)