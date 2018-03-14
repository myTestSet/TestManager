//全局变量
var PRODUCT_HOST = 'http://ak-code.hikop.com'

var ERRORCODE = {
  SUCCESS: 0,
  UNKNOWN: 1,
  FAILED: 2,
  IN_BLACKLIST: 6,
  PARAM_ERROR: 12,
  NOT_FOUND: 13,
  NOT_LOGIN: 14
};

function msg_info(msg, type, timeout) {
  if (!type) type = 'info';
  if (!timeout) timeout = 3000;
  var id = (new Date).getTime() + '' + parseInt(Math.random() * 100);
  var msg_html = '<div class="pad margin no-print" id="' + id + '">' +
    '<div class="callout callout-' + type + '" style="margin-bottom: 0!important;">' +
    '<h4><i class="fa fa-info"></i>&nbsp;&nbsp;' + msg + '</h4>' +
    '</div>' +
    '</div>';
  $('.content-header').after(msg_html);
  setTimeout(function () {
    $("#" + id).fadeOut();
  }, timeout);
  window.location.href = '#message-top';
}

$.fn.serializefiles = function() {
  var obj = $(this);
  /* ADD FILE TO PARAM AJAX */
  var formData = new FormData();
  $.each($(obj).find("input[type='file']"), function(i, tag) {
      $.each($(tag)[0].files, function(i, file) {
          formData.append(tag.name, file);
      });
  });
  var params = $(obj).serializeArray();
  $.each(params, function (i, val) {
      formData.append(val.name, val.value);
  });
  return formData;
};

//获取url中的参数
function getUrlParam(name) {
  var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
  var r = window.location.search.substr(1).match(reg);  //匹配目标参数
  if (r != null) return unescape(r[2]); return null; //返回参数值
}

// 设置菜单active状态
function setMenuActive() {
  var url = window.location.pathname || '/';
  if(url == "/" || url == "/manager/"|| url == "/manager/order/order-list"){
    $("li.treeview.order").addClass("active");
  }else if(url.indexOf("/manager/common_code/") > -1){
    $("li.treeview.common_code").addClass("active");
  }else if(url.indexOf("manager/order/refund-list") > -1){
    $("li.treeview.refund").addClass("active");
  }else if(url.indexOf("/manager/order/invoice-list") > -1){
    $("li.treeview.order-invoice").addClass("active");
  }else if(url.indexOf("/product/product-list") > -1){
    $("li.treeview.product").addClass("active");
  }
}

$(function(){
  //设置提示消息自动隐藏
  setTimeout(function () {
    $(".dmsg").fadeOut();
  }, 3000);

  //设置菜单active
  setMenuActive()
});
