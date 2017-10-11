/**
 * Created by nyloner on 2017/9/8.
 */
! function(e, t) {
    "object" == typeof exports && "object" == typeof module ? module.exports = t() : "function" == typeof define && define.amd ? define([], t) : "object" == typeof exports ? exports.Showcase = t() : e.Showcase = t()
}(this, function() {
    return function(e) {
        function t(n) {
            if (o[n]) return o[n].exports;
            var r = o[n] = {
                i: n,
                l: !1,
                exports: {}
            };
            return e[n].call(r.exports, r, r.exports, t), r.l = !0, r.exports
        }
        var o = {};
        return t.m = e, t.c = o, t.d = function(e, o, n) {
            t.o(e, o) || Object.defineProperty(e, o, {
                configurable: !1,
                enumerable: !0,
                get: n
            })
        }, t.n = function(e) {
            var o = e && e.__esModule ? function() {
                return e.default
            } : function() {
                return e
            };
            return t.d(o, "a", o), o
        }, t.o = function(e, t) {
            return Object.prototype.hasOwnProperty.call(e, t)
        }, t.p = "", t(t.s = 0)
    }([function(e, t, o) {
        e.exports = o(1)
    }, function(e, t, o) {
        "use strict";

        function n(e) {
            return e && e.__esModule ? e : {
                default: e
            }
        }
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.Intro = void 0;
        var r = o(2),
            f = o(5),
            u = (n(f), o(6));
        n(u);
        t.Intro = r.Intro
    }, function(e, t, o) {
        "use strict";
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), t.Intro = void 0;
        var n = o(3),
            r = function(e) {
                return e && e.__esModule ? e : {
                    default: e
                }
            }(n);
        t.Intro = r.default
    }, function(e, t, o) {
        "use strict";
        Object.defineProperty(t, "__esModule", {
            value: !0
        });
        var n = o(4),
            r = function(e) {
                return e && e.__esModule ? e : {
                    default: e
                }
            }(n),
            f = void 0,
            u = void 0,
            i = void 0,
            d = void 0,
            s = void 0,
            c = void 0,
            l = void 0,
            a = void 0,
            p = function() {
                var e = window.scrollY;
                e > 300 && (e = 300), f.style.transform = "rotateX(" + (40 - e / 300 * 40) + "deg) translateY(-" + (200 - e / 300 * 200) + "px)"
            },
            v = function() {
                window.scrollY - s > -600 && u.classList.add("in")
            },
            y = function() {
                window.scrollY - c > -600 && i.classList.add("in")
            },
            b = function() {
                var e = window.scrollY;
                !a && e - l > -300 && (d.play(), a = !0)
            },
            _ = function() {
                p(), v(), y(), b()
            },
            w = function() {
                f = r.default.byId("mockup"), u = r.default.byId("design-canvas"), i = r.default.byId("ux-canvas"), d = r.default.byId("video"), s = r.default.getTop(u), c = r.default.getTop(i), l = r.default.getTop(d), a = !1, _(), window.addEventListener("scroll", _)
            };
        t.default = w
    }, function(e, t, o) {
        "use strict";
        Object.defineProperty(t, "__esModule", {
            value: !0
        });
        var n = {};
        n.getOffset = function(e) {
            for (var t = 0, o = 0; e && !isNaN(e.offsetLeft) && !isNaN(e.offsetTop);) t += e.offsetLeft - e.scrollLeft, o += e.offsetTop - e.scrollTop, e = e.offsetParent;
            return {
                top: o,
                left: t
            }
        }, n.getTop = function(e) {
            var t = 0;
            if (e.offsetParent)
                do {
                    t += e.offsetTop
                } while (e = e.offsetParent);
            return [t]
        }, n.byId = function(e) {
            return document.getElementById(e)
        }, t.default = n
    }, function(e, t) {}, function(e, t) {}])
});
