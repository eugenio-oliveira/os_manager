from django import forms
from .models import OrdemServico, Cliente
from django.forms.widgets import TextInput, Select, Textarea, DateInput

class ClienteModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nome} ({obj.cpf})"

class OrdemServicoForm(forms.ModelForm):
    cliente = ClienteModelChoiceField(
        queryset=Cliente.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Cliente"
    )

    class Meta:
        model = OrdemServico
        exclude = []
        widgets = {
            'responsavel': Select(attrs={'class': 'form-control'}),
            'situacao': Select(attrs={'class': 'form-control', 'readonly': True}),
            'data_os': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'previsao_entrega': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'canal_venda': Select(attrs={'class': 'form-control'}),
            'equipamento': TextInput(attrs={'class': 'form-control'}),
            'marca': TextInput(attrs={'class': 'form-control'}),
            'modelo': TextInput(attrs={'class': 'form-control'}),
            'serie': TextInput(attrs={'class': 'form-control'}),
            'condicoes': Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'defeitos': Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'acessorios': Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'solucao': Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'laudo_tecnico': Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'termos_garantia': Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        situacao = cleaned_data.get("situacao")
        instance = self.instance

        if instance and instance.pk and instance.situacao == 'fechada' and situacao != 'fechada':
            raise forms.ValidationError("Não é possível reabrir uma OS que já foi fechada.")
