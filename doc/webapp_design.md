# NACCBIS Web Application Design Document

This living document explains the architectural and design choices made
during the development of the web application.  

## Models

Abstract base classes will be used for combining common database fields from multiple database tables, e.g. offensive tables that have fields in common.

Here's an example of abstract base classes from the [Django documentation](https://docs.djangoproject.com/en/2.1/topics/db/models/#abstract-base-classes):

```
from django.db import models

class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True

class Student(CommonInfo):
    home_group = models.CharField(max_length=5)
```

---

## Urls


---
## Leaderboards

How should we handle sorting a table by a stat?
 - Should probably be handled by the server
