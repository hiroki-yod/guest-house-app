import json
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.shortcuts import redirect
from django.views.generic import ListView
from ..models import ReservationFrame
from ..models import Price

# STRIPEのシークレットキー
stripe.api_key = settings.STRIPE_SECRET_KEY

class ProductTopPageView(ListView):
    # 商品マスタ
    model = ReservationFrame
    # ページリンク
    template_name = "booking/stripe/product-top.html"
    #レコード情報をテンプレートに渡すオブジェクト
    context_object_name = "product_list"


class CreateCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        # 商品マスタ呼出
        product = ReservationFrame.objects.get(id=self.kwargs["pk"])
        price   = Price.objects.get(product=product)

        # ドメイン
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        # 決済用セッション
        checkout_session = stripe.checkout.Session.create(
            # 決済方法
            payment_method_types=['card'],
            # 決済詳細
            line_items=[
                {
                    'price': price.stripe_price_id,       # 価格IDを指定 
                    'quantity': 1,                        # 数量
                },
            ],
            # POSTリクエスト時にメタデータ取得
            metadata = {
                        "product_id":product.id,
                       },
            mode='payment',                               # 決済手段（一括）
            success_url=YOUR_DOMAIN + '/success/',        # 決済成功時のリダイレクト先
            cancel_url=YOUR_DOMAIN + '/cancel/',          # 決済キャンセル時のリダイレクト先
        )
        return redirect(checkout_session.url)