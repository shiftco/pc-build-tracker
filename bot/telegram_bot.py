import os
import urllib.request
import urllib.parse
import json

class TelegramAlertBot:
    def __init__(self, bot_token=None, chat_id=None):
        self.bot_token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.environ.get("TELEGRAM_CHAT_ID")
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}" if self.bot_token else None

    def is_configured(self):
        return bool(self.bot_token and self.chat_id)

    def send_price_drop_alert(self, peca_nome, loja, preco_antigo, preco_novo, url_produto, imagem_url=None):
        """
        Dispara um alerta rico de queda de preço para o Telegram com botão inline.
        """
        if not self.is_configured():
            print(f"[Telegram] Alerta simulado (configure TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID para envio real):")
            print(f"🔥 QUEDA DE PREÇO: {peca_nome}")
            print(f"🏪 Loja: {loja} | De R$ {preco_antigo:.2f} por R$ {preco_novo:.2f}")
            print(f"🔗 {url_produto}")
            return False

        economia = preco_antigo - preco_novo
        percentual = (economia / preco_antigo) * 100

        caption = (
            f"🚨 <b>ALERTA DE OFERTA: PREÇO CAIU!</b>\n\n"
            f"🖥️ <b>Componente:</b> {peca_nome}\n"
            f"🏪 <b>Loja:</b> {loja}\n"
            f"📉 <b>De:</b> <s>R$ {preco_antigo:,.2f}</s>\n"
            f"⚡ <b>Por:</b> <b>R$ {preco_novo:,.2f} à vista (PIX)</b>\n"
            f"💰 <b>Economia:</b> R$ {economia:,.2f} (-{percentual:.1f}%)\n\n"
            f"⏱️ <i>Acesse rápido antes que o estoque esgote!</i>"
        )

        inline_keyboard = {
            "inline_keyboard": [
                [{"text": f"🛒 Ir para Oferta na {loja}", "url": url_produto}]
            ]
        }

        try:
            if imagem_url:
                endpoint = f"{self.api_url}/sendPhoto"
                payload = {
                    "chat_id": self.chat_id,
                    "photo": imagem_url,
                    "caption": caption,
                    "parse_mode": "HTML",
                    "reply_markup": json.dumps(inline_keyboard)
                }
            else:
                endpoint = f"{self.api_url}/sendMessage"
                payload = {
                    "chat_id": self.chat_id,
                    "text": caption,
                    "parse_mode": "HTML",
                    "reply_markup": json.dumps(inline_keyboard)
                }

            data = urllib.parse.urlencode(payload).encode("utf-8")
            req = urllib.request.Request(endpoint, data=data)
            with urllib.request.urlopen(req, timeout=10) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                print(f"[Telegram] Notificação enviada com sucesso para chat_id {self.chat_id}")
                return res.get("ok", False)
        except Exception as e:
            print(f"[Telegram] Erro ao enviar mensagem: {e}")
            return False

if __name__ == "__main__":
    bot = TelegramAlertBot()
    # Teste simulado
    bot.send_price_drop_alert(
        peca_nome="Gigabyte GeForce RTX 5070 Gaming OC 12GB GDDR7",
        loja="Terabyte",
        preco_antigo=6199.99,
        preco_novo=5899.99,
        url_produto="https://www.terabyteshop.com.br/produto/34407/placa-de-video-gigabyte-nvidia-geforce-rtx-5070-gaming-oc-12gb-gddr7-dlss-ray-tracing-gv-n5070gaming-oc-12gd",
        imagem_url="https://www.terabyteshop.com.br/img/produtos/g/placa-de-video-gigabyte-geforce-rtx-5070-gaming-oc-12gb-gddr7-192bit-gv-n5070gaming-oc-12gd_200424.jpg"
    )
