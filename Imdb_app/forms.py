class SignupForm(forms.Form):
    display_name = models.CharField(max_length=50)
    # Was unsure of to whether to include the likes,want_to_see, and have_seen in the inital signup or rather after


# This is the comment form **Model Form
class Comment_Form(forms.ModelForm):
    class Meta:
        Model = Comment_model
        fields = [
            'input_field', 
            'movie',
            'commenter', 
            'date_created',
            'recommended'
        ]