# Ansible vault template

## Adding new deployment

- Copy to `vault-template` and rename it to deployment server hostname
- Fill in all the TODOs that are needed:
    - `django_site_host`
        - Must be valid FQDN 
    - `node_site_host`
        - Must be valid FQDN
        - fill in if present
        - prepend extra path to `django_site_host` as cannot be hosted on the same domain
    - `letsencrypt_reminder_email` - Email where certificate expire emails will be sent by Lets Encrypt
- Add to `ansible/inventory` to correct deployment environment section
