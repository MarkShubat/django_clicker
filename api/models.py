from django.db import models
from django.contrib.auth.models import User
from random import random

# Create your models here.
class MainCycle(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE, default=0)
    click_count = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)
    auto_click_power = models.IntegerField(default=0)
    level = models.IntegerField(default=0)

    def click(self):
        self.click_count += self.click_power
    
    def is_level_up(self):
        if self.click_count > self.count_level_price():
            self.level += 1

            if self.level % 10 == 0:
                return 3
            if self.level % 3 == 0:
                return 2
            return 1
        return False

    def count_level_price(self):

        return (self.level**2+1)*100


class Boost(models.Model):
    mainCycle = models.ForeignKey(MainCycle, null=False, on_delete=models.CASCADE)
    power = models.IntegerField(default=1)
    price = models.IntegerField(default=10)
    level = models.IntegerField(default=0)
    boost_type = models.IntegerField(default=0)

    def update(self):
        if self.price > self.mainCycle.click_count:
            return False

        self.mainCycle.click_count -= self.price

        self.level += 1
        self.power *= 5 
        self.price *= 2


        if self.boost_type == 1:
            self.mainCycle.auto_click_power += self.power
            self.price *= 5
        elif self.boost_type == 0:
            self.mainCycle.click_power += self.power
            self.price *= 3
        elif self.boost_type == 2:
            self.mainCycle.click_count = 666
            self.mainCycle.click_power = 666
            self.mainCycle.auto_click_power = 666



        self.mainCycle.save()

        return self.mainCycle
