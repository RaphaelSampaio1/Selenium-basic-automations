from pathlib import Path
import os

from dotenv import load_dotenv

from challenge import challengeSite

# Collecting credentials
ENV_PATH = Path(__file__).resolve().parent / "data" / ".env"
load_dotenv(dotenv_path=ENV_PATH)
EMAIL = os.getenv("EMAIL", "").strip()
PASSW = os.getenv("PASSW", "").strip()

if not EMAIL or not PASSW:
    raise RuntimeError(
        "Missing environment variables. Create a .env file in the project folder with:\n"
        "EMAIL=your_email@example.com\nPASSW=your_password"
    )

# Initializing
bot = challengeSite()
SITE = "https://sampaiodev-rpa-desafios.vercel.app/"
CSV_PATH=r"data\database.csv"
FILE_PATH= r"data\teste.txt"


if __name__ == "__main__":
    bot.initialize_driver(site=SITE)
    bot.challenge1(email=EMAIL, passw=PASSW)
    bot.challenge2(csv_path=CSV_PATH)

    movies= ["Acao","Comedia","Drama","Terror","Ficção" ,"Documentario"]
    for i in movies:
        bot.challenge3(movie_type=i)

    bot.challenge4(file_path=FILE_PATH)

    bot.webscraping()

    


    #input("xx")
