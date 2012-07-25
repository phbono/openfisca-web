# -*-coding:Utf-8 -*

#from django.db import models
import datetime
from django.db import models

from django.forms import Form, IntegerField, DateField, ChoiceField, BooleanField, TextInput  

from django import template

from django.forms.extras.widgets import SelectDateWidget

from django.forms.fields import CheckboxInput



pacs   = [ ('pac' + str(i), 'Personne à charge')  for i in range(1,10)]
QUIFOY = (('vous', 'Vous'), ('conj', 'Conjoint')) +  tuple(pacs)
enfants = [ ('enf' + str(i), 'enfant')  for i in range(1,10)]
QUIFAM = (('chef', 'parent 1'), ('part', 'parent 2')) + tuple(enfants) 

register = template.Library()

@register.filter(name='is_checkbox')
def is_checkbox(value):
    return isinstance(value, CheckboxInput)

#class Individual(models.Model):
#    noindiv = models.IntegerField(label = 'n°', initial = 1)
#    birth   = models.DateField(widget = SelectDateWidget(), initial = timezone.now())
#    noidec  = models.IntegerField(label = 'Numéro de déclaration', initial = 1)
#    quifoy  = models.CharField(label = 'Position déclaration impôts',choices = QUIFOY)
#    remplirdeclar = models.BooleanField(required = False, initial = True, label = 'Foyer')
#    noifam = models.IntegerField(label = 'Numéro de famille', initial = 1)
#    quifam = models.CharField(label = 'Position déclaration impôts',choices = QUIFAM)
#        
#    def __unicode__(self):
#        return self.noindiv
#    
#class IndividualForm(ModelForm):
#    class Meta:
#        model = Individual


class IndividualForm(Form):
    noi = IntegerField(label = 'n°')
    birth   = DateField(widget = SelectDateWidget(years=range(1900, datetime.date.today().year)))
    idfoy  = IntegerField(label = 'Numéro de déclaration')
    quifoy  = ChoiceField(label = 'Position déclaration impôts',choices = QUIFOY)
    #remplirdeclar = BooleanField(required = False, initial = True, label = 'Foyer')
    idfam = IntegerField(label = 'Numéro de famille')
    quifam = ChoiceField(label = 'Position famille', choices = QUIFAM )



#class DeclarForm(Form):
#    def __init__(self, *args, **kwargs):
#        extra = kwargs.pop('extra')
#        super(Form, self).__init__(*args, **kwargs)
#
#        for code, label in extra:
#            
#            self.fields[code] = CharField(label=label)


class MyBooleanField(BooleanField):
    def __init__(self, *args, **kwargs):
        BooleanField.__init__(self, required=False, *args, **kwargs)


class MyIntegerField(IntegerField):
#    def __init__(self, kwargs = {}, *args):
    def __init__(self, *args, **kwargs):
        widgetAttr = {'size':'8', 
                      'align': 'right',
                      'maxlength':'9', 
                      'style' : "text-align: right"
                      }
        wid = TextInput(attrs=widgetAttr)
        fieldAttr = {'max_value': 999999999, 
                     'min_value': 0,
                     'required' : False,
                     'localize': True
                     }
        fieldAttr.update(kwargs)
        IntegerField.__init__(self, widget = wid, **fieldAttr)


class MyDateField(DateField):
    def __init__(self, kwargs = {}):
        wid = SelectDateWidget(years = [i for i in reversed(xrange(1900,2010))])
        fieldAttr = {'required' : False, 
                     'localize': True
                     }
        fieldAttr.update(kwargs)
        DateField.__init__(self, widget= wid, **fieldAttr)



class Declar1Form(Form):
    statmarit = ChoiceField(choices = ((2,'Célibataire'), (1,'Marié'), (5,'Pacsé'), (4,'Veuf'),(5,'Divorcé')))
    
    def __init__(self, *args, **kwargs):
        super(Declar1Form, self).__init__(*args, **kwargs)

        birth_dates = ['birthv','birthc'] + ['birth' + str(i) for i in range(1,10)]
        for birth_date in birth_dates:
            if birth_date == 'birthv':
                self.fields[birth_date] = MyDateField({'required':True})
            else:
                self.fields[birth_date] = MyDateField()



class Declar2Form(Form):
    def __init__(self, *args, **kwargs):
        super(Declar2Form, self).__init__(*args, **kwargs)

        cases = ['caseL', 'caseE', 'caseN', 'caseP', 'caseF', 'caseW', 'caseS', 'caseG', 'caseT']  
        for case in cases:
            self.fields[case] = MyBooleanField()
            

from core.columns import BoolCol, IntCol

