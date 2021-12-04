$(document).ready(function() {
    if($_SESSION['logged_in'] == 1) {
        ("body").hide();
    }

       $(" [class*='dis-edt-btn-']").click(function(){
        var form = $(this).closest("form");
        $("." + form.attr('class')+ " input[type=button]").hide();
        $("." + form.attr('class')+ " input[type=submit]").show();
        $("." + form.attr('class')+ ' input[type=text]').removeAttr('disabled');
        $("." + form.attr('class')+ ' textarea').removeAttr('disabled');
    });

    $(" [class*='dis-done-btn-']").click(function(){
        var form = $(this).closest("form");
        form.attr('method','post');
        form.attr('action','/diseaseedit');
    });

    $(" [class*='dis-del-btn-']").click(function(){
        var name = $(this).attr('class');
        name = name.substring(12);
        var form = $(this).closest("form");
        form.attr('method','post');
        form.attr('action','/diseasedelete/' + name);
    });

    $( "[class*='my-dis-form-'] input[type=text], [class*='my-dis-form-'] textarea" ).attr('disabled','disabled');
    $( "[class*='dis-done-btn-']" ).hide();
});