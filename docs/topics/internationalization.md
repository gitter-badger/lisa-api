# Internationalization

LISA ships with translatable error messages.

* Select a language other than English as the default, using the `lang_django` setting in configuration file.
* Allow clients to choose a language themselves. A typical usage for API clients would be to include an `Accept-Language` request header.

## Enabling internationalized APIs

You can change the default language by using the `lang_django` setting in LISA API configuration file:

    lang_django = "es-es"

By default, the per-request language requests is enabled, so client requests will respect the `Accept-Language` header where possible. For example, let's make a request for an unsupported media type:

**Request**

    GET /api/users HTTP/1.1
    Accept: application/xml
    Accept-Language: es-es
    Host: example.org

**Response**

    HTTP/1.0 406 NOT ACCEPTABLE

    {"detail": "No se ha podido satisfacer la solicitud de cabecera de Accept."}

LISA includes these built-in translations both for standard exception cases, and for serializer validation errors.

Note that the translations only apply to the error strings themselves. The format of error messages, and the keys of field names will remain the same. An example `400 Bad Request` response body might look like this:

    {"detail": {"username": ["Esse campo deve ser unico."]}}


## Adding new translations

LISA translations are managed online using [Transifex][transifex-project]. You can use the Transifex service to add new translation languages. The maintenance team will then ensure that these translation strings are included in the LISA package.


#### Translating a new language locally

This guide assumes you are already familiar with how to translate a Django app.  If you're not, start by reading [Django's translation docs][django-translation].

If you're translating a new language you'll need to translate the existing LISA error messages:

1. Make a new folder where you want to store the internationalization resources. Add this path to your [`LOCALE_PATHS`][django-locale-paths] setting.

2. Now create a subfolder for the language you want to translate. The folder should be named using [locale name][django-locale-name] notation. For example: `de`, `pt_BR`, `es_AR`.

3. Now copy the [base translations file][lisa-po-source] from the LISA source code into your translations folder.

4. Edit the `lisa_api.po` file you've just copied, translating all the error messages.

5. Run `lisa-api-cli compilemessages -l pt_BR` to make the translations 
available for Django to use. You should see a message like `processing file lisa_api.po in <...>/locale/pt_BR/LC_MESSAGES`.

6. Restart your development server to see the changes take effect.

If you're only translating custom error messages that exist inside your project codebase you don't need to copy the LISA source `lisa_api.po` file into a `LOCALE_PATHS` folder, and can instead simply run Django's standard `makemessages` process.

## How the language is determined

You can find more information on how the language preference is determined in the [Django documentation][django-language-preference]. For reference, the method is:

1. First, it looks for the language prefix in the requested URL.
2. Failing that, it looks for the `LANGUAGE_SESSION_KEY` key in the current user’s session.
3. Failing that, it looks for a cookie.
4. Failing that, it looks at the `Accept-Language` HTTP header.
5. Failing that, it uses the global `LANGUAGE_CODE` setting which is defined in the LISA configuration file with the `lang_django` setting.

For API clients the most appropriate of these will typically be to use the `Accept-Language` header; Sessions and cookies will not be available unless using session authentication, and generally better practice to prefer an `Accept-Language` header for API clients rather than using language URL prefixes.

[django-translation]: https://docs.djangoproject.com/en/1.8/topics/i18n/translation
[transifex-project]: https://www.transifex.com/projects/p/lisa-api/
[lisa-po-source]: https://raw.githubusercontent.com/project-lisa/lisa-api/master/lisa_api/locale/en_US/LC_MESSAGES/lisa_api.po 
[django-language-preference]: https://docs.djangoproject.com/en/1.8/topics/i18n/translation/#how-django-discovers-language-preference
[django-locale-paths]: https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-LOCALE_PATHS
[django-locale-name]: https://docs.djangoproject.com/en/1.8/topics/i18n/#term-locale-name