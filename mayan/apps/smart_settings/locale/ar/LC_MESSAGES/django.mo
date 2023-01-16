��    8      �  O   �      �     �  �   �  �   �  B  �    �  s  �  d   c
    �
  +  �  �     #  �           �     2  �  u  �  Z   A  ^   �  8   �  �   4  �   �  C   �  �   �  2  �  �   �  �  �  b   u  �  �     a!     b"     i"     n"     "     �"  =   �"     �"     �"  
   #  
   #     #     *#     =#     [#     d#  d   ~#  `   �#     D$  �   S$    I%  O   Z&    �&     �'     �'     �'  x  �'  �  Z)  2   "+  P   U+  Q   �+  v   �+     o,  �   �,  '   ;-  �  c-     7/  �   S/  p  �/  !   i1     �1     �1  u   �1     92     U2  �   q2  �   /3     �3     �3  C   �3  R   14     �4  S   �4     �4  a   5  W   r5  �   �5  
   �6  
   �6     �6     �6  .   �6  Q   $7     v7     }7     �7     �7     �7  &   �7  *   �7     %8  1   48  �   f8  \   9     ^9    ~9     �:  ,   �:  �   �:     �;  !   �;  
   �;  �  �;         3       1         ,         #          $       
   	      (          7       *                                      2          5   %                    4      '              -             /              "            !      &   .      0          8               +          6   )    "%s" not a valid entry. A boolean that specifies whether to use the X-Forwarded-Host header in preference to the Host header. This should only be enabled if a proxy which sets this header is in use. A boolean that specifies whether to use the X-Forwarded-Port header in preference to the SERVER_PORT META variable. This should only be enabled if a proxy which sets this header is in use. USE_X_FORWARDED_HOST takes priority over this setting. A dictionary containing the settings for all databases to be used with Django. It is a nested dictionary whose contents map a database alias to a dictionary containing the options for an individual database. The DATABASES setting must configure a default database; any number of additional databases may also be specified. A list of IP addresses, as strings, that: Allow the debug() context processor to add some variables to the template context. Can use the admindocs bookmarklets even if not logged in as a staff user. Are marked as "internal" (as opposed to "EXTERNAL") in AdminEmailHandler emails. A list of all available languages. The list is a list of two-tuples in the format (language code, language name) for example, ('ja', 'Japanese'). This specifies which languages are available for language selection. Generally, the default value should suffice. Only set this setting if you want to restrict language selection to a subset of the Django-provided languages.  A list of authentication backend classes (as strings) to use when attempting to authenticate a user. A list of strings representing the host/domain names that this site can serve. This is a security measure to prevent HTTP Host header attacks, which are possible even under many seemingly-safe web server configurations. Values in this list can be fully qualified names (e.g. 'www.example.com'), in which case they will be matched against the request's Host header exactly (case-insensitive, not including port). A value beginning with a period can be used as a subdomain wildcard: '.example.com' will match example.com, www.example.com, and any other subdomain of example.com. A value of '*' will match anything; in this case you are responsible to provide your own validation of the Host header (perhaps in a middleware; if so this middleware must be listed first in MIDDLEWARE). A string representing the language code for this installation. This should be in standard language ID format. For example, U.S. English is "en-us". It serves two purposes: If the locale middleware isn't in use, it decides which translation is served to all users. If the locale middleware is active, it provides a fallback language in case the user's preferred language can't be determined or is not supported by the website. It also provides the fallback translation when a translation for a given literal doesn't exist for the user's preferred language. A string representing the time zone for this installation. Note that this isn't necessarily the time zone of the server. For example, one server may serve multiple Django-powered sites, each with a separate time zone setting. A tuple representing a HTTP header/value combination that signifies a request is secure. This controls the behavior of the request object’s is_secure() method. Warning: Modifying this setting can compromise your site’s security. Ensure you fully understand your setup before changing it. Default Default: '' (Empty string). Password to use for the SMTP server defined in EMAIL_HOST. This setting is used in conjunction with EMAIL_HOST_USER when authenticating to the SMTP server. If either of these settings is empty, Django won't attempt authentication. Default: '' (Empty string). Username to use for the SMTP server defined in EMAIL_HOST. If empty, Django won't attempt authentication. Default: '/accounts/login/' The URL where requests are redirected for login, especially when using the login_required() decorator. This setting also accepts named URL patterns which can be used to reduce configuration duplication since you don't have to define the URL in two places (settings and URLconf). Default: '/accounts/profile/' The URL where requests are redirected after login when the contrib.auth.login view gets no next parameter. This is used by the login_required() decorator, for example. This setting also accepts named URL patterns which can be used to reduce configuration duplication since you don't have to define the URL in two places (settings and URLconf). Default: 'django.contrib.sessions.backends.db'. Controls where Django stores session data. Default: 'django.core.mail.backends.smtp.EmailBackend'. The backend to use for sending emails. Default: 'localhost'. The host to use for sending email. Default: 'sessionid'. The name of the cookie to use for sessions.This can be whatever you want (as long as it's different from the other cookie names in your application). Default: 'webmaster@localhost' Default email address to use for various automated correspondence from the site manager(s). This doesn't include error messages sent to ADMINS and MANAGERS; for that, see SERVER_EMAIL. Default: 25. Port to use for the SMTP server defined in EMAIL_HOST. Default: 2621440 (i.e. 2.5 MB). The maximum size (in bytes) that an upload will be before it gets streamed to the file system. See Managing files for details. See also DATA_UPLOAD_MAX_MEMORY_SIZE. Default: 2621440 (i.e. 2.5 MB). The maximum size in bytes that a request body may be before a SuspiciousOperation (RequestDataTooBig) is raised. The check is done when accessing request.body or request.POST and is calculated against the total request size excluding any file upload data. You can set this to None to disable the check. Applications that are expected to receive unusually large form posts should tune this setting. The amount of request data is correlated to the amount of memory needed to process the request and populate the GET and POST dictionaries. Large requests could be used as a denial-of-service attack vector if left unchecked. Since web servers don't typically perform deep request inspection, it's not possible to perform a similar check at that level. See also FILE_UPLOAD_MAX_MEMORY_SIZE. Default: False. Whether to use a TLS (secure) connection when talking to the SMTP server. This is used for explicit TLS connections, generally on port 587. If you are experiencing hanging connections, see the implicit TLS setting EMAIL_USE_SSL. Default: False. Whether to use an implicit TLS (secure) connection when talking to the SMTP server. In most email documentation this type of TLS connection is referred to as SSL. It is generally used on port 465. If you are experiencing problems, see the explicit TLS setting EMAIL_USE_TLS. Note that EMAIL_USE_TLS/EMAIL_USE_SSL are mutually exclusive, so only set one of those settings to True. Default: None. Specifies a timeout in seconds for blocking operations like the connection attempt. Default: None. The URL where requests are redirected after a user logs out using LogoutView (if the view doesn't get a next_page argument). If None, no redirect will be performed and the logout view will be rendered. This setting also accepts named URL patterns which can be used to reduce configuration duplication since you don't have to define the URL in two places (settings and URLconf). Default: [] (Empty list). List of compiled regular expression objects representing User-Agent strings that are not allowed to visit any page, systemwide. Use this for bad robots/crawlers. This is only used if CommonMiddleware is installed (see Middleware). Django Edit Edit setting: %s Edit settings Enter the new setting value. Is this settings being overridden by an environment variable? Name Namespace: %s, not found Namespaces Overridden Setting count Setting namespaces Setting updated successfully. Settings Settings in namespace: %s Settings inherited from an environment variable take precedence and cannot be changed in this view.  Settings updated, restart your installation and refresh your browser for changes to take effect. Smart settings The file storage engine to use when collecting static files with the collectstatic management command. A ready-to-use instance of the storage backend defined in this setting can be found at django.contrib.staticfiles.storage.staticfiles_storage. The full Python path of the WSGI application object that Django's built-in servers (e.g. runserver) will use. The django-admin startproject management command will create a simple wsgi.py file with an application callable in it, and point this setting to that application. The list of validators that are used to check the strength of user's passwords. URL to use when referring to static files located in STATIC_ROOT. Example: "/static/" or "http://static.example.com/" If not None, this will be used as the base path for asset definitions (the Media class) and the staticfiles app. It must end in a slash if set to a non-empty value. Value View settings Warning When set to True, if the request URL does not match any of the patterns in the URLconf and it doesn't end in a slash, an HTTP redirect is issued to the same URL with a slash appended. Note that the redirect may cause any data submitted in a POST request to be lost. The APPEND_SLASH setting is only used if CommonMiddleware is installed (see Middleware). See also PREPEND_WWW. Project-Id-Version: Mayan EDMS
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2023-01-16 06:54+0000
Last-Translator: Marwan Rahhal <Marwanr@sssit.net>, 2023
Language-Team: Arabic (https://www.transifex.com/rosarior/teams/13584/ar/)
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Language: ar
Plural-Forms: nplurals=6; plural=n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 && n%100<=10 ? 3 : n%100>=11 && n%100<=99 ? 4 : 5;
 &quot;%s&quot; ليس إدخالاً صالحًا. قيمة منطقية تحدد ما إذا كنت تريد استخدام رأس قيمة منطقية تحدد ما إذا كان سيتم استخدام رأس  قاموس يحتوي على إعدادات جميع قواعد البيانات التي سيتم استخدامها  محددات تشغيلية قائمة بجميع اللغات المتاحة. القائمة عبارة عن قائمة من مجموعتين بالتنسيق (رمز اللغة ، اسم اللغة) ع محاولة مصادقة مستخدم. قائمة بالسلاسل التي تمثل أسماء المضيف / المجال التي يمكن لهذا الموقع تقديمها. هذا إجراء أمني لمنع هجمات رأس HTTP Host ، والتي تكون ممكنة حتى في ظل العديد من تكوينات خادم الويب التي تبدو آمنة. يمكن أن تكون القيم الموجودة في هذه القائمة عبارة عن أسماء مؤهلة بالكامل محددات تشغيلية سلسلة تمثل المنطقة الزمنية لهذا التثبيت. لاحظ أن هذه ليست بالضرورة المنطقة الزمنية للخادم مجموعة تمثل مجموعة رأس / قيمة HTTP تشير إلى أن الطلب آمن. يتحكم هذا في سلوك أسلوب is_secure () الخاص بكائن الطلب. تحذير: قد يؤدي تعديل هذا الإعداد إلى تعريض أمان موقعك للخطر. تأكد من فهمك الكامل للإعداد قبل تغييره. القيمة الإفتراضية محددات تشغيلية محددات تشغيلية  يتم إعادة توجيه الطلبات لتسجيل الدخول ، خاصة عند استخدام المصمم محددات تشغيلية محددات تشغيلية الافتراضي: &quot;django.core.mail.backends.smtp.EmailBackend&quot;. الواجهة الخلفية لاستخدامها في إرسال رسائل البريد الإلكتروني. الافتراضي: &quot;localhost&quot;. المضيف المراد استخدامه لإرسال البريد الإلكتروني. محددات تشغيلية محددات تشغيلية  المنفذ المراد استخدامه لخادم البريد تحديد الحد الاقصى المسموح به لتحميل البيانات محددات تشغيلية حدث خطأ في النظام ! يرجى مراجعة مدير النظام !!    محددات تشغيلية  يحدد مهلة بالثواني لحظر العمليات مثل محاولة الاتصال. يتم إعادة توجيه الطلبات بعد تسجيل خروج المستخدم قائمة كائنات التعبير العادي المترجمة التي تمثل سلاسل وكيل المستخدم والتي لا يُسمح لها بزيارة أي صفحة على مستوى النظام. جانغو تعديل تعديل الإعداد: %s تعديل الإعدادات أدخل قيمة الإعداد الجديد. هل تم الغاء هذه الإعدادات بواسطة متغير بيئة؟ اسم  %s ، غير موجود المساحة تم الإلغاء عدد الإعدادات تحديد مساحات الأسماء تم تحديث الإعداد بنجاح. إعدادات الإعدادات في مساحة الاسم: %s الإعدادات الموروثة من متغير البيئة لها الأسبقية ولا يمكن تغييرها في طريقة العرض هذه. تم تحديث الإعدادات ، قم بإعادة تحميل لإحداث التغير الإعدادات الذكية محرك تخزين الملفات المراد استخدامه عند تجميع الملفات الثابتة باستخدام أمر الإدارة التجميعية. يمكن العثور على نسخة جاهزة للاستخدام لخلفية التخزين المحددة  تحديد مسار العمل قوة كلمات مرور المستخدم. عند الإشارة إلى الملفات الثابتة الموجودة في ، فسيتم استخدامه كمسار أساسي لتعريفات الأصول  قيمة استعراض الإعدادات تحذير عند التعيين على True ، إذا كان عنوان URL للطلب لا يتطابق مع أي من الأنماط الموجودة في URLconf ولا ينتهي بشرطة مائلة ، يتم إصدار إعادة توجيه HTTP إلى نفس عنوان URL مع إلحاق شرطة مائلة. لاحظ أن إعادة التوجيه قد تتسبب في فقد أي بيانات تم إرسالها في طلب POST. 