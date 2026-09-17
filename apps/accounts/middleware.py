from django.utils import timezone


class UpdateLastSeenMiddleware:
    """Обновляет время последнего визита пользователя."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            now = timezone.now()
            last_seen = request.user.last_seen

            # Обновляем не чаще, чем раз в минуту
            if not last_seen or (now - last_seen).total_seconds() > 60:
                request.user.last_seen = now
                request.user.save(update_fields=['last_seen'])

        return response