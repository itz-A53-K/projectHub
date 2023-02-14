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
        ),
    )
    
    proj_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    short_Desc = models.CharField(max_length=500, blank=True)
    full_Desc= models.TextField(blank=True)

    category = models.CharField(max_length=100, choices=CATEGORY)
    
    used_language= models.CharField(max_length=500, null=True, blank=True)

    price= models.FloatField( blank=True, null=True)
    discounted_price = models.FloatField( blank=True , null=True)
    free = models.BooleanField(default=False)

    publish_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    default_image= models.ImageField(null=True,blank=True)

    sourcecode_link= models.CharField(max_length=500,null=True, blank=True)

    def __str__(self):
        return self.title
    
class Proj_image(models.Model):
    id= models.BigAutoField(primary_key=True)
    image= models.ImageField(upload_to="Project_Image")
    proj_id = models.ForeignKey( Project, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.id

class Cart(models.Model):
    cart_id= models.BigAutoField(primary_key=True)
    project= models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id= models.IntegerField()
    price = models.FloatField()
    
class Order(models.Model):
    order_id= models.BigAutoField(primary_key=True)
    project= models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id= models.IntegerField()
    price = models.FloatField()

    order_time = models.DateTimeField(auto_now_add=True)
    
