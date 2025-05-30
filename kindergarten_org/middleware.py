# kindergarten_org/middleware.py
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from asgiref.sync import sync_to_async
from django.contrib import auth

class AsyncSessionMiddleware(SessionMiddleware):
    async def __call__(self, request):
        await sync_to_async(self.process_request)(request)
        response = await self.get_response(request)
        await sync_to_async(self.process_response)(request, response)
        return response

class AsyncAuthenticationMiddleware(AuthenticationMiddleware):
    async def __call__(self, request):
        request.user = await sync_to_async(auth.get_user)(request)
        response = await self.get_response(request)
        return response

class AsyncMessageMiddleware(MessageMiddleware):
    async def __call__(self, request):
        await sync_to_async(self.process_request)(request)
        response = await self.get_response(request)
        await sync_to_async(self.process_response)(request, response)
        return response