from django.test import TestCase
from sign.models import Event,Guest
from django.test import Client
from django.contrib.auth.models import User

# Create your tests here.

class MdelTest(TestCase):
    Event.objects.create(id=1,name ='oneplus 3 event',status=True,limit=2000,address='shenzhen',start_time='2016-08-31 02:18:22')
    Guest.objects.create(id=1, event_id=1, realname='alen',phone='13711001101', email='alen@mail.com', sign=False)

    def test_event_models(self):
        result = Event.objects.get(name='oneplus 3 event')
        self.assertEquals(result.address,'shenzhen')
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='13711001101')
        self.assertEquals(result.realname,'alen')
        self.assertFalse(result.sign)

class IndexPageTest(TestCase):
    '''测试登录首页'''
    def test_index_page_renders_index_templates(self):
        '''测试index视图'''
        response = self.client.get('/')
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')

class LoginActionTest(TestCase):
    '''测试登录函数'''
    def setUp(self):
        User.objects.create_user('admin','1756033641@qq.com','admin12345')
        self.c = Client()

    def test_login_action_username_password_null(self):
        '''用户民密码为空'''
        test_data = {'username':'','password':''}
        resopnse = self.c.post('/login_action/',data = test_data)
        self.assertEquals(resopnse.status_code,200)
        self.assertIn(b"username or password error",resopnse.content)

    def test_login_action_username_passwors_error(self):
        '''用户名密码错误'''
        test_data = {'username':'123',"password":'123'}
        response= self.c.post('/login_action/',data=test_data)
        self.assertEquals(response.status_code,200)
        self.assertIn(b"username or password error",response.content)

    def test_login_aciton_success(self):
        '''登录成功'''
        test_data = {'username':'admin','password':'admin12345'}
        response = self.c.post('/login_action/',data=test_data)
        self.assertEquals(response.status_code,302)
