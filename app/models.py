from django.db import models
from django.utils import timezone
#password=1234



class UserTable(models.Model):
	user_id=models.AutoField(primary_key=True)
	dp=models.FileField(null=True,blank=True)
	email=models.CharField(max_length=50,null=False)
	name=models.CharField(max_length=100)
	def __str__(self):
		return self.name

class PostTable(models.Model):
	post_id=models.AutoField(primary_key=True)
	user_id=models.ForeignKey(UserTable, on_delete=models.CASCADE)
	topic=models.CharField(max_length=50)
	link=models.CharField(max_length=350)
	content=models.CharField(max_length=250)
	category=models.CharField(max_length=25)
	created_at = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.category

class ContactTable(models.Model):
	email=models.CharField(max_length=20)
	statement=models.CharField(max_length=100)
	def __str__(self):
		return self.statement
