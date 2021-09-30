import smtplib as smtp

server = smtp.SMTP_SSL(host="smtp.gmail.com",port=465)
server.login("xxxxxxx@gmail.com",input("password"))
server.sendmail("xxxxxxxx@gmail.com", "xxxxxxx@hotmail.com", "Hola como estas")
server.quit()
