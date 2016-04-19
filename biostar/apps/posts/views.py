# -*- coding: utf8 -*-
from django.shortcuts import render_to_response
from django.views.generic import TemplateView, DetailView, ListView, FormView, UpdateView
from .models import Post
from django import forms
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Submit, ButtonHolder
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib import messages
from . import auth
from braces.views import LoginRequiredMixin
from datetime import datetime
from django.utils.timezone import utc
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from biostar.const import OrderedDict
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import re
import logging

import langdetect
from django.template.loader import render_to_string

def english_only(text):
    try:
        text.decode('ascii')
    except Exception:
        raise ValidationError('Title may only contain plain text (ASCII) characters')


def valid_language(text):
    supported_languages = settings.LANGUAGE_DETECTION
    if supported_languages:
        lang = langdetect.detect(text)
        if lang not in supported_languages:
            raise ValidationError(
                    'Language "{0}" is not one of the supported languages {1}!'.format(lang, supported_languages))

logger = logging.getLogger(__name__)


def valid_title(text):
    "Validates form input for tags"
    text = text.strip()
    if not text:
        raise ValidationError('Por favor ingresa un título')

    if len(text) < 10:
        raise ValidationError('El título es muy corto')

    words = text.split(" ")
    if len(words) < 3:
        raise ValidationError('Más de dos palabras por favor.')


def valid_tag(text):
    "Validates form input for tags"
    text = text.strip()
    if not text:
        raise ValidationError('Ingresa por lo menos un tag')
    if len(text) > 50:
        raise ValidationError('El tag line es muy grande (50 caracteres máx.)')
    words = text.split(",")
    if len(words) > 5:
        raise ValidationError('Tienes muchos tags (5 permitidos)')

class PagedownWidget(forms.Textarea):
    TEMPLATE = "pagedown_widget.html"

    def render(self, name, value, attrs=None):
        value = value or ''
        rows = attrs.get('rows', 15)
        klass = attrs.get('class', '')
        params = dict(value=value, rows=rows, klass=klass)
        return render_to_string(self.TEMPLATE, params)


class LongForm(forms.Form):
    FIELDS = "title content post_type tag_val".split()

    POST_CHOICES = [(Post.QUESTION, "Pregunta"),
                    (Post.JOB, "Oferta de trabajo"),
                    (Post.TUTORIAL, "Tutorial"), (Post.TOOL, "Herramienta"),
                    (Post.FORUM, "Foro"), (Post.NEWS, "Noticias"),
                    (Post.BLOG, "Blog"), (Post.PAGE, "Página")]

    title = forms.CharField(
        label="Título del post",
        max_length=200, min_length=10, validators=[valid_title, english_only],
        help_text="Títulos descriptivos promueven mejores respuestas.")

    post_type = forms.ChoiceField(
        label="Tipo de post",
        choices=POST_CHOICES, help_text="Selecciona un tipo de Post: Pregunta, Foro, Trabajo, Blog")

    tag_val = forms.CharField(
        label="Post Tags",
        required=True, validators=[valid_tag],
        help_text="Escoje uno o más tags que concuerden con el tema. Para crear un tag nuevo sólo escribelo y presiona INTRO.",
    )

    content = forms.CharField(widget=PagedownWidget, validators=[valid_language],
                              min_length=80, max_length=15000,
                              label="Ingresa el post abajo")

    def __init__(self, *args, **kwargs):
        super(LongForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "post-form"
        self.helper.layout = Layout(
            Fieldset(
                'Post',
                Field('title'),
                Field('post_type'),
                Field('tag_val'),
                Field('content'),
            ),
            ButtonHolder(
                Submit('submit', 'Enviar')
            )
        )


class ShortForm(forms.Form):
    FIELDS = ["content"]

    content = forms.CharField(widget=PagedownWidget, min_length=20, max_length=5000,)

    def __init__(self, *args, **kwargs):
        super(ShortForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Post',
                'content',
            ),
            ButtonHolder(
                Submit('submit', 'Enviar')
            )
        )


def parse_tags(category, tag_val):
    pass


@login_required
@csrf_exempt
def external_post_handler(request):
    "This is used to pre-populate a new form submission"
    import hmac

    user = request.user
    home = reverse("home")
    name = request.REQUEST.get("name")

    if not name:
        messages.error(request, "Request incorrecto. No se encuentra el parámetro nombre")
        return HttpResponseRedirect(home)

    try:
        secret = dict(settings.EXTERNAL_AUTH).get(name)
    except Exception, exc:
        logger.error(exc)
        messages.error(request, "EXTERNAL_AUTH incorrecto, error interno")
        return HttpResponseRedirect(home)

    if not secret:
        messages.error(request, "EXTERNAL_AUTH incorrecto, No hay una KEY para el nombre dado")
        return HttpResponseRedirect(home)

    content = request.REQUEST.get("content")
    submit = request.REQUEST.get("action")
    digest1 = request.REQUEST.get("digest")
    digest2 = hmac.new(secret, content).hexdigest()

    if digest1 != digest2:
        messages.error(request, "digests does not match")
        return HttpResponseRedirect(home)

    # auto submit the post
    if submit:
        post = Post(author=user, type=Post.QUESTION)
        for field in settings.EXTERNAL_SESSION_FIELDS:
            setattr(post, field, request.REQUEST.get(field, ''))
        post.save()
        post.add_tags(post.tag_val)
        return HttpResponseRedirect(reverse("post-details", kwargs=dict(pk=post.id)))

    # pre populate the form
    sess = request.session
    sess[settings.EXTERNAL_SESSION_KEY] = dict()
    for field in settings.EXTERNAL_SESSION_FIELDS:
        sess[settings.EXTERNAL_SESSION_KEY][field] = request.REQUEST.get(field, '')

    return HttpResponseRedirect(reverse("new-post"))


