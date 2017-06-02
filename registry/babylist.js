javascript:(
function(){
  var w=window, 
      l=w.location, 
      d=w.document, 
      s=d.createElement('script'), 
      e=encodeURIComponent, 
      o='object', 
      n='BabyUS', 
      u='https://www.babylist.com/add_reg_item', 
      r='readyState', 
      T=setTimeout,
      a='setAttribute',
      g=function(){
        d[r] && d[r]!='complete' && d[r] !='interactive' ? 
          T(g,200):
          !w[n] ? 
            (s[a]('charset','UTF-8'),s[a]('src',u+'.js?loc='+e(l)+'&b='+n+'&format=js'),d.body.appendChild(s),f()):
            f()
      },
      f=function(){
        !w[n] ?
          T(f,200):
          w[n].showPopover()
      };
  typeof s != o ?
    l.href = u + '?u=' + e(l) + '&t=' + e(d.title):
    g()
}())