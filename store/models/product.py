from django.db import models 
from .category import Category 
# from django_json_editor import JSONEditorWidget


class Product(models.Model): 
	name = models.CharField(max_length=60) 
	price = models.IntegerField(default=0) 
	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1) 
	description = models.CharField( 
		max_length=250, default='', blank=True, null=True) 
	image = models.ImageField(upload_to='uploads/products/')
	attributes = models.JSONField(default=dict)

	@staticmethod
	def get_product_by_id(ids): 
		return Products.objects.filter(id__in=ids) 

	@staticmethod
	def get_all_products(): 
		return Products.objects.all() 

	@staticmethod
	def get_all_products_by_categoryid(category_id): 
		if category_id: 
			return Products.objects.filter(category=category_id) 
		else: 
			return Products.get_all_products() 

	def __str__(self): 
		return self.name 