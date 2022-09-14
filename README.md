# RESTFrameworkの雛形

	mkdir プロジェクト名


	pyenv local 3.8.0


	python3 -m venv 環境_venv 


	source 環境_venv/bin/activate


	pip install --upgrade pip 


	pip install Django


	django-admin startproject プロ


### setting.py更新

	LANGUAGE_CODE = 'ja'
	TIME_ZONE = 'Asia/Tokyo' 


	python manage.py startapp アプ


	settings.py INSTALLED_APPS に追加

(/アプリディレクトリ/templates/アプリ名ディレクトリ/index.html　作成)

	mkdir templates
	cd templates
	mkdir アプリ名
	touch index.html 
	
	
	<!DOCTYPE html>
	<html>
	  <head>
		  ここはトップページです。
	  </head>
	  <body>
	  </body>
	</html>

View.py設定

	from django.shortcuts import render 
	def index(request):
		return render(request, 'アプリ/index.html')

(プロジェクトurls.py設定)

	from django.contrib import admin
	from django.urls import path, include

	urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('アプリ.urls')),
	]

アプリディレクトリ内でurls.py設定

	touch urls.py
	
	
	from django.urls import path
	from . import views
	app_name = "アプリ名"
	urlpatterns = [
		path('', views.index, name='index'),
	]
	
	python manage.py makemigrations アプリ名
	python manage.py migrate
	python manage.py runserver
	python manage.py createsuperuser
	
(Adminページの作成)

## manage.pyと同じ階層に、.gitignoreを作成

	*.log
	*.pyc
	__pycache__/
	db-volumes/
	db.sqlite3
	.env

## manage.pyと同じ階層に、.envを作成

	pip install django-environ
	SECRET_KEY=''
	DEBUG=True

## .envをsetting.pyに導入

	import environ
	import os
	env = environ.Env()
	env.read_env('.env')
	SECRET_KEY = env('SECRET_KEY')
	DEBUG = env('DEBUG')

## postgresql
(brew install postgresql)

↓ postgresql 削除方法
https://codenote.net/mac/homebrew/3894.html

	psql —version
	brew services start postgresql
(⚠️brew services stop postgresql　で止める)

(postgresqlを起動)

	createdb データベース名
	psql -l
	pip3 install psycopg2-binary
	env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip3 install psycopg2 

setting.py データベース変更
	import os 

	DATABASES = {
	    'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': 'testDB',
		'USER': 'hogehoge',
		'PASSWORD': 'password',
		'HOST': 'db',
		'PORT': 5432,
	    }
	}

⭐️python manage.py migrate (データベース作成)

# RESTFRAMEWORK「https://office54.net/python/django/web-api-rest」

Templateの説明(必要ないなら、seiarlizedは必要ない)

serializers.pyは主に、上記のForm画面を作成するものである。
1. 投稿されたデータを保存するmodelを作成
2. serializers.pyにて、serializers.ModelSerializerを継承したクラスを定義し、上記のmodelを設定
3. view.pyにて、viewsets.ModelViewSetを継承したクラスを定義し、serializer_class = 2.のクラス(TemplateSerializer)
4. urls.pyにて、
router = routers.DefaultRouter()
router.register('template', views.TemplateViewSet)
path('api/', include(router.urls))を追加する。
Registerされた、名称でPOST画面がひらけて、投稿を行える。


## ① pip install djangorestframework

## ②setting.py
	INSTALLED_APPS = [
	    'rest_framework',
	]
## ③ アプリディレクトリ下でserializers.pyを作成
	from rest_framework import serializers
	from .models import Template

	class TemplateSerializer(serializers.ModelSerializer):
	    class Meta:
		model = Template
		fields = ('template_name', 'category',)

## ④ models.pyに下記をコピペ
	from django.db import models
	class Tempcategory(models.Model):
	    name = models.CharField('カテゴリー', max_length=50)

	def __str__(self):
	return self.name

	class Template(models.Model):
	    template_name = models.CharField(max_length=255, unique=True)
	    category = models.ForeignKey(Tempcategory, on_delete=models.CASCADE, related_name="tempcategory")
	    def __str__(self):
		return self.template_name


## ⑤ view.pyにて
	from django.shortcuts import render 
	from rest_framework import viewsets, filters
	from .models import Template
	from .serializers import TemplateSerializer

	class TemplateViewSet(viewsets.ModelViewSet):
	    queryset = Template.objects.all()
	    serializer_class = TemplateSerializer

	def index(request):
	    return render(request, ‘アプリ名/index.html')


## ⑥urls.py
	from django.contrib import admin
	from django.urls import path, include
	from rest_framework import routers
	from .views import TemplateViewSet
	from . import views
	
	router = routers.DefaultRouter()
	router.register('template', views.TemplateViewSet)

	app_name = “アプリ名”

	urlpatterns = [
	    path('index/', views.index, name='index'),
	    path('api/', include(router.urls)),
	]


## → seiarlizedを用いない場合
view.py

	from django.contrib import admin
	from django.urls import path, include
	from django.shortcuts import render 
	from rest_framework import viewsets, filters
	from rest_framework.views import APIView
	from rest_framework.response import Response
	from rest_framework.decorators import api_view
	from rest_framework import status

	class NonSeializers_Api(APIView):
	    def get(self, request):
		out_dict = {}
		out_dict['message'] = 'get'
		return Response(out_dict, status=status.HTTP_200_OK)
	    def post(self, request):
		out_dict = {}
		out_dict['message'] = 'post'
		return Response(out_dict)



アプリurls.py

	urlpatterns = [
	    path('nonseializers_api/', views.NonSeializers_Api.as_view(), name = "NonSeializers_Api"),
	]
	
	
	python manage.py makemigrations アプリ名
	python manage.py migrate
