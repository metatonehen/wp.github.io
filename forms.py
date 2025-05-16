from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class UploadFileForm(FlaskForm):
    file = FileField('Archivo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'svg'], 'Solo se permiten imágenes')
    ])
    description = StringField('Descripción', validators=[Length(max=200)])
    submit = SubmitField('Subir')

class EditContentForm(FlaskForm):
    content = TextAreaField('Contenido HTML', validators=[DataRequired()])
    submit = SubmitField('Guardar')