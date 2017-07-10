from django.forms import FileField, ClearableFileInput
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView

from maker.models import Apk, ApkPointer
from . import BaseModelForm
from .repository import RepositoryAuthorizationMixin, ApkUploadMixin


class ApkForm(BaseModelForm):
    apks = FileField(required=False, widget=ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Apk
        fields = ['apks']

    class Media:
        js = ('maker/js/drag-and-drop.js',)


class ApkUploadView(ApkUploadMixin, UpdateView):
    form_class = ApkForm
    template_name = "maker/error.html"

    def get(self, request, *args, **kwargs):
        # don't answer GET requests
        return HttpResponseNotFound()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            return self.form_invalid(form)

        # add posted APKs
        failed = self.add_apks()
        if len(failed) > 0:
            form.add_error('apks', self.get_error_msg(failed))
            return super(ApkUploadView, self).form_invalid(form)

        # don't let the View create anything as we already did
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('repo', args=[self.get_repo().pk])


class ApkPointerDeleteView(RepositoryAuthorizationMixin, DeleteView):
    model = ApkPointer
    template_name = 'maker/app/apk_delete.html'
    pk_url_kwarg = 'pk'

    def get_repo(self):
        return self.get_object().app.repo

    def get_success_url(self):
        self.get_repo().update_async()
        return reverse_lazy('app_edit', kwargs={'repo_id': self.kwargs['repo_id'],
                                                'app_id': self.kwargs['app_id']})
