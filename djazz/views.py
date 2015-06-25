from django.http import HttpResponseNotAllowed

HTTP_METHODS_11 = ['HEAD', 'GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'TRACE']

class HttpView:
    
    _http_methods = list(HTTP_METHODS_11)
    
    def methods_available(self):
        methods = getattr(self, '_http_methods_available', None)
        if methods == None:
            methods = [m for m in self._http_methods if not getattr(self, m, None) == None]
            self._http_methods_available = methods
        
        return methods
    
    def view_unavailable(self):
        return HttpResponseNotAllowed(self.methods_available())
    
    def preprocess(self, request, *args, **kwargs):
        pass
    
    def postprocess(self, request, response, *args, **kwargs):
        pass
    
    def get_view_method(self, method):
        if not method in self.methods_available():
            return None
        return getattr(self, method, None)
    
    def view(self, request, *args, **kwargs):
        view = self.get_view_method(request.method.upper())
        if not view:
            return self.view_unavailable()
        
        process = self.preprocess(request, *args, **kwargs)
        if not preprocess == None:
            return process
        
        response = view(request, *args, **kwargs)
        
        process = self.postprocess(request, response, *args, **kwargs)
        if not process == None:
            return process
        
        return response
    
    def HEAD(self, request, *args, **kwargs):
        return self.GET(self, request, *args, **kwargs)
