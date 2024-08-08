from flask import Flask, request
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

@app.route("/api/stock/<string:symbol>", methods=["GET"])
def get_stock_data(symbol):
    option = request.args.get("option")  # Seçilen seçeneği al
    try:
        print(f"Received symbol: {symbol}, option: {option}")
        stock = yf.Ticker(symbol + ".IS")  # BIST için .IS ekleyin
        print(f"Ticker created: {stock}")

        # Farklı dönemler için tarihsel verileri almak
        periods = {
            "1d": "1d",
            "1mo": "1mo",
            "3mo": "3mo",
            "6mo": "6mo",
            "1y": "1y"
        }

        if option == "1d":  # Anlık fiyat
            data = stock.history(period="1d")
            price = data['Close'].iloc[0]  # Anlık fiyatı al
            return f"Anlık fiyat: {price}"

        elif option in periods:  # Diğer dönem seçenekleri
            data = stock.history(period=periods[option])
            prices = data['Close'].to_dict()
            prices_str = "\n".join([f"{date.date()}: " + "\t\t" + str(price) for date, price in prices.items()])  # İki tab ekledik

            # Başlıkları belirle
            title_mapping = {
                "1mo": "1 Aylık Kapanış Fiyatları:",
                "3mo": "3 Aylık Kapanış Fiyatları:",
                "6mo": "6 Aylık Kapanış Fiyatları:",
                "1y": "1 Yıllık Kapanış Fiyatları:"
            }
            title = title_mapping.get(option, "Kapanış Fiyatları:")
            return f"{title}\n{prices_str}"  # Dönem bilgisi ile birlikte döndür

        elif option == "info":  # Hisse Senedi Bilgileri
            info = stock.info
            
            # Türkçe anahtar isimleri ile bilgileri listele
            translated_info = {
                "symbol": "Sembol",
                "shortName": "Kısa İsim",
                "longName": "Uzun İsim",
                "address1": "Adres 1",
                "address2": "Adres 2",
                "city": "Şehir",
                "state": "Eyalet",
                "country": "Ülke",
                "zip": "Posta Kodu",
                "phone": "Telefon",
                "website": "Web Sitesi",
                "sector": "Sektör",
                "industry": "Sanayi",
                "marketCap": "Piyasa Değeri",
                "dividendYield": "Temettü Verimi",
            }
            
            info_str = "\n".join([f"{translated_info.get(key, key)}: {value}" for key, value in info.items() if key in translated_info])
            return f"Hisse Senedi Bilgileri:\n{info_str}"

        else:
            return "Geçersiz seçenek", 400

    except Exception as e:
        print(f"Error: {e}")
        return str(e), 400

if __name__ == "__main__":
    app.run(debug=True)
