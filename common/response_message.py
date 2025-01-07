class UserMessage():
    @staticmethod
    def success(data):
        return {'status':1000,'data':data}
    
    @staticmethod
    def error(data):
        return {'status':1002,'data':data}
    
    @staticmethod
    def other(data):
        return {'status':1001,'data':data}
    

class ArticleMessage():
    @staticmethod
    def success(data):
        return {'status':2000,'data':data}
    
    @staticmethod
    def error(data):
        return {'status':2002,'data':data}
    
    @staticmethod
    def other(data):
        return {'status':2001,'data':data}
    
class FavoriteMessage():
    @staticmethod
    def success(data):
        return {'status':3000,'data':data}
    
    @staticmethod
    def error(data):
        return {'status':3002,'data':data}
    
    @staticmethod
    def other(data):
        return {'status':3001,'data':data}