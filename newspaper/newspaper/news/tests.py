# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from newspaper.news.models import News


class NewsTestCase(TestCase):

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

    def test_newslist(self):
        news = News.objects.create(title='Mi noticia test',
                                   description='Mi descripcion test',
                                   publish_date=datetime.now())
        response = self.client.get(reverse('news_list'))
        self.assertEquals(response.status_code, 200)
        self.assertIn(news.title, response.content)
        self.assertIn(news.description, response.content)

    def test_news_add(self):
        response = self.client.get(reverse('news_add'))
        self.assertEquals(response.status_code, 200)


class SeleniumTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Chrome()
        super(SeleniumTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(SeleniumTestCase, self).tearDown()

    def test_register(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')
        assert 'Noticias publicadas:' in selenium.page_source
        assert 'Noticias Pendientes de publicar:' in selenium.page_source
        btn_new_news = selenium.find_element_by_id('new_news')
        btn_new_news.send_keys(Keys.RETURN)
        assert ' nueva publicaci' in selenium.page_source
        id_title = selenium.find_element_by_id('id_title')
        id_description = selenium.find_element_by_id('id_description')
        id_publish_date = selenium.find_element_by_id('id_publish_date')
        btn_submit = selenium.find_element_by_id('btn_submit')
        id_title.send_keys('Esto contiene una B b y lanza error')
        id_description.send_keys('Toda la descripcion de la news')
        assert id_publish_date.get_property('value') != ''
        btn_submit.send_keys(Keys.RETURN)
        assert 'El campo titulo no puede contener B' in selenium.page_source
        selenium.get('http://127.0.0.1:8000/news/add/')
        assert ' nueva publicaci' in selenium.page_source
        id_title = selenium.find_element_by_id('id_title')
        id_description = selenium.find_element_by_id('id_description')
        id_publish_date = selenium.find_element_by_id('id_publish_date')
        print id_publish_date.get_attribute('value')
        btn_submit = selenium.find_element_by_id('btn_submit')
        id_title.send_keys('News test selenium')
        id_description.send_keys('Toda la descripcion de la news')
        id_publish_date.get_attribute('value')
        id_publish_date.clear()
        id_publish_date.get_attribute('value')
        id_publish_date.send_keys('01/06/2018 16:25:33')
        id_publish_date.get_attribute('value')
        btn_submit.send_keys(Keys.RETURN)
        assert 'Noticias publicadas:' in selenium.page_source
        assert 'Noticias Pendientes de publicar:' in selenium.page_source
        assert 'News test selenium' in selenium.page_source
