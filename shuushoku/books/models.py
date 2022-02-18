from django.db import models

# Create your models here.
class Book(models.Model):
    # bookid : INTEGER型で、主キー
    bookid = models.IntegerField(primary_key=True)
    # 書名 : 文字列100桁
    title = models.CharField(max_length=100)
    # 著者 : 文字列30桁
    author = models.CharField(max_length=30)
