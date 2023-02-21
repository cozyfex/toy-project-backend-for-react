from django.db import models


class DefaultNamingWord(models.Model):
    class Meta:
        db_table = 'default_naming_word'

    id = models.BigAutoField(primary_key=True, verbose_name='Default Naming Word Id')
    word = models.CharField(max_length=255, unique=True, verbose_name="Default Naming Word Title")
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='Register Date')
    mod_date = models.DateTimeField(auto_now_add=True, verbose_name='Modify Date')

    def __str__(self):
        return self.word
