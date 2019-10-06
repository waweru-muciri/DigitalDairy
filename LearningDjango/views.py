from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def index(request):
	return render(request, template_name='digitaldairy/html/landing-page.html')


def service_worker_js(request):
	return render(request, 'digitaldairy/service-worker.js',content_type="application/x-javascript")


def firebase_messaging_sw_js(request):
	return render(request, 'digitaldairy/firebase-messaging-sw.js',content_type="application/x-javascript")


