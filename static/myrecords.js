$(document).ready(function() {
    $(" [class*='rec-edt-btn-']").click(function(){
     var form = $(this).closest("form");
     $("." + form.attr('class')+ " input[type=button]").hide();
     $("." + form.attr('class')+ " input[type=submit]").show();
     $("." + form.attr('class')+ ' input[type=text]').removeAttr('disabled');
     $("." + form.attr('class')+ ' input[name=cname]').removeAttr('type');
     $("." + form.attr('class')+ ' input[name=dcode]').removeAttr('type');

 });

 $(" [class*='rec-done-btn-']").click(function(){
     var form = $(this).closest("form");
     form.attr('method','post');
     form.attr('action','/recordedit');
 });

 $(" [class*='rec-del-btn-']").click(function(){
     var name = $(this).attr('class');
     name = name.substring(12);
     var form = $(this).closest("form");
     form.attr('method','post');
     form.attr('action','/recorddelete/' + name);
 });

 $( "[class*='record-form-'] input[type=text]" ).attr('disabled','disabled');
 $( "[class*='rec-done-btn-']" ).hide();
});