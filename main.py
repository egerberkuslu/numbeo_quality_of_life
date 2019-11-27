from selenium import webdriver
import time
import json
driver_path = "C:/Users/ege/Desktop/chromedriver.exe"
browser = webdriver.Chrome(executable_path=driver_path)

browser.get("https://www.numbeo.com/quality-of-life/")

all_countries = browser.find_elements_by_xpath('//*[@id="country"]')


object = {
    'countries' : [],
}
temp = []
for i in all_countries:
    temp.append(i.text)
temp = str(temp[0]).strip().split('\n') #tüm ülkeleri aldırdı
temp.pop(0) #select countryi kısmını boşalttı.
all_countries = []
for i in temp:
    all_countries.append(i.strip().replace(' ','+')) #stripli halini attı
counter_for_country = -1

for country in all_countries: # şuan elimde all_countries düzgün bir şekilde var !
    counter_for_country = counter_for_country +1

    object['countries'].append({
        'name': country,
        'cities': [],
    })
    browser.get("https://www.numbeo.com/quality-of-life/country_result.jsp?country=" + country)
    all_cities_in_country = browser.find_elements_by_xpath('//*[@id="city"]')
    temp = []
    for i in  all_cities_in_country:
        temp.append(i.text)
    temp = str(temp[0]).strip().split('\n')  # tüm cityleri aldırdı
    temp.pop(0)  # select city kısmını boşalttı.
    all_cities_in_country = []
    for i in temp:
        i = i.strip()
        if ' ' in i:
            array = i.split(' ')
            i = ''
            for x in array:
                x = str(x).capitalize()
                i = i + x + " "
            i = i.strip().replace(' ','-')
        if ',' in i:
            array = i.split(',')
            for x in array:
                x = str(x).strip().capitalize()
                i = i + x + " "
            i = i.strip().replace(' ','-')
        all_cities_in_country.append(i.strip())  # stripli halini attı
    counter_for_city = -1

    for city in all_cities_in_country:
        counter_for_city =  counter_for_city + 1
        if "+" in country:
           country = country.replace('+', '-')
        if "'" in city:
            city = city.replace("'","%27")
        print("*"*100)
        print("CITY ==> ",city,"COUNTRY ==> ",country)
        try:
            link = "https://www.numbeo.com/quality-of-life/in/" + city
            if "St.-John%27s" in city and "Antigua-And-Barbuda" in country:
                link = "https://www.numbeo.com/quality-of-life/in/St-John%27s-Antigua-And-Barbuda"
            browser.get(link)
            if "Cannot find city id for" in browser.find_element_by_xpath('/html/body/div/h1').text: # yanlış link geldi
                print("yanlış link")
                link = "https://www.numbeo.com/quality-of-life/in/" + city+ "-" + country
                print("link düzeldi")
                print(link)
                browser.get(link)
            elif "Quality of Life in" in browser.find_element_by_xpath('/html/body/div/h1').text:
                print("link doğru")
                print(link)

            try:
                    table = browser.find_elements_by_xpath('/html/body/div/table')
                    object['countries'][counter_for_country]['cities'].append({
                        'name':city,
                         'all_specs': []
                    })
                    if table:
                        for row_counter in range(1,11):
                                if row_counter != 9:
                                    spec = str(browser.find_element_by_xpath('/html/body/div[1]/table[1]/tbody/tr['+str(row_counter)+']/td[1]').text).strip().replace("ƒ","").replace(':','').strip()
                                    value =str(browser.find_element_by_xpath('/html/body/div[1]/table[1]/tbody/tr['+str(row_counter)+']/td[2]').text).strip()
                                    quality = str(browser.find_element_by_xpath('/html/body/div[1]/table[1]/tbody/tr['+str(row_counter)+']/td[3]').text).strip()
                                    if "?" == value or value == "":
                                        value = None
                                    if '?' == quality or quality == '':
                                        quality = None
                                    object['countries'][counter_for_country]['cities'][counter_for_city]['all_specs'].append({
                                        'spec':spec,
                                        'value':value,
                                        'quality':quality
                                    })

                                    print("SPEC = ", spec, " | ", "VALUE = ", value, " | ", "Quality = ", quality)

                    else:
                        print("NO DATA")
                        constant_specs = ['Purchasing Power Index','Safety Index','Health Care Index','Climate Index','Cost of Living Index','Property Price to Income Ratio','Traffic Commute Time Index'
                                        'Pollution Index','Quality of Life Index']
                        for const_spec in  constant_specs:
                            object['countries'][counter_for_country]['cities'][counter_for_city]['all_specs'].append({
                                'spec':const_spec,
                                'value':None,
                                'quality':None
                            })

            except:
                print("table is not exist")
                constant_specs = ['Purchasing Power Index', 'Safety Index', 'Health Care Index', 'Climate Index',
                                  'Cost of Living Index', 'Property Price to Income Ratio', 'Traffic Commute Time Index'
                                                                                            'Pollution Index',
                                  'Quality of Life Index']
                for const_spec in constant_specs:
                    object['countries'][counter_for_country]['cities'][counter_for_city]['all_specs'].append({
                        'spec': const_spec,
                        'value': None,
                        'quality': None
                    })
        except:
            print("something wrong")
    if counter_for_country == 3:
        with open('output.json', 'w') as outfile:
            json.dump(object, outfile)
        break
