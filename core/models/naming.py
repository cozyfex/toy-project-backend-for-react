from django.db import models


class Naming(models.Model):
    class Meta:
        db_table = 'naming'

    id = models.BigAutoField(primary_key=True, verbose_name='Naming Id')
    title = models.CharField(max_length=255, unique=True, verbose_name="Naming Title")
    like = models.IntegerField(default=0, verbose_name='Like')
    visit = models.IntegerField(default=0, verbose_name='Visit')
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='Register Date')
    mod_date = models.DateTimeField(auto_now_add=True, verbose_name='Modify Date')

    def __str__(self):
        return self.title
