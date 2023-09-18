from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import CustomUser

class CreateUserForm(UserCreationForm):
    # Custom fields
    full_name = forms.CharField(required=True, max_length=50,label='Full Name')
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=True)
    role = forms.ChoiceField(choices=[('Faculty', 'Faculty')], required=True)
    contact_no = forms.CharField(max_length=10, required=True)
    telephone_no = forms.CharField(max_length=10, required=False)
    current_address = forms.CharField(max_length=150, required=True)
    permanent_address = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    educational_qualification = forms.CharField(max_length=100, required=True)
    department = forms.ChoiceField(choices=[
    ('Computer', 'Computer'),
    ('CSE_AI_ML', 'CSE AI/ML'),
    ('CSE_Blockchain_IOT', 'CSE Blockchain and IOT'),
    ('Mechanical', 'Mechanical'),
    ('Electronics', 'Electronics'),
    ('Extc', 'Extc'),
    ('Civil', 'Civil'),
    ('IT', 'IT'),
    ('Automobile', 'Automobile'),
    ('Basic_Science_Humanities', 'Basic Science and Humanities')], required=True)

    designation = forms.ChoiceField(choices=[
    ('Assistant_Professor', 'Assistant Professor'),('HOD', 'HOD'),('Associate_Professor', 'Associate Professor'),('Lecturer', 'Lecturer')], required=True)

    permanent_employee =  forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')], required=True)
    date_of_probation = forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date'}))
    salary = forms.DecimalField(max_digits=10, decimal_places=2, required=True,label='Annual Salary')
    payscale = forms.CharField(max_length=20, required=False,widget=forms.TextInput(attrs={'placeholder': 'e.g., 10-12'}),label='Annual Payscale in LPA')

    def clean_email(self):
        email = self.cleaned_data['email']
        # Add custom validation logic here
        if not email.endswith('@mhssce.ac.in'):
            raise forms.ValidationError("Email must be from mhssce.ac.in domain.")
        existing_user = CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).first()

        if existing_user:
            raise forms.ValidationError("This email address is already taken. Please choose a different one.")

        return email
    
    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)

        # Assign values to the custom fields
        user.gender = self.cleaned_data['gender']
        user.role = self.cleaned_data['role']
        user.full_name = self.cleaned_data['full_name']
        user.contact_no = self.cleaned_data['contact_no']
        user.telephone_no = self.cleaned_data['telephone_no']
        user.current_address = self.cleaned_data['current_address']
        user.permanent_address = self.cleaned_data['permanent_address']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.educational_qualification = self.cleaned_data['educational_qualification']
        user.department = self.cleaned_data['department']
        user.designation = self.cleaned_data['designation']
        user.permanent_employee = self.cleaned_data['permanent_employee']
        user.date_of_probation = self.cleaned_data['date_of_probation']
        user.salary = self.cleaned_data['salary']
        user.payscale = self.cleaned_data['payscale']

        if commit:
            user.save()
            print(user)
        return user

    class Meta:
        model = CustomUser
        fields = ['full_name','email','password1', 'password2', 'gender', 'role','contact_no', 'telephone_no',
                  'current_address', 'permanent_address','educational_qualification',
                  'department', 'designation', 'permanent_employee', 'date_of_probation', 'salary', 'payscale']