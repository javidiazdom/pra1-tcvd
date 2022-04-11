from scrapper import FilmDataScrapper 

output = "dataset.csv"
scrapper = FilmDataScrapper()
scrapper.scrape()
scrapper.dataToCsv(output)