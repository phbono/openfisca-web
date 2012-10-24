'''
Created on Aug 3, 2012

@author: Utilisateur
'''


from simulation.lanceur import Simu
 
from core.utils import Scenario, OutNode
from numpy import count_nonzero

from django.db import models
from django.contrib import admin
from django.forms import ModelForm

# from https://code.djangoproject.com/wiki/DynamicModels

def create_model(name, fields=None, app_label='', module='', options=None, admin_opts=None):
    """
    Create specified model
    """
    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)

    # Create an Admin class if admin options were provided
    if admin_opts is not None:
        class Admin(admin.ModelAdmin):
            pass
        for key, value in admin_opts:
            setattr(Admin, key, value)
        admin.site.register(model, Admin)

    return model




#    def create_model(self, model_name):
#        fields = {}
#        for field in self.create_fields_dict().keys():
#            print field
#            fields[field] = models.FloatField()
#            options = {}
#            admin_opts = {}
#        self.model = create_model(model_name, fields,
#                            options= options,
#                            admin_opts=admin_opts,
#                            app_label='simulation',
#                            module='simulation.no_models'
#                            )
#        
#        class TempForm(ModelForm):
#            class Meta:
#                model = self.model
#        
#        print self.create_fields_dict()
#        form = TempForm(data=self.create_fields_dict()) 
#        print 'is valid :' , form.is_valid() 
#        form.save()



scenario = Scenario()
simu = Simu(scenario=scenario)
simu.build()
cht = simu.waterfall_chart()
print cht

from simulation.utils import MyNode
from simulation.models import Node

#x = MyNode()
#x.init_from_OutNode(simu.data_courant)
#x.remove_null_children()
#print x.code, x.vals, x.is_null
#print x
#d =  x.create_fields_dict()












from chartit import DataPool, Chart


openfisca_data = DataPool(
       series=
        [{'options': {
            'source': Node.objects.all()},
          'terms': [
            'val',
            'code']}
         ])



cht = Chart(
        datasource = openfisca_data,
        series_options =
          [{'options':{
              'type': 'column',
              'stacking': False},
            'terms':{
              'code': [
                'val']
              }}],
        chart_options =
          {'title': {
               'text': 'Openfisca'}})

#scenario = Scenario()
#simu = Simu()
#simu.build()
#
#x = MyNode()
#x.init_from_OutNode(simu.data_courant)
#x.remove_null_children()
#print x.code, x.vals, x.is_null
#print x
#
#
#from simulation.models import Node, NodeForm
#print x.create_fields_dict()
#form = NodeForm(data = x.create_fields_dict())
#print form
#print form.is_valid()

# model =  x.create_model('test')
# print len(model._meta.fields)

