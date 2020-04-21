from django.db import models
# from mongoengine import *
# from mongoengine import connect
# connect('qichacha_com', host='10.0.0.120', port=57017)


class Types(models.Model):
    ''' 数据所属类别 '''
    name = models.CharField(max_length=25,null=False,blank=False)

    def __str__(self):
        return self.name

class Counter(models.Model):
    number = models.IntegerField()
    time = models.TimeField(auto_now=True,auto_now_add=False)
    collection = models.CharField(max_length=125,null=False,blank=False)
    name = models.CharField(default=None,max_length=255)
    timestamp = models.DateField(auto_now=True,auto_now_add=False)
    record = models.IntegerField()
    typec = models.ForeignKey(Types,on_delete=models.CASCADE,default=None)

    def get_time_number(self):
        return [self.timestamp.strftime("%m-%d")+' '+self.time.strftime('%H')+":00",self.record]


    def __str__(self):
        return self.name

class SumNum(models.Model):
    ''' 保存当天的总量 '''
    number = models.IntegerField()
    typec  = models.ForeignKey(Types,on_delete=models.CASCADE,default=None)
    date = models.DateField(auto_now=True,auto_now_add=False)



