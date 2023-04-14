from django.db import models

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
# Create your models here.
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class snippets(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    code = models.TextField()
    lineous = models.BooleanField(default=False)
    language = models.CharField(default='python', max_length=100, choices=LANGUAGE_CHOICES)
    style = models.CharField(default='friendly', max_length=100, choices=STYLE_CHOICES)
    
    # updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created']
    owner=models.ForeignKey('auth.user', related_name='snippets',on_delete=models.CASCADE)
    heighighted=models.TextField()
    def save(self, *args, **kwargs):
        """
        Use the pygements library to create a Heghighted HTML representation of the Code snippet
        """
        lexer=get_all_lexers(self.language)
        lineous='table' if self.lineous else False
        options={'title':self.title} if self.title else {}
        formatter=HtmlFormatter(style=self.style,linenos=lineous,full=True,**options)
        self.highlighted = highlight(self.highlight)
        super().save(*args, **kwargs)

