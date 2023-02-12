from django.db import models

# Create your models here.

# admin login credentials : Abinash (kjh65%ARt)

class Project(models.Model):
    CATEGORY=(
        ('Web Development', (
                ('Front-end Development', 'Front-end Development'),
                ('JavaScript', 'JavaScript'),
                ('AJAX', 'AJAX'),
                ('Node Js', 'Node Js'),
                ('React Js', 'React Js'),
                ('Angular Js', 'Angular Js'),
                ('Django', 'Django'),
                ('PHP', 'PHP'),
            )
        ),
        ('Android Development', (
                ('Java', 'Java'),
                ('kotlin', 'Kotlin')
            )
        ),
        ('Cyber Security', 'Cyber Security'),
        ('Others', (
                ('C','C'),
                ('C++','C++'),
                ('C#','C#'),
                ('Python','Python')
            )
        )
    )
    
    proj_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    shortDesc = models.CharField(max_length=500, blank=True)
    fullDesc= models.TextField(blank=True)

    category = models.CharField(max_length=100, choices=CATEGORY)
    
    used_language= models.CharField(max_length=500, null=True, blank=True)

    price= models.FloatField(default="Free")
    discounted_price = models.FloatField(default="Free", blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)

    images= models.CharField(max_length=500, null=True,blank=True)

    sourcecode_link= models.CharField(max_length=500,null=True, blank=True)

    def __str__(self):
        return self.title
    



    
