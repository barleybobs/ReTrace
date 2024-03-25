# Meta Refresh Testing

All testing was carried out in Chrome 123.0.6312.58 on Windows 11.

When there are multiple meta redirects then you will be redirected to the one with the shortest delay. If there are multiple redirects with the same delay then you will be redirected to the one which is the last in the source code.

## Valid Meta Refreshes

-   Delay can be followed by ; or ,
-   URL can be https://, http:// **_(See [Odd Behaviour](#odd-behaviour))_**
-   url= is optional and does not have to be used
-   Quotes around url= are optional
-   When https or http is not used and the url just begins with // it still redirects to the url but will use the protocol that was used for the page that is redirecting it
-   The URL can be relative
-   The delay can have a decimal point **_(See [Odd Behaviour](#odd-behaviour))_**

```html
<meta http-equiv='refresh' content='0; url=https://google.com'>         <!-- Goes to https://google.com -->
<meta http-equiv='refresh' content='0, https://google.com'>
<meta http-equiv='refresh' content='0 url=https://google.com'>
<meta http-equiv='refresh' content='0; url="https://google.com"'>
<meta http-equiv='refresh' content='0; url=//google.com'>           
<meta http-equiv='refresh' content='0; url=test'>                       <!-- Goes to https://yoursite.com/previouspath/test -->
<meta http-equiv='refresh' content='1.1; url=https://google.com'>       <!-- Goes to https://google.com after 1.1s -->
<meta http-equiv='refresh' content='0;'>                                <!-- Reloads after 0s -->
<meta http-equiv='refresh' content='0; url='>
```

## Invalid Meta Refreshes

-   Must include delay
-   Delay must be numerical _(cannot be letters)_
-   Quotes must not be broken

```html
<meta http-equiv='refresh' content='url=https://google.com'>
<meta http-equiv='refresh' content='url=https:google.com'>
<meta http-equiv='refresh' content='https://google.com'>
<meta http-equiv='refresh' content='https:google.com'>
<meta http-equiv='refresh' content='a; url=https://google.com'>
<meta http-equiv='refresh' content='0; url='https://google.com"'>
```

## Odd Behaviour

-   When using https: or https:/ chrome acts as though the link was https://
-   When using http: or http:/ chrome drops this and will use it as a relative url.
-   When using https:/// or http:/// or any other length of / above the normal 2 then it will act as the relevant https:// or http://
-   They still work if they have multiple decimal points. It appears that everything after the second decimal point is ignored

```html
<meta http-equiv='refresh' content='0; url=https:google.com'>           <!-- Goes to https://google.com -->
<meta http-equiv='refresh' content='0; url=https:/google.com'>
<meta http-equiv='refresh' content='0; url=https:///google.com'>
<meta http-equiv='refresh' content='0; url=http:///google.com'>
<meta http-equiv='refresh' content='0; url=http:google.com'>            <!-- Goes to https://yoursite.com/previouspath/google.com -->
<meta http-equiv='refresh' content='0; url=http:/google.com'>           <!-- Goes to https://yoursite.com/previouspath/google.com -->
<meta http-equiv='refresh' content='1.1.1; url=https://google.com'>     <!-- Goes to https://google.com after 1.1s -->
```