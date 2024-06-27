import time
import random

from selenium import webdriver

from page_parser import get_data, get_art_page, start_parser
from excel_controller import ExcelController


def save_current_row(row):
    with open("current_row.txt", "w") as f:
        f.write(str(row))

def get_current_row():
    with open("current_row.txt") as f:
        return int(f.read())


def main():
    driver: webdriver.Chrome = start_parser()

    excelController = ExcelController("Agco.xlsx", get_current_row())
    max_row = excelController.max_row

    # Iterate arts by rows parse data of this arts and update the document
    while excelController.row <= max_row:
        art = str(excelController.sheet[f"A{excelController.row}"].value).replace("-", "").replace(",", "")
        print(excelController.row, art)

        get_art_page(driver=driver, art=art)

        time.sleep(random.randint(3, 5))

        data: dict = get_data(driver=driver, art=art)
        
        excelController.sheet[f"B{excelController.row}"] = data["marks"]
        excelController.sheet[f"C{excelController.row}"] = data["models"]
        excelController.sheet[f"D{excelController.row}"] = "" if data["img"] else "Пусто"

        excelController.save_document()

        excelController.row += 1

        save_current_row(excelController.row)

        time.sleep(random.randint(3, 5))

if __name__ == "__main__":
    main()




