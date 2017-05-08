# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class CurrencyApp(models.Model):
	text=models.TextField(blank=True, null=True)
	
	def __str__(self):
		return self.text