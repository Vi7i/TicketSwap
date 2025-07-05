from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    is_user=models.BooleanField('is_user',default=False)
    is_admin=models.BooleanField('is_admin',default=False)
    location=models.CharField(max_length=255,null=True,blank=True)
    profile=models.ImageField(upload_to="profile/user_profile/")
    phonenumber=models.CharField(max_length=15,default=0,blank=False,null=False)
    
    about=models.TextField(max_length=255,null=True,blank=True)
    def save(self, *args, **kwargs):
        if self.is_superuser and not self.is_admin:
            self.is_admin=True
            self.location=""
        super().save(*args, **kwargs)

class emailverification(models.Model):
    email=models.CharField(max_length=255, null=True, blank=True)
    token=models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.email
    


# class Ticket(models.Model):
#     ticket_name = models.CharField(max_length=100)
#     number_of_tickets = models.IntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     date_of_expiry = models.DateTimeField()
#     type = models.CharField(max_length=20)
#     uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.ticket_name

class Ticket(models.Model):
    ticket_name = models.CharField(max_length=100)
    number_of_tickets = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_expiry = models.DateTimeField()
    type = models.CharField(max_length=20)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ticket_images/', null=True, blank=True)
    def __str__(self):
        return self.ticket_name



class Book(models.Model):
    ticket=models.ForeignKey(Ticket,on_delete=models.CASCADE)
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.IntegerField()
    payment=models.BooleanField(default=0)
    def __str__(self):
        return f'Booked by {self.booked_by.username}'




class Contact(models.Model):
    queries=models.TextField(max_length=90)
    query_by=models.ForeignKey(User, on_delete=models.CASCADE)


class Complaint(models.Model):
    ticket_name= models.CharField(max_length=20)
    uploaded_by=models.CharField(max_length=20)
    complaint_by= models.CharField(max_length=20)
    ticket_price= models.CharField(max_length=20)
    actual_price= models.CharField(max_length=20)
