(function (name, context, definition) {
    'use strict'
    if (typeof window.define === 'function' && window.define.amd) { window.define(definition) } else if (typeof module !== 'undefined' && module.exports) { module.exports = definition() } else if (context.exports) { context.exports = definition() } else { context[name] = definition() }
  })('Test', this, function () {
    'use strict'
    var Test = function () {
      if (!(this instanceof Test)) {
        return new Test()
      }
    }
    
    Test.prototype = {
        name:"abc_test",
        init:function(){
        },
        ajax: function(url, success, error) {
        var data = {
            name: this.name };
        var text = window.JSON.stringify(data);
        if (!window.XMLHttpRequest || "withCredentials" in new window.XMLHttpRequest) {
          if (window.XMLHttpRequest) {
            var xhr = new window.XMLHttpRequest;
            xhr.open("POST", url, true),
              xhr.setRequestHeader("Content-Type", "text/plain;charset=utf-8"),
              xhr.setRequestHeader("Accept", "application/json"),
              xhr.withCredentials = true,
              xhr.onload = function() {
                success(window.JSON.parse(xhr.responseText))
              },
              xhr.onreadystatechange = function() {
                4 === xhr.readyState && (200 === xhr.status ? success(window.JSON.parse(xhr.responseText)) : error({
                  error: "status: " + xhr.status
                }))
              },
              xhr.send(text)
          }
        } else {
          var protocol = window.location.protocol,
            xdr = new window.XDomainRequest; - 1 === url.indexOf(protocol) && (url = url.replace(/^https?:/, protocol)),
            xdr.open("POST", url),
            xdr.ontimeout = function() {
              "function" == typeof error && error({
                error: "timeout"
              })
            },
            xdr.onerror = function() {
              "function" == typeof error && error({
                error: "error"
              })
            },
            xdr.onload = function() {
              "function" == typeof success && success(window.JSON.parse(xdr.responseText))
            },
            xdr.send(text)
        }
      }

    }

    Test.VERSION = '0.5.1'
    return Test
})