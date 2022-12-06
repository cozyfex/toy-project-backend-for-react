from django.db import models


class BaseBoard(models.Model):
    class Meta:
        db_table = 'base_board'

    id = models.BigAutoField(primary_key=True, verbose_name='Board Id')
    title = models.CharField(max_length=255, null=False, verbose_name='Board Title')
    name = models.CharField(max_length=255, null=False, verbose_name='Board Author')
    content = models.TextField(null=True, verbose_name='Board Content')
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='Register Date')
    mod_date = models.DateTimeField(auto_now_add=True, verbose_name='Modify Date')
