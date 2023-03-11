from django.db import models
import datetime

# Create your models here.

# admin login credentials : Abinash (kjh65%ARt)

class Project(models.Model):
    
    CATEGORY=(
        ('Project', 'Project'),
        ('Template', 'Template'),
    )

    SUB_CATEGORY=(
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
        ),
    )
    
    proj_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    short_Desc = models.CharField(max_length=500, blank=True)

    # Change it to full blog
    full_Desc= models.TextField(blank=True)

    category = models.CharField(max_length=100, choices=CATEGORY)
    sub_category = models.CharField(max_length=100, choices=SUB_CATEGORY)
    
    used_language= models.CharField(max_length=500, null=True, blank=True)
    created_by= models.CharField(max_length=100, null=True, blank=True, default="Team Members")

    price= models.FloatField( blank=True, null=True)
    discounted_price = models.FloatField( blank=True , null=True)
    free = models.BooleanField(default=False)

    publish_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    default_image= models.ImageField(null=True,blank=True, upload_to="Project_Image/")

    sourcecode_link= models.CharField(max_length=500,null=True, blank=True)

    # Need to create a table named "ProjectScreenshot", Where 4 columns are required to be included. 1. ID, 2. projectId, 3. imageLinks, 4. projectTitle

    # If you wish you can change the project description to project blog

    def __str__(self):
        return self.title
    
class Proj_image(models.Model):
    id= models.BigAutoField(primary_key=True)
    image_url= models.ImageField(upload_to="Project_Image/")
    project = models.ForeignKey( Project, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.id

class Cart(models.Model):
    cart_id= models.BigAutoField(primary_key=True)
    project= models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id= models.IntegerField()
    # price = models.FloatField()
    
class Order(models.Model):
    order_id= models.BigAutoField(primary_key=True)
    project= models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id= models.IntegerField()
    price = models.FloatField()
    transaction_id= models.CharField(max_length=300)
    order_time = models.DateTimeField(default=datetime.datetime.now())
    
class User_detail(models.Model):
    id=models.BigAutoField(primary_key=True)
    user_id= models.BigIntegerField()
    name= models.CharField(max_length=200)
    gender= models.CharField(max_length=30, null=True, blank=True)
    phone= models.IntegerField( null=True, blank=True, default="0")
    profileImg= models.ImageField(upload_to="Profile_Image/",null=True, blank=True,  default="/defaultImg/person-circle.png")
    address = models.TextField(null=True, blank=True )
    
    def __str__(self):
        return self.name

