import os

config = {

    # This config file will be detected in localhost environment and values defined here will overwrite those in config.py
    'environment': "localhost",

    # application name
    'app_name': "arbitration-ks",
    
    # contact page email settings
    'contact_sender': "noreply@upload.arbitration-ks.appspot.com",
    'contact_recipient': "noreply@upload.arbitration-ks.appspot.com",
    
    # Enable Federated login (OpenID and OAuth)
    # Google App Engine Settings must be set to Authentication Options: Federated Login
    'enable_federated_login': False,

    # jinja2 templates
    'webapp2_extras.jinja2': {'template_path': ['ks/templates', 'bp_admin/templates', 'bp_content/themes/%s/templates' % os.environ['theme']],
                              'environment_args': {'extensions': ['jinja2.ext.i18n']}},

    # webapp2 sessions
    'webapp2_extras.sessions': { 'secret_key': 'nmbasdja*wFRawfjasfcj8(^3wrf(asdfajf;awefj32r98*^Q{#t' },

    # webapp2 authentication
    'webapp2_extras.auth': { 'user_model': 'bp_includes.models.User',
                            'cookie_name': 'gae_session' },
          
    # get your own recaptcha keys by registering at http://www.google.com/recaptcha/
    'captcha_public_key': "6Ldo2fwSAAAAAB4e3uKTRw69jBS4JiOf7e85pBG0",
    'captcha_private_key': "6Ldo2fwSAAAAAH9VP_7_hGDiOS8vbWpzK44e7-nN",
    
    # Password AES Encryption Parameters
    # aes_key must be only 16 (*AES-128*), 24 (*AES-192*), or 32 (*AES-256*) bytes (characters) long.
    'aes_key': "4ab14c33d92e74d233e42843aab31543",
    'salt': "awefwaf9&asfd;lj*&asdfj&^_)3fqfja{{sf2/23rfa[[.,<<&Hd23faf;afj3if83jfa;38j2a",
    
    # add status codes and templates used to catch and display errors
    # if a status code is not listed here it will use the default app engine
    # stacktrace error page or browser error page
    'error_templates': {
        403: 'errors/forbidden_access.html',
        404: 'errors/default_error.html',
        500: 'errors/default_error.html',
    },    
}