class Declar3Form(Form):
    def __init__(self, *args, **kwargs):
        description = kwargs.pop('description')
        print description.col_names
        super(Declar3Form, self).__init__(*args, **kwargs)
        fields = ['f1aj', 'f1bj', 'f1cj', 'f1dj', 
                  'f1ap', 'f1bp', 'f1cp', 'f1dp', 
                  'f1ak', 'f1bk', 'f1ck', 'f1dk', 
                  'f1ai', 'f1bi', 'f1ci', 'f1di', 
                  'f1au', 'f1bu', 'f1cu', 'f1du', 
                  'f1ax', 'f1bx', 'f1cx', 'f1dx',
                  'f1av', 'f1bv', 'f1cv', 'f1dv', 
                  'f1bl', 'f1cb',  'f1dq', 
                  'f1as', 'f1bs', 'f1cs', 'f1ds', 
                  'f1at', 'f1bt',
                  'f1ao', 'f1bo', 'f1co', 'f1do']
    
        convert = dict()
        abcd = ['a', 'b', 'c', 'd']
        for l in abcd: 
            convert['f1'+l+'j' ] = 'sali'
            convert['f1'+l+'p' ] = 'choi'
            convert['f1'+l+'k' ] = 'fra'
            convert['f1'+l+'i' ] = 'cho_ld'
            convert['f1'+l+'u' ] = 'hsup'
            convert['f1'+l+'x' ] = 'ppe_tp_sa'
            convert['f1'+l+'v' ] = 'ppe_du_sa'
            convert['f1'+l+'s' ] = 'rsti'
            convert['f1'+l+'o' ] = 'alr'             
        
        for field in fields:
            
            print 'is ' + str(field) + ' in description :' + str( field in description.col_names) 
            
            if field not in ['f1bl', 'f1cb', 'f1dq', 'f1at', 'f1bt']:
                col = description.get_col(convert[field])
                if col.label is not None:
                    label = col.label
                else:
                    label = field    
                print col
                print label
                
                if isinstance(col, IntCol):
                    self.fields[field] = MyIntegerField(label=label)
                if isinstance(col, BoolCol):
                    self.fields[field] = MyBooleanField(label=label)

            elif field in ['f1bl', 'f1cb', 'f1dq']:                
                self.fields[field] = MyIntegerField(label='')

    
class Declar4Form(Form):
    def __init__(self, *args, **kwargs):
        int_fields = ['f2da', 'f2dh', 'f2ee', 'f2dc', 'f2fu', 'f2ch', 
                      'f2ts', 'f2go', 'f2tr', 'f2cg', 'f2bh', 'f2ca', 
                      'f2ab', 'f2bg', 'f2aa', 'f2al', 'f2am', 'f2an',
                      'f2dm', 'f3vg', 'f3vh', 'f3vt', 'f3vu', 'f3vv',
                       'f4be', 'f4ba', 'f4bb', 'f4bc', 'f4bd', 'f4bf',
                       'f0xx']
        for field in int_fields:
            self.fields[field] = MyIntegerField(label='') 
    

class Declar5Form(Form):
    def __init__(self, *args, **kwargs):
        int_fields = ['f6de', 'f6gi', 'f6gj', 'f6el', 'f6em', 'f6gp',
                      'f6gu', 'f6dd', 'f6rs', 'f6rt', 'f6ru', 'f6ss',
                      'f6st', 'f6su', 'faps', 'fapt', 'fapu', 'fbps',
                      'fbpt', 'fbpu', 'fcps', 'fcpt', 'fcpu', 'fdps', 
                      'fdpt', 'fdpu', 'f6qs', 'f6qt', 'f6qu', 'f7ue',
                      'f7ud', 'f7uf', 'f7xs', 'f7xt', 'f7xu', 'f7xw', 
                      'f7xy', 'f7ac', 'f7ae', 'f7ag', 'f7db', 'f7df',
                      'f7dl', 'f7vy', 'f7vz', 'f7vw', 'f7vx', 'f7wn',
                      'f7wo', 'f7wm', 'f7wp', 'f7wq', 'f7wh', 'f7wk',
                      'f7wf', 'f7wi', 'f7wj', 'f7wl', 'f8by', 'f8cy',
                      'f8ut', 'f8tf', 'f8ti', 'f8tl', 'f8tk', 'f7we']
    
        bool_fields = ['f6qr', 'f6qw', 'f7dq', 'f7dg']
    
        for field in int_fields:
            self.fields[field] = MyIntegerField()
           
        for field in bool_fields:
            self.fields[field] = MyBooleanField()
        
        
#class IndividuForm(forms.Form):
#    def 
#    __init__(self, indiv = None):
#        super(IndividuForm, self).__init__()
#    # indiv est un dict de dict. La clé est le noi de l'individu
#    # Exemple :
#    # 0: {'quifoy': 'vous', 'noi': 0, 'quifam': 'parent 1', 'noipref': 0, 'noidec': 0, 
#    #     'birth': datetime.date(1980, 1, 1), 'quimen': 'pref', 'noichef': 0}
#        if indiv == None:
#            indiv = {0: {'quifoy': 'vous', 'noi': 0, 'quifam': 'parent 1', 'noipref': 0, 'noidec': 0,
#                         'birth': datetime.date(1980, 1, 1), 'quimen': 'pref', 'noichef': 0} 


#class MenageForm(forms.Form):
#    def __init__(self, *args, **kwargs):
#        scenario = kwargs.pop('scenario')
#        super(MenageForm, self).__init__(*args, **kwargs)
#            for individual in 



