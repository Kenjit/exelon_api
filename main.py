import Scraper,os

def main():
    breakdown = Scraper.scraper()
    print(breakdown)
    os.chdir("C:\\Users\\ktsuchiy\\Desktop")
    breakdown.to_csv("breakdown_3.csv")


if __name__ == "__main__":
    main()