from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from boards.forms import NewTopicForm
from boards.models import Board, Post, Topic

from boards.views import board_topics, home, new_topic

# Create your tests here.

class HomeTests(TransactionTestCase):
    
    reset_sequences = True
    
    def setUp(self) -> None:
        Board.objects.create(name='Django', description='Django board.')
        url = reverse('home')
        self.response = self.client.get(url)

    # comprobar que es accesible la pagina principal
    def test_home_view_status_code(self):
        #url = reverse('home')
        #response = self.client.get(url)
        #self.assertEquals(response.status_code, 200)
        self.assertEquals(self.response.status_code,200)

    # comprobar que la función que resuelve / es la función home
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    # la pagina home debe contener un link al topic
    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))

class BoardTopicTests(TransactionTestCase):

    reset_sequences = True

    def setUp(self) -> None:
        Board.objects.create(name='Django', description='Foro Django')

    #cuando existe el topic retorna un 200
    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})    #resolver url empleando el name así no esta dependiente de donde lo implmentamos
        response = self.client.get(url)
        #print('pk creada para board valor:{0}'.format(self.board_pk))
        self.assertEquals(response.status_code, 200)

    # cuando no existe el topics retorna un 404
    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    # asegurar que existe función board_topics para resolver 
    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})

        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))


class NewTopicTests(TransactionTestCase):

    reset_sequences = True

    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        User.objects.create_user(username='john', email='john@doe.com', password='123') 

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    # CHEQUEOS CON USUARIO

    # Debe contener el token de seguridad
    def test_csrf(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    # se crea el Topic y el Post
    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    
    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    # PRUEBAS DE FORMS
    def test_contains_form(self):  # <- new test
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_invalid_post_data(self):  # <- updated this one
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)