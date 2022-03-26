from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import re

class IpassCard:
    def __init__(self, options=None):
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('https://www.i-pass.com.tw/Inquire')

    def run(self):
        self.card_id_input()
        self.record_range()
        self.id_last4code()
        self.search_click()
        self.wait_for_robot_check()
        self.rows_count_select()
        self.record_data()
        self.driver.close()

    def card_id_input(self):
        id_input = self.driver.find_element_by_id('CardId')
        card_id = input('please input Ipass id: ')
        id_input.send_keys(card_id)

    def record_range(self):
        range = self.driver.find_element_by_id('gridRadios3')
        range.click()

    def id_last4code(self):
        code_ = self.driver.find_element_by_id('IDL4')
        id_l4 = input('please input last 4 code of your ID: ')
        code_.send_keys(id_l4)
    
    def search_click(self):
        button = self.driver.find_element_by_class_name('postmed-btn')
        button.click()

    def wait_for_robot_check(self):
        input('press Enter when done with rocot check...')

    def rows_count_select(self):
        count = self.driver.find_element_by_xpath('//*[@id="PrintFriendlyArea"]/p[1]')
        self.count = count.text
        c = int(re.search('共 (\d+) 筆', self.count).group(1))
        if c > 10:
            select = Select(self.driver.find_element_by_id('paginate_count_of_page2'))
            select.select_by_visible_text('100')

    def record_data(self):
        rows = self.driver.find_element_by_id('Searchresult')
        print(self.count)
        print(rows.text)


if __name__ == '__main__':
    options=Options()
    options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    card = IpassCard(options)
    card.run()