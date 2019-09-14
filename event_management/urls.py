from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register('api/items', ItemViewSet, 'items')
router.register('api/invoices', InvoicesViewSet, 'invoices')
router.register('api/quotationparts', QuotationPartsViewSet, 'quotationparts')
router.register('api/quotations', QuotationsViewSet, 'quotations')
urlpatterns = router.urls