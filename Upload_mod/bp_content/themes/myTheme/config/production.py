import os

config = {

    # This config file will be detected in production environment and values defined here will overwrite those in config.py
    'environment': "production",

    # ----> ADD MORE CONFIGURATION OPTIONS HERE <----
    # application name
    'app_name': "arbitration-ks",
    
    # contact page email settings
    'contact_sender': "wagner@nmb.gov",
    'contact_recipient': "wagner@nmb.gov",

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
}
