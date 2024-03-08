import requests
import urllib.request
import json
from bs4 import BeautifulSoup


def get_info(make=None, model=None, fuel=None, drive=None, year=None, min_mpg=None, price_max=None, price_min=None,  milage_high=None, milage_low=None,limit=5):
    """
    This function makes sure that we can find the make and model of a specific car to pass into the web scrapper to get more information
    """
    api_url = "https://api.api-ninjas.com/v1/cars?"
    if make:
        api_url += f"&make={make}"
    if model:
        api_url += f"&model={model}"
    if fuel:
        api_url += f"&fuel={fuel}"
    if year:
        api_url += f"&year={year}"
    if drive:
        api_url += f"&drive={drive}"
    if min_mpg:
        api_url += f"&min_mpg={min_mpg}"

    if api_url == "https://api.api-ninjas.com/v1/cars?":
        print("Invalid parameters")
        return 
    
    response = requests.get(api_url, headers={'X-Api-Key': 'yRJd6XVFaGA4Uq6N97xnmA==8wQXpzLdseHdo1uq'})
    if response.status_code == requests.codes.ok and response.text != '[]':
        data = json.loads(response.text)
        if not make:
            for i in range(1):
                make = data[i]["make"]
        
    model = model.replace(' ', "-")
    return (make.lower(), model.lower(), fuel, drive.upper(), year, min_mpg, price_max, price_min, milage_high, milage_low)
    
    
def scrape(make=None, model=None, fuel=None, drive=None, year=None, min_mpg=None, price_max=None, price_min=None, milage_high=None, milage_low=None):
    """
    This function calls the web scrapper to get the average price of a specific make and mode of a car depending on parameters that the user passes in
    """
    
    url_to_scrape = "https://www.truecar.com/used-cars-for-sale/listings/"
    if make:
        url_to_scrape += f"{make}/"
    if model:  
        url_to_scrape += f"{model}/"

    if price_max and price_min:
        url_to_scrape += f"price-{price_min}-{price_max}/"
    elif price_min:
        url_to_scrape += f"price-above-{price_min}/"
    elif price_max:
        url_to_scrape += f"price-below-{price_max}/"
        
    if milage_high and milage_low:
        url_to_scrape += f"?milageHigh={milage_high}&milageLow={milage_low}"
    elif milage_high:
        url_to_scrape += f"?milageHigh={milage_high}"
    elif milage_low:
        url_to_scrape += f"?milageLow={milage_low}"
        
    if drive:
        url_to_scrape += f"?driveTrain[]={drive}"
    print(url_to_scrape)
    
    
    to_scrape = requests.get(f"https://www.truecar.com/used-cars-for-sale/listings/{make}/{model}/")
    soup = BeautifulSoup(to_scrape.text, "html.parser")
    quotes = soup.findAll("span", attrs={"data-test":"vehicleCardPriceLabelAmount"})
    temp = []
    for q in quotes:
        thing = q.text.strip("$")
        thing2 = thing.replace(",","")
        temp.append(int(thing2))
    avg = sum(temp) / len(temp)
    print(avg)



def main():
    print("------------------------")
    print("Please enter the following parameters.")
    make = input("Make: ") #
    model = input("Model: ") #
    fuel = input("Fuel: ") #
    drive = input("Drive: ")
    year = input("Year: ")
    min_mpg = input("Min MPG: ")
    price_max = input("Max Price: ")
    price_min = input("Min Price: ")
    milage_high = input("High Milage: ")
    milage_low = input("Low Milage: ")

    print(get_info(make, model, fuel, drive, year, min_mpg, price_max, price_min, milage_high, milage_low))
    
    make, model, fuel, drive, year, min_mpg, price_max, price_min, milage_high, milage_low = get_info(make, model, fuel, drive, year, min_mpg, price_max, price_min, milage_high, milage_low)
    
    print(scrape(make.lower(), model.lower(), fuel, drive.upper(), year, min_mpg, price_max, price_min, milage_high, milage_low))
    
    print("------------------------")

if __name__ == "__main__":
    main()