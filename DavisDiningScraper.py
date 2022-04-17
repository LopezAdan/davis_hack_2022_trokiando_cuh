import enum
import sys
import os
import asyncio
from pyppeteer import launch
from datetime import date
import calendar
import json

def get_today(): 
    curr_date = date.today()
    return calendar.day_name[curr_date.weekday()]

async def pressTab(page, num):
    """ Used to navigate around the page just cause i'm too 
    lazy to actually find stuff in a fancy way"""
    for i in range(num): 
        await page.keyboard.press('Tab')


async def main():
    """ Opens a chromium browser, visits each dining hall menu, and scrapes each food item
         and places it in a JSON file"""
    browser = await launch(headless=True, args=["--window-position=0,0"] )
    page = await browser.newPage()
    await page.setJavaScriptEnabled(False)
    url = 'https://housing.ucdavis.edu/dining/menus/dining-commons/'
    dining_commons = {
        "cuarto": {}, 
        "segundo": {},
        "tercero": {}, 
        "latitude": {}
        }

    day = get_today()
    for dining_hall in dining_commons: 
        print("Gathering data on dining hall: ", dining_hall)
        await page.goto(url + dining_hall)
        possible =  await page.Jx(f"//a[contains(., '{day}')]")
        href = await page.evaluate('(element) => element.getAttribute("href")', possible[0])
        matching_div = await page.J(f"{href}")
        inner_divs = await matching_div.JJ(":scope > div") 
        for div in inner_divs: 
            if await page.evaluate('(element) => element.getAttribute("class")', div) != "filter-menu-options":
                
                # Get Type of food: 
                title = await div.JJ(":scope > h4")
                if title: 
                    title = await page.evaluate('(element) => element.textContent', title[0])
                dining_commons[dining_hall][title] = {}
                
                foods = await div.JJ(":scope > ul")

                for i, food in enumerate(foods): 
                    items = await food.JJ(":scope > li")
                    for item in items: 
                        
                        #Get name of food
                        item_name = await item.JJ(":scope > span")
                        if item_name: 
                            item_name = await page.evaluate('(element) => element.textContent', item_name[0])
                            dining_commons[dining_hall][title][item_name] = {}

                        #Get nutrition info 
                        nutrition =  await item.JJ(":scope > ul")
                        nutrition = nutrition[0] if isinstance(nutrition, list) else nutrition
                        nutrition = await nutrition.JJ(":scope > li")
                        nutrition = nutrition[0] if isinstance(nutrition, list) else nutrition

                        nutrition_div = await nutrition.JJ(":scope > div")
                        headers = ["description"]
                        for i, d in enumerate(nutrition_div): 
                            
                            info =  [await page.evaluate('(element) => element.textContent', p) for p in await d.JJ(":scope > p")]
                            headers = [await page.evaluate('(element) => element.textContent', h) for h in await d.JJ(":scope > h6")]

                            #Because first iteration on div only gets the description
                            if i == 0: 
                                headers = ["description"]

                            if info and headers: 
                                for h, p in zip(headers, info):
                                    dining_commons[dining_hall][title][item_name][h] = p
  

    with open('app.json', 'w') as fp:
        json.dump(dining_commons, fp, indent=4)

 

asyncio.get_event_loop().run_until_complete(main())