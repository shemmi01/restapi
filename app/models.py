from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=200)


class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=300)



class Student(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=20)
    address = models.TextField(null=True, blank=True)
    father_name = models.CharField(max_length=200)


class ExcelFileUpload(models.Model):
    excel_file_upload= models.FileField(upload_to="excel")


