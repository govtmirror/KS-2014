# *-* coding: UTF-8 *-*

# standard library imports
import logging
# related third party imports
from google.appengine.api import users
# local application/library specific imports
#from bp_content.themes.default.config import config
from bp_content.themes.myTheme.config import config



def user_required(handler):
    """
         Decorator for checking if there's a user associated
         with the current session.
         Will also fail if there's no session present.
    """

    logging.info("check user_required a")
    def check_login(self, *args, **kwargs):
        """
            If handler has no login_url specified invoke a 403 error
        """
        logging.info("check user_required b")
        if self.request.query_string != '':
            query_string = '?' + self.request.query_string
        else:
            query_string = ''

        continue_url = self.request.path_url + query_string
        login_url = self.uri_for('login', **{'continue': continue_url})

        logging.info("check user_required c")
        auth = self.auth.get_user_by_session()
        try:
            auth = self.auth.get_user_by_session()
            if not auth:
                try:
                    self.redirect(login_url, abort=True)
                except (AttributeError, KeyError), e:
                    self.abort(403)
        except AttributeError, e:
            # avoid AttributeError when the session was delete from the server
            logging.error(e)
            self.auth.unset_session()
            self.redirect(login_url)

        return handler(self, *args, **kwargs)
    return check_login


def user_permission_required(permissionName):
    
    logging.info("check user_permission_required a")
    def user_has_permission(handler):
        """
             Decorator for checking if the user has
             permission to access a piece of functionality.
        """
        logging.info("check user_permission_required b")
            
        @user_required  #first ensure the user is logged in
        def check_user_permission(self, *args, **kwargs):
            logging.info("check user_permission_required c")
            if self.group:
                logging.info("check user_permission_required d")
                groupAsDict = self.group.to_dict()
                logging.info("groupAsDict=")
                logging.info(groupAsDict)   
                logging.info(permissionName)        
                if permissionName in groupAsDict: #ensure that the key permissionName is a key in the dict
                    if groupAsDict[permissionName] == True:
                        return handler(self, *args, **kwargs)
            
            self.abort(403)
        
        return check_user_permission

    return user_has_permission


def admin_required(handler):
    """
         Decorator for checking if there's a admin user associated
         with the current session.
         Will also fail if there's no session present.
    """

    def check_admin(self, *args, **kwargs):
        """
            If handler has no login_url specified invoke a 403 error
        """
        if not users.is_current_user_admin() and config.get('environment') == "production":
            self.response.write(
                '<div style="padding-top: 200px; height:178px; width: 500px; color: white; margin: 0 auto; font-size: 52px; text-align: center; background: url(\'http://3.bp.blogspot.com/_d_q1e2dFExM/TNWbWrJJ7xI/AAAAAAAAAjU/JnjBiTSA1xg/s1600/Bank+Vault.jpg\')">Forbidden Access <a style=\'color: white;\' href=\'%s\'>Login</a></div>' %
                users.create_login_url(self.request.path_url + self.request.query_string))
            return
        else:
            return handler(self, *args, **kwargs)

    return check_admin


def cron_method(handler):
    """
    Decorator to indicate that this is a cron method and applies request.headers check
    """

    def check_if_cron(self, *args, **kwargs):
        """
         Check if it is executed by Cron in Staging or Production
         Allow run in localhost calling the url
        """
        if self.request.headers.get('X-AppEngine-Cron') is None \
            and config.get('environment') == "production" \
            and not users.is_current_user_admin():
            return self.error(403)
        else:
            return handler(self, *args, **kwargs)

    return check_if_cron


def taskqueue_method(handler):
    """
    Decorator to indicate that this is a taskqueue method and applies request.headers check
    """

    def check_if_taskqueue(self, *args, **kwargs):
        """
         Check if it is executed by Taskqueue in Staging or Production
         Allow run in localhost calling the url
        """
        if self.request.headers.get('X-AppEngine-TaskName') is None \
            and config.get('environment') == "production" \
            and not users.is_current_user_admin():
            return self.error(403)
        else:
            return handler(self, *args, **kwargs)

    return check_if_taskqueue
