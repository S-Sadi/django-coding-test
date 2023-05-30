from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
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

    def get(self, request, *args, **kwargs):
        title = request.GET.get('title')
        price_from = request.GET.get("price_from")
        price_to = request.GET.get("price_to")
        date = request.GET.get("date")
        variant = request.GET.get("variant")
        filtered_data = Product.objects.all()

        
        if title:
            filtered_data = filtered_data.filter(title__icontains=title)
        
        if variant:
            filtered_data = filtered_data.filter(productvariantprice__product_variant_two__variant_title__icontains=variant)
        
        if price_from and price_to:
            filtered_data = filtered_data.filter(Q(productvariantprice__price__gte=price_from), Q(productvariantprice__price__lte=price_to))
        
        if date:
            filtered_data = filtered_data.filter(productvariantprice__created_at__date=date)
        
        
        paginator = Paginator(filtered_data, per_page=3)
        page_num = self.request.GET.get('page')
        pages = paginator.get_page(page_num)
        context = self.get_context_data()
        context['pages'] = pages
        
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Product.objects.all()
        paginator = Paginator(all_products, per_page=3)
        page_num = self.request.GET.get('page')
        pages = paginator.get_page(page_num)
        context["pages"] = pages
        context["total_products"] = paginator.count
        return context