class NewPost(LoginRequiredMixin, FormView):
    form_class = LongForm
    template_name = "post_edit.html"

    def get(self, request, *args, **kwargs):
        initial = dict()

        # Attempt to prefill from GET parameters
        for key in "title tag_val content".split():
            value = request.GET.get(key)
            if value:
                initial[key] = value


        # Attempt to prefill from external session
        sess = request.session
        if settings.EXTERNAL_SESSION_KEY in sess:
            for field in settings.EXTERNAL_SESSION_FIELDS:
                initial[field] = sess[settings.EXTERNAL_SESSION_KEY].get(field)
            del sess[settings.EXTERNAL_SESSION_KEY]

        form = self.form_class(initial=initial)
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
        # Validating the form.
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        # Valid forms start here.
        data = form.cleaned_data.get

        title = data('title')
        content = data('content')
        post_type = int(data('post_type'))
        tag_val = data('tag_val')

        post = Post(
            title=title, content=content, tag_val=tag_val,
            author=request.user, type=post_type,
        )
        post.save()

        # Triggers a new post save.
        post.add_tags(post.tag_val)

        messages.success(request, "%s created" % post.get_type_display())
        return HttpResponseRedirect(post.get_absolute_url())


class NewAnswer(LoginRequiredMixin, FormView):
    """
    Creates a new post.
    """
    form_class = ShortForm
    template_name = "post_edit.html"
    type_map = dict(answer=Post.ANSWER, comment=Post.COMMENT)
    post_type = None

    def get(self, request, *args, **kwargs):
        initial = {}

        # The parent id.
        pid = int(self.kwargs['pid'])
        # form_class = ShortForm if pid else LongForm
        form = self.form_class(initial=initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        pid = int(self.kwargs['pid'])

        # Find the parent.
        try:
            parent = Post.objects.get(pk=pid)
        except ObjectDoesNotExist, exc:
            messages.error(request, "El post no existe. Quizás fue borrado")
            return HttpResponseRedirect("/")

        # Validating the form.
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        # Valid forms start here.
        data = form.cleaned_data.get

        # Figure out the right type for this new post
        post_type = self.type_map.get(self.post_type)
        # Create a new post.
        post = Post(
            title=parent.title, content=data('content'), author=request.user, type=post_type,
            parent=parent,
        )

        messages.success(request, "%s created" % post.get_type_display())
        post.save()

        return HttpResponseRedirect(post.get_absolute_url())


class EditPost(LoginRequiredMixin, FormView):
    """
    Edits an existing post.
    """

    # The template_name attribute must be specified in the calling apps.
    template_name = "post_edit.html"
    form_class = LongForm

    def get(self, request, *args, **kwargs):
        initial = {}

        pk = int(self.kwargs['pk'])
        post = Post.objects.get(pk=pk)
        post = auth.post_permissions(request=request, post=post)

        # Check and exit if not a valid edit.
        if not post.is_editable:
            messages.error(request, "Este usuario no puede modificar el post")
            return HttpResponseRedirect(reverse("home"))

        initial = dict(title=post.title, content=post.content, post_type=post.type, tag_val=post.tag_val)

        # Disable rich editing for preformatted posts
        pre = 'class="preformatted"' in post.content
        form_class = LongForm if post.is_toplevel else ShortForm
        form = form_class(initial=initial)
        return render(request, self.template_name, {'form': form, 'pre': pre})

    def post(self, request, *args, **kwargs):

        pk = int(self.kwargs['pk'])
        post = Post.objects.get(pk=pk)
        post = auth.post_permissions(request=request, post=post)

        # For historical reasons we had posts with iframes
        # these cannot be edited because the content would be lost in the front end
        if "<iframe" in post.content:
            messages.error(request, "Este post no es editable porque está un iframe. Contáctate si quiere editarlo")
            return HttpResponseRedirect(post.get_absolute_url())

        # Check and exit if not a valid edit.
        if not post.is_editable:
            messages.error(request, "Este usuario no edita este post")
            return HttpResponseRedirect(post.get_absolute_url())

        # Posts with a parent are not toplevel
        form_class = LongForm if post.is_toplevel else ShortForm

        form = form_class(request.POST)
        if not form.is_valid():
            # Invalid form submission.
            return render(request, self.template_name, {'form': form})

        # Valid forms start here.
        data = form.cleaned_data

        # Set the form attributes.
        for field in form_class.FIELDS:
            setattr(post, field, data[field])

        # TODO: fix this oversight!
        post.type = int(data.get('post_type', post.type))

        # This is needed to validate some fields.
        post.save()

        if post.is_toplevel:
            post.add_tags(post.tag_val)

        # Update the last editing user.
        post.lastedit_user = request.user
        post.lastedit_date = datetime.utcnow().replace(tzinfo=utc)
        post.save()
        messages.success(request, "Post actualizado")

        return HttpResponseRedirect(post.get_absolute_url())

    def get_success_url(self):
        return reverse("user_details", kwargs=dict(pk=self.kwargs['pk']))

