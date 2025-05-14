from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" type="text/css" href="https://graph.org/file/3e0142ddf19629ac0a685-2f26b719c1f8621167.jpg">
    <titleSudoR2spr Repository</title>
	<link rel="icon" type="image/x-icon" href="https://graph.org/file/7a9c981f314451bd881eb-2c65f757933b5ce9da.jpg">

</head>

<body>
    <div class="container" style="bg-dark text-red text-center py-3 mt-5">
        <a href="https://github.com/nikhilsaini098" class="card">
            <p>
              />▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄<br 
	      />██░▄▄▄░█░▄▄▀█▄░▄██░▀██░█▄░▄██<br 
              />██▄▄▄▀▀█░▀▀░██░███░█░█░██░███<br 
	      />██░▀▀▀░█░██░█▀░▀██░██▄░█▀░▀██<br 
              />▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀<br />
                                             <br>

                <b>v2.0.0</b>
            </p>
        </a>
    </div>
	<br></br><br></br><br></br>
	<footer class="bg-dark text-white text-center py-3 mt-5">
	<center><img loading="lazy" class="object-none object-center" src="https://graph.org/file/7a9c981f314451bd881eb-2c65f757933b5ce9da.jpg" width="240" height="120">
        Powered By SAMURAI 
		<img loading="lazy" class="object-none object-center" src="https://graph.org/file/3e0142ddf19629ac0a685-2f26b719c1f8621167.jpg" width="240" height="120">
		<div class="footer__copyright">
            <p class="footer__copyright-info">
                © 2024 Video Downloader. All rights reserved.
            </p>
        </div>
    </footer></center>
</body>

</html>
"""


if __name__ == "__main__":
    app.run()
