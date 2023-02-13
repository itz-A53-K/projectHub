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
                ('C#','C#'),
            )
        ),
        ('Android Development', (
                ('Java', 'Java'),
                ('kotlin', 'Kotlin'),
            )
        ),
        ('Cyber Security', 'Cyber Security'),
        ('Others', (
                ('C','C'),
                ('C++','C++'),
                ('Python','Python')
            )
        )
    )
    
    proj_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    short_Desc = models.CharField(max_length=500, blank=True)

    # Change it to full blog
    full_Desc= models.TextField(blank=True)

    category = models.CharField(max_length=100, choices=CATEGORY)
    
    used_language= models.CharField(max_length=500, null=True, blank=True)

    price= models.FloatField(default="Free")
    discounted_price = models.FloatField(default="Free", blank=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    images= models.CharField(max_length=500, null=True,blank=True)

    sourcecode_link= models.CharField(max_length=500,null=True, blank=True)

    # Need to create a table named "ProjectScreenshot", Where 4 columns are required to be included. 1. ID, 2. projectId, 3. imageLinks, 4. projectTitle

    # If you wish you can change the project description to project blog

    def __str__(self):
        return self.title
    



    
