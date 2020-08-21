import weasyprint
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.template.loader import render_to_string
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from .models import Gift, GiftList
from .serializers import GiftSerializer, GiftListSerializer


class GiftViewSet(generics.ListAPIView):
    """
    This endpoint displays all gift present in the database
    """
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer


class GiftDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    This endpoint displays the details of one specific gift through its ID in addition to updating/destroying it
    """
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer


class GiftListsView(generics.ListCreateAPIView):
    """
    This endpoint displays all gift lists registered as well as creation of new gift lists
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsAuthenticatedOrReadOnly)
    queryset = GiftList.objects.all()
    serializer_class = GiftListSerializer



class GiftListDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    This endpoint handles updates/deletion/retrieving operations on a singular gift list through its ID
    """
    queryset = GiftList.objects.all()
    serializer_class = GiftListSerializer


class PurchaseGiftView(APIView):
    """
    This endpoint displays one gift list through its ID

     In additon to updating or deleting their gift list
    """

    def post(self, request, pk, gift_id):
        gift_list = get_object_or_404(GiftList, pk=pk)
        gift = get_object_or_404(Gift, giftlist__id=pk, pk=gift_id)
        if gift.purchased:
            return Response({'response': 'Gift already purchased'})
        if gift.stock == 0:
            return Response({'response': 'Gift out of stock'})
        gift.purchased = True
        gift.stock -= 1
        gift.save()
        if gift == 0:
            return Response({'response': 'Gift does not exist on Gift list'})
        send_mail('Gift list purchase',
                  f'Dear {request.user.first_name}, \n\n {gift.name} has been purchased from {gift_list.list_name}!',
                  'challenger@wedding.com', [f'{request.user.email}'])
        return Response({'response': 'Purchase successful'})


class GiftListPdfView(APIView):
    """
    This endpoint generates a pdf report for users given that they own the gift lists

    It lists purchased and unpurchased gifts along with their totals
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, giftlist_id):
        giftlist = get_object_or_404(GiftList, pk=giftlist_id)
        if giftlist.user == request.user:
            purchased_gifts = get_list_or_404(Gift, giftlist__id=giftlist_id, purchased=True)
            unpurchased_gifts = get_list_or_404(Gift, giftlist__id=giftlist_id, purchased=False)
            unpurchased_total = 0
            purchased_total = 0
            for purchased_gift in purchased_gifts:
                purchased_total += purchased_gift.price
            for unpurchased_gift in unpurchased_gifts:
                unpurchased_total += unpurchased_gift.price

            html_string = render_to_string('giftlist/pdf.html',
                                           {'giftlist': giftlist, 'purchasedgifts': purchased_gifts,
                                            'unpurchasedgifts': unpurchased_gifts,
                                            'purchased_total': purchased_total,
                                            'unpurchased_total': unpurchased_total})
            file_name = f'{giftlist.list_name}-Report.pdf'
            html = weasyprint.HTML(string=html_string)
            html.write_pdf(target=f'/tmp/{file_name}')

            fs = FileSystemStorage('/tmp')
            with fs.open(f'{file_name}') as pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                return response

        return Response({'access': 'Unauthorised'})
