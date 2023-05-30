from django.views import generic
from django.core.paginator import Paginator

from product.models import Variant, Product, ProductVariantPrice


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list( variants.all() )
        return context

class ProductListView(generic.TemplateView):
    template_name = "products/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Product.objects.all()
        paginator = Paginator(all_products, per_page=3)
        page_num = self.request.GET.get('page')
        pages = paginator.get_page(page_num)
        context["pages"] = pages
        context["total_products"] = paginator.count
        return context