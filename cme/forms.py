from django import forms
from .models import samQuestion, samAnswer
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.layout import Layout, Div
from crispy_forms.helper import FormHelper

class evaluationForm(forms.Form):
    # your_name = forms.CharField(label='Your name', max_length=100)
    CHOICES=[(0,0  ),(1,1  ),(2,2),(3,3),(4,4),(5,5),(-1,'NA')]
    programContent = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label='Program Content', required=True)#forms.RadioSelect()#models.IntegerField()
    learningObjectives = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=True, label='Learning Objectives Clearly Presented')
    facultyKnowledge = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=True, label='Faculty Knowledge')
    quality = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=True, label='Quality and Level of Presentations')
    handouts = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=True, label='Handouts/online materials')
    meetingRoom = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=True, label='Meeting Room and Facilities')
    audio = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=True, label='Audio')
    additionalComments = forms.CharField(widget=forms.Textarea,label='Additonal Comments:', required=False)

    Layout(Div(InlineRadios('CHOICES')))
    # def __init__(self, user, *args, **kwargs):
    #     super(evaluationForm, self).__init__(*args, **kwargs)
    #     self.user = user
    #     self.helper = FormHelper()



class evaluationSpeakerForm(forms.Form):
    CHOICES = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (-1, 'NA')]
    attendance_CHOICES = [(0, '0%'), (0.25, '25%'), (0.50, '50%'), (0.75, '75%'), (1.0, '100%')]
    needCAMPEP = forms.CheckboxInput()
    needMDCB = forms.CheckboxInput()
    percentAttended = forms.ChoiceField(widget=forms.RadioSelect, choices=attendance_CHOICES, required=True, label='Percent of session attended')
    learningObjectives = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=True, label='Learning Objectives Appropriate')
    usefulness = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=True, label='Usefulness of Information')
    quality = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=True, label='Quality and Level of Presentation')
    handout = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=True, label='Handout/Notes/Online Materials')
    worthiness = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=True, label='Worthiness for repeating')
    additionalComments = forms.CharField(widget=forms.Textarea,label='Additonal Comments:', required=False)
    # id=forms.IntegerField(widget = forms.HiddenInput(), required = True)
    Layout(Div(InlineRadios('CHOICES')))
    Layout(Div(InlineRadios('attendance_CHOICES')))

     # def __init__(evaluationSpeakerForm, self, *args, **kwargs):
    #     self.user = kwargs.pop('user', None)
    #     super(evaluationSpeakerForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    # def __init__(self, *args, **kwargs):
    #     self.helper = FormHelper()
    #     self.helper.form_class = 'form-horizontal'

class samQuestionsForm(forms.Form):

    samAnswer = forms.ChoiceField(required=True)#=forms.RadioSelect, choices=samQuestion.choice_set())#widget=forms.RadioSelect)#, choices=[])
    # class Meta:
    #     model = samQuestion


        # pass
    def __init__(self,  choiceList, *args, **kwargs):
        self.choiceList = []  # choiceList
        # print('#### SELF####',self)
    #
        for item in choiceList:
            self.choiceList.append((item.pk, item.answer_text))
    #     # print(self.choiceList)
    #     # print('###')
    #     # print(list(self.choiceList))
        super(samQuestionsForm, self).__init__(*args, **kwargs)
    #     # samAnswer.widget=forms.RadioSelect
        # samAnswer.initial=0
        # self.fields['samAnswer']=
        self.fields['samAnswer'].widget = forms.RadioSelect()
        self.fields['samAnswer'].label = False
        self.fields['samAnswer'].choices = self.choiceList

    def __22init__(self, choiceList, *args, **kwargs):
        self.choiceList = []#choiceList

        for item in choiceList:
            self.choiceList.append((item.pk,item.answer_text))
        # print(self.choiceList)
        # print('###')
        # print(list(self.choiceList))
        super(samQuestionsForm, self).__init__(*args, **kwargs)
        # samAnswer.widget=forms.RadioSelect
        # samAnswer.initial=0
        # self.fields['samAnswer']=
        self.fields['samAnswer'].widget = forms.RadioSelect()
        self.fields['samAnswer'].label=False
        self.fields['samAnswer'].choices=self.choiceList
        self.helper = FormHelper(self)
        # Layout(Div(InlineRadios('self.choiceList')))
        # self.fields['samAnswer'].initial=0
        # samAnswer.initial=0
