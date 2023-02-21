from django.db import models


class NamingWord(models.Model):
    class Meta:
        db_table = 'naming_word'

    id = models.BigAutoField(primary_key=True, verbose_name='Naming Word Id')
    naming_id = models.ForeignKey('Naming', on_delete=models.CASCADE, verbose_name='Naming Id')
    word = models.CharField(max_length=255, unique=True, verbose_name="Naming Word Title")
    sort = models.IntegerField(default=0, verbose_name='Sort')
    depth = models.IntegerField(default=0, verbose_name='Depth')
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='Register Date')
    mod_date = models.DateTimeField(auto_now_add=True, verbose_name='Modify Date')

    def __str__(self):
        return self.